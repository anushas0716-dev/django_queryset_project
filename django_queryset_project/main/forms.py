from django import forms
from .models import Student, Course


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email', 'course']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 120}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
