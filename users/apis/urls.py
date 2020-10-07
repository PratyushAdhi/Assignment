from django.contrib import admin
from django.urls import path
from .views import StudentListAPIView, TeacherCreateAPIView, TeacherListAPIView, StudentCreateAPIView, StudentRetrieveAPIView, TeacherRetrieveAPIView, AdminUserRetrieveAPIView

urlpatterns = [
    path("admins/<str:username>/",AdminUserRetrieveAPIView.as_view(), name="admin-retrieve"),
    path("students/", StudentListAPIView.as_view(), name="student-list"),
    path("students/create/", StudentCreateAPIView.as_view(), name="student-create"),
    path("students/<str:username>/", StudentRetrieveAPIView.as_view(),name="student-retrieve"),
    path("teachers/", TeacherListAPIView.as_view(), name="teacher-list"),
    path("teacher/create/", TeacherCreateAPIView.as_view(), name="teacher-create"),
    path("teacher/<str:username>/", TeacherRetrieveAPIView.as_view(),name="teacher-retrieve"),
]
