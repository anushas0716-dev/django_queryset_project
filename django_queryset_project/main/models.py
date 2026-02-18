from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(blank=True, default='')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (age {self.age})"
