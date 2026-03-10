from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from home.forms import TeacherForm, StudentForm
from home.models import Student, Teacher


class StudentRegistrationPost(View):

    def get(self, request):
        teacher_form = TeacherForm()
        student_form = StudentForm()

        # ================== fetch queries ==================

        # students = Student.objects.all()

        # students = Student.objects.filter(department='BBA') # filter by department

        # students = Student.objects.filter(department='BBA', age__gt=20) # filter by department and age

        # students = Student.objects.exclude(department='BBA') # exclude by department

        # students = Student.objects.order_by('name') # order by name

        # students = Student.objects.order_by('-name') # order by name descending

        # students = Student.objects.order_by('?') # random order

        # students = Student.objects.order_by('pk').reverse()[:5] # reverse order and limit to 5

        # students = Student.objects.values() # return dictionary

        # students = Student.objects.values('name','department') # return dictionary with specific fields

        # students = Student.objects.values_list('name','department') # return tuple

        # students = Student.objects.values_list('name','department', named=True) # return named tuple
        """
            students = Student.objects.values_list('name', 'department')
            # becurse we are using tuple so we can access the values by index
            {% for student in students %}

            <p>{{ student.0 }} - {{ student.1 }}</p>

            {% endfor %}
        """

        # students = Student.objects.using('default') # use default database

        # students = Student.objects.dates('passed_in_year','year', order='DESC') # get dates

        # specific query
        # students = Student.objects.get(pk=1) # get single object
        # students = get_object_or_404(Student, pk=1) # get single object or 404

        # students = Student.objects.get(name='John') # get single object

        # students = Student.objects.first()

        # students = Student.objects.last()

        # students = Student.objects.latest('created_at')

        # students = Student.objects.earliest('created_at')

        # students = Student.objects.filter(roll__lt=10)

        # students = Student.objects.filter(roll__gt=5)

        # students = Student.objects.filter(roll__lte=10)

        # students = Student.objects.filter(roll__gte=5)

        # students = Student.objects.filter(department__exact='BBA')

        # students = Student.objects.filter(name__iexact='john')

        # students = Student.objects.filter(name__contains='John')

        # students = Student.objects.filter(name__icontains='john')

        # students = Student.objects.filter(name__startswith='J')

        # students = Student.objects.filter(name__endswith='n')

        # students = Student.objects.filter(name__regex=r'^J')

        # students = Student.objects.filter(name__iregex=r'^j')

        # students = Student.objects.filter(roll__range=(101,110))

        students = Student.objects.filter(id__in=[1,2,3]) # filter by id

        # ================== single object ==================

        student = get_object_or_404(Student, pk=1) # get single object or 404

        # ================== aggregation ==================

        from django.db.models import Count, Avg, Max, Min, Sum
        # aggregate is used to perform calculations on a set of values return a dictionary
        # total_students = Student.objects.aggregate(Count('id'))
        # total_students = Student.objects.aggregate(total=Count('id'))
        # total_students = Student.objects.aggregate(total=Count('id'), avg_age=Avg('age'))
        # total_students = Student.objects.aggregate(total=Count('id'), max_age=Max('age'), min_age=Min('age'))
        # total_students = Student.objects.aggregate(total=Count('id'), sum_age=Sum('age'))
        # total_students = Student.objects.aggregate(total=Count('id'), avg_age=Avg('age'), max_age=Max('age'), min_age=Min('age'), sum_age=Sum('age'))
        
        # ========================== annotate ==========================
        # annotate is used to add calculated fields to each object in a queryset
        total_students = Student.objects.annotate(total=Count('id'))
        
        # ================== context ==================

        context = {
            "teacher_form": teacher_form,
            "student_form": student_form,
            "students": students,
            "student": student,
            "total_students": total_students

        }

        return render(request,"home.html",context)

    def post(self, request):

        teacher_form = TeacherForm(request.POST)
        student_form = StudentForm(request.POST)

        if 'teacher_submit' in request.POST:
            if teacher_form.is_valid():
                teacher_form.save()
                return redirect('StudentRegistrationPost')

        if 'student_submit' in request.POST:
            if student_form.is_valid():
                student_form.save()
                return redirect('StudentRegistrationPost')

        # teachers = Teacher.objects.all()

        context = {
            "teacher_form": teacher_form,
            "student_form": student_form,
            # 'teachers': teachers,
            "students": students,
            "student": student,
            "total_students": total_students
        }

        return render(request, 'home.html', context)