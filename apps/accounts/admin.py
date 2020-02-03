from django.contrib import admin
from .models import CustomUser, Field, Advisor, Student


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    model = CustomUser


@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    model = Advisor


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    model = Field


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    model = Student

