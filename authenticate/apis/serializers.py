from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import reverse
from users.models import User
from .utils import Utils

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length = 50)
    password = serializers.CharField(max_length = 50,write_only = True)


    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")
        password = attrs.get("password", "")
        return attrs

    def create(self, validated_data):
        email = validated_data.get("email")
        username = validated_data.get("username")
        password = validated_data.get("password")
        return User.objects.create_user(email, username, password)

    class Meta:
        model = User
        fields = ("username", "email", "password")


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length = 50, read_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)


    class Meta:
        model = User
        fields = ["email", "username", "password", "tokens"]

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid Credentials")

        return {
            "email": email,
            "password": password,
            "tokens": user.tokens()
        }

        return super().validate(attrs)


class RequestPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("email",)

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50, write_only =True)
    token = serializers.CharField(write_only =True)
    uidb64 = serializers.CharField(max_length = 255, write_only =True)

    # fields = ("password", "token", "uidb64",)

    def validate(self, attrs):
        try:
            password = attrs.get("password", "")
            token = attrs.get("token", "")
            uidb64 = attrs.get("uidb64", "")
            print(uidb64)
            id = force_str(urlsafe_base64_decode(uidb64))
            print(id)
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Invalid Reset Parameter", 401)
            user.set_password(password)
            user.save()
            return user
        except Exception:
            raise AuthenticationFailed("Invalid Reset Parameter", 401)
        return super().validate(attrs)
