from django.urls import path
from . import views

urlpatterns = [
    # Home / dashboard
    path('', views.home, name='home'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # QuerySet demo
    path('demo/', views.queryset_demo, name='queryset_demo'),
]
