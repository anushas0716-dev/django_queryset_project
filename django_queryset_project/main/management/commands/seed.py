from django.core.management.base import BaseCommand
from main.models import Course, Student


class Command(BaseCommand):
    help = 'Seed the database with sample courses and students'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Student.objects.all().delete()
        Course.objects.all().delete()

        # Create courses
        python_course = Course.objects.create(
            title='Python',
            description='Learn Python programming from scratch.'
        )
        django_course = Course.objects.create(
            title='Django',
            description='Build web apps with Django.'
        )
        js_course = Course.objects.create(
            title='JavaScript',
            description='Master modern JavaScript and ES6+.'
        )

        # Create students
        students = [
            Student(name='John',    age=22, email='john@example.com',  course=python_course),
            Student(name='Sara',    age=19, email='sara@example.com',  course=python_course),
            Student(name='Ali',     age=25, email='ali@example.com',   course=django_course),
            Student(name='Maria',   age=21, email='maria@example.com', course=django_course),
            Student(name='James',   age=17, email='james@example.com', course=js_course),
            Student(name='Fatima',  age=30, email='fatima@example.com',course=python_course),
            Student(name='Carlos',  age=23, email='carlos@example.com',course=js_course),
            Student(name='Aisha',   age=20, email='aisha@example.com', course=django_course),
        ]
        Student.objects.bulk_create(students)

        self.stdout.write(self.style.SUCCESS(
            f'✅  Seeded {Course.objects.count()} courses and {Student.objects.count()} students.'
        ))
