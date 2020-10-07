from rest_framework import serializers
from ..models import Student, Teacher, AdminUser


class StudentSerializer(serializers.ModelSerializer):
    lookup_field = "username"

    class Meta:
        model = Student
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        model = Teacher
        fields = "__all__"


class AdminUserSerializer(serializers.ModelSerializer):
    lookup_field = "username"

    class Meta:
        model = AdminUser
        fields = "__all__"
