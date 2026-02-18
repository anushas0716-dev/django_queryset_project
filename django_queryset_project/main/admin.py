from django.contrib import admin
from .models import Course, Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('title',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'email', 'course', 'enrolled_at')
    list_filter = ('course',)
    search_fields = ('name', 'email')
    ordering = ('name',)
