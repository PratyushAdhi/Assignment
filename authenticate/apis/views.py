from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import reverse
from users.models import User
from .serializers import RegisterSerializer, RequestPasswordResetEmailSerializer, SetNewPasswordSerializer, LoginSerializer
from .utils import Utils

#Registers a new user.
class RegisterAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = RegisterSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        return Response(data=user_data, status=status.HTTP_201_CREATED)

#Logs in an existing user
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

#Requests for password reset. Email is sent to registered ID.
class RequestPasswordResetEmailAPIView(GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists(): #check if this user of given email exists
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relative_link = reverse(
                'password-reset', kwargs={'uidb64': uidb64, 'token': token})
            absurl = "http://" + current_site + relative_link
            email_body = absurl
            data = {
                "email_body": email_body,
                "email_subject": "Verify Email",
                "to_email": user.email
            }
            Utils.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(GenericAPIView): #routes from the link sent by email to a
    # page where access token and uidb are given, which acn be used to change password

    def get(self, request, uidb64, token):
        try:
            id = smart_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Try again"}, status=status.HTTP_401_UNAUTHORIZED
                )

            return Response({
                "success": True,
                "message": "Validation Complete",
                "uidb64": uidb64,
                "token": token
            }, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({
                "error": "Token invalid"
            }, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetNewPasswordAPIView(GenericAPIView):
    #password reset.
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        user = request.data
        serializer = SetNewPasswordSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        return Response({
            "message": "password reset"},
            status=status.HTTP_200_OK
        )