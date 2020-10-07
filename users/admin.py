from django.contrib import admin
from .models import User, AdminUser, Teacher, Student
# Register your models here.
admin.site.register(User)
admin.site.register(AdminUser)
admin.site.register(Teacher)
admin.site.register(Student)