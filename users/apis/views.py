from rest_framework.generics import (ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from .permissions import IsTeacherOrAdmin, IsOwnerOrTeacherOrAdmin, IsAdmin, IsOwnerOrAdmin
from .serializers import StudentSerializer, TeacherSerializer, AdminUserSerializer
from ..models import Student, Teacher, AdminUser
from rest_framework.permissions import IsAdminUser


class StudentListAPIView(ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsTeacherOrAdmin,IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_teacher:
            return Student.objects.all()
        else:
            return Student.objects.get(email=self.request.user.email)



class StudentRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsOwnerOrTeacherOrAdmin,IsAdmin,IsAdminUser]
    lookup_field = "username"

class StudentCreateAPIView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsTeacherOrAdmin,IsAdminUser]


class TeacherListAPIView(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer(many=True)
    permission_classes = [IsAdmin,IsAdminUser]



class TeacherCreateAPIView(CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin,IsAdminUser]


class TeacherRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = "username"
    permission_classes = [IsOwnerOrAdmin,IsAdminUser]
#
#
class AdminUserRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    lookup_field = "username"
    permission_classes = [IsAdmin,IsAdminUser]

    def get_queryset(self):
        return AdminUser.objects.get(email=self.user.email)