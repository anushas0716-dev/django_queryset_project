# Django QuerySet Demo Project

A fully working Django project demonstrating all core QuerySet operations from the lesson, with a live interactive web UI.

---

## 📁 Project Structure

```
django_queryset_project/
├── manage.py
├── requirements.txt
├── django_queryset_project/
│   ├── settings.py
│   └── urls.py
├── main/
│   ├── models.py          ← Course and Student models
│   ├── views.py           ← All views with QuerySet examples
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── management/
│       └── commands/
│           └── seed.py    ← Populates sample data
└── templates/
    ├── base.html
    └── main/
        ├── home.html
        ├── queryset_demo.html   ← 🔑 Main learning page
        ├── student_list.html    ← Live filter demo
        ├── student_form.html
        ├── course_list.html
        ├── course_detail.html
        └── confirm_delete.html
```

---

## 🚀 Setup (takes ~2 minutes)

### 1. Create virtual environment and install Django

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run migrations (creates the SQLite database)

```bash
python manage.py migrate
```

### 3. Seed sample data

```bash
python manage.py seed
```

This creates 3 courses (Python, Django, JavaScript) and 8 students.

### 4. Create admin user

```bash
python manage.py createsuperuser
# or use the quick version:
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin','','admin')"
```

### 5. Run the server

```bash
python manage.py runserver
```

Open: **http://127.0.0.1:8000**

---

## 🌐 Pages

| URL | What it shows |
|-----|---------------|
| `/` | Dashboard — count, avg age, all students, annotated courses |
| `/demo/` | **QuerySet Demo** — all operations with live results |
| `/students/` | Filterable student list (icontains, gte, lte, FK lookup) |
| `/courses/` | Course list with annotated student counts |
| `/courses/<id>/` | Course detail with aggregate stats |
| `/admin/` | Django admin |

---

## 🧪 Practice in the Django Shell

```bash
python manage.py shell
```

```python
from main.models import Course, Student
from django.db.models import Q, Avg, Max, Min, Count

# ── CREATE
c1 = Course.objects.create(title="Python")
Student.objects.create(name="John", age=22, course=c1)

# ── READ
Student.objects.all()
Student.objects.filter(age__gt=20)
Student.objects.filter(name__icontains="jo")
Student.objects.get(id=1)

# ── FILTER LOOKUPS
Student.objects.filter(age__range=(18, 25))
Student.objects.filter(name__startswith="J")
Student.objects.filter(course__title="Python")   # FK lookup

# ── Q OBJECTS
Student.objects.filter(Q(age__lt=20) | Q(age__gt=24))
Student.objects.filter(~Q(course__title="Python"))

# ── AGGREGATION
Student.objects.aggregate(Avg("age"), Max("age"), Count("id"))

# ── ANNOTATION
Course.objects.annotate(student_count=Count("students"))

# ── values / values_list
Student.objects.values("name", "age")
Student.objects.values_list("name", flat=True)

# ── UPDATE
Student.objects.filter(course__title="Python").update(age=25)

# ── DELETE
Student.objects.filter(age__lt=18).delete()
```

---

## 📚 QuerySet Lookup Cheat Sheet

| Lookup | SQL equivalent |
|--------|---------------|
| `field__exact` | `= value` |
| `field__iexact` | `= value` (case-insensitive) |
| `field__contains` | `LIKE '%value%'` |
| `field__icontains` | `LIKE '%value%'` (case-insensitive) |
| `field__startswith` | `LIKE 'value%'` |
| `field__endswith` | `LIKE '%value'` |
| `field__gt` | `> value` |
| `field__gte` | `>= value` |
| `field__lt` | `< value` |
| `field__lte` | `<= value` |
| `field__range` | `BETWEEN a AND b` |
| `field__in` | `IN (...)` |
| `field__isnull` | `IS NULL` / `IS NOT NULL` |
| `related__field` | `JOIN` on FK |
