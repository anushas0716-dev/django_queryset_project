from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg, Max, Min, Count, Sum
from .models import Course, Student
from .forms import StudentForm, CourseForm


# ─── HOME ────────────────────────────────────────────────────────────────────

def home(request):
    """Dashboard showing QuerySet demo results."""
    context = {
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
        'all_students': Student.objects.select_related('course').order_by('name'),
        'all_courses': Course.objects.annotate(student_count=Count('students')),
        'avg_age': Student.objects.aggregate(avg=Avg('age'))['avg'],
        'oldest': Student.objects.order_by('-age').first(),
        'youngest': Student.objects.order_by('age').first(),
    }
    return render(request, 'main/home.html', context)


# ─── STUDENTS ────────────────────────────────────────────────────────────────

def student_list(request):
    """List students with live filtering — demonstrates QuerySet lookups."""
    qs = Student.objects.select_related('course')

    # Search by name (icontains)
    name_q = request.GET.get('name', '').strip()
    if name_q:
        qs = qs.filter(name__icontains=name_q)

    # Filter by min age
    min_age = request.GET.get('min_age', '').strip()
    if min_age.isdigit():
        qs = qs.filter(age__gte=int(min_age))

    # Filter by max age
    max_age = request.GET.get('max_age', '').strip()
    if max_age.isdigit():
        qs = qs.filter(age__lte=int(max_age))

    # Filter by course
    course_id = request.GET.get('course', '').strip()
    if course_id.isdigit():
        qs = qs.filter(course_id=int(course_id))

    # Ordering
    order = request.GET.get('order', 'name')
    if order in ('name', '-name', 'age', '-age', 'course__title'):
        qs = qs.order_by(order)

    context = {
        'students': qs,
        'courses': Course.objects.all(),
        'filters': request.GET,
        'count': qs.count(),
    }
    return render(request, 'main/student_list.html', context)


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'main/student_form.html', {'form': form, 'title': 'Add Student'})


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'main/student_form.html', {'form': form, 'title': f'Edit {student.name}'})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'main/confirm_delete.html', {'obj': student, 'type': 'Student'})


# ─── COURSES ─────────────────────────────────────────────────────────────────

def course_list(request):
    courses = Course.objects.annotate(student_count=Count('students')).order_by('title')
    return render(request, 'main/course_list.html', {'courses': courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    students = course.students.all().order_by('name')
    stats = students.aggregate(avg_age=Avg('age'), max_age=Max('age'), min_age=Min('age'), total=Count('id'))
    return render(request, 'main/course_detail.html', {'course': course, 'students': students, 'stats': stats})


def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'main/student_form.html', {'form': form, 'title': 'Add Course'})


def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'main/confirm_delete.html', {'obj': course, 'type': 'Course'})


# ─── QUERYSET DEMO ────────────────────────────────────────────────────────────

def queryset_demo(request):
    """
    Interactive page showing all QuerySet operations with live results.
    Each section corresponds to a concept from the lesson.
    """
    from django.db.models import Q

    demo = {}

    # Basic reads
    demo['all_students'] = list(Student.objects.all().values('id', 'name', 'age', 'course__title'))
    demo['count'] = Student.objects.count()
    demo['first'] = Student.objects.first()
    demo['last'] = Student.objects.last()

    # Filter lookups
    demo['age_gt_20'] = list(Student.objects.filter(age__gt=20).values('name', 'age'))
    demo['name_contains_a'] = list(Student.objects.filter(name__icontains='a').values('name', 'age'))
    demo['age_range'] = list(Student.objects.filter(age__range=(18, 23)).values('name', 'age'))

    # Q objects — OR / NOT
    demo['q_or'] = list(Student.objects.filter(Q(age__lt=20) | Q(age__gt=24)).values('name', 'age'))
    demo['q_not'] = list(Student.objects.filter(~Q(course__title='Python')).values('name', 'age', 'course__title'))

    # Aggregation
    demo['aggregates'] = Student.objects.aggregate(
        avg_age=Avg('age'),
        max_age=Max('age'),
        min_age=Min('age'),
        total=Count('id'),
    )

    # Annotation
    demo['courses_annotated'] = list(
        Course.objects.annotate(student_count=Count('students')).values('title', 'student_count')
    )

    # values / values_list
    demo['values'] = list(Student.objects.values('name', 'age'))
    demo['values_list'] = list(Student.objects.values_list('name', flat=True))

    # exists
    demo['has_students'] = Student.objects.exists()
    demo['has_young'] = Student.objects.filter(age__lt=18).exists()

    # Order by
    demo['ordered_asc'] = list(Student.objects.order_by('age').values('name', 'age'))
    demo['ordered_desc'] = list(Student.objects.order_by('-age').values('name', 'age'))

    return render(request, 'main/queryset_demo.html', {'demo': demo})
