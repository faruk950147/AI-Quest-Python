from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from home.forms import TeacherForm, StudentForm
from home.models import Student, Teacher


class StudentRegistrationPost(View):

    def get(self, request):
        teacher_form = TeacherForm()
        student_form = StudentForm()
        # ================== fetch queries ==================
        
        # students = Student.objects.all() # return all students objects
        # Get students with department 'BBA' 
        # students = Student.objects.filter(department='BBA') 
        # Get students with department 'BBA' and age greater than 20
        # students = Student.objects.filter(department='BBA', age__gt=20)
        # students = Student.objects.exclude(department='BBA')
        # order_by
        # students = Student.objects.order_by('name')
        # students = Student.objects.order_by('-name')
        # random order
        # students = Student.objects.order_by('?')
        # order by pk
        # students = Student.objects.order_by('pk').reverse()[:5]
        # values for fields
        # students = Student.objects.values()
        # only specific fields
        # students = Student.objects.values('name', 'department')
        # return tuple so don't show values with it
        # students = Student.objects.values_list()
        # students = Student.objects.values_list('name', 'department', named=True)
        """
        students = Student.objects.values_list('name', 'department')
        # becurse we are using tuple so we can access the values by index
        {% for student in students %}

        <p>{{ student.0 }} - {{ student.1 }}</p>

        {% endfor %}
        """
        # return a queryset object with using('default') method
        # students = Student.objects.using('default')
        
        # dates
        # students = Student.objects.dates('passed_in_year', 'year', order='DESC')
        
        # get by pk
        # students = Student.objects.get(pk=1)
        # get by name
        # students = Student.objects.get(name='John')
        # get by department
        # students = Student.objects.get(department='BBA')
        # first by
        # students = Student.objects.first()
        # students = Student.objects.order_by('pk').first()
        # last
        # students = Student.objects.order_by('-pk').first()
        # students = Student.objects.get(pk=3)
        # students = get_object_or_404(Student, pk=3)
        # last by
        # students = Student.objects.last()
        # lastest
        # students = Student.objects.latest('created_at')
        # earlist
        # students = Student.objects.earliest('created_at')
        # count
        # students = Student.objects.count()
        
        # ================== create queries and updates ==================
        # create
        # students = Student.objects.create(name='John', department='BBA')
        # get_or_create
        # students, created = Student.objects.get_or_create(name='John', department='BBA')
        # update
        # students = Student.objects.filter(pk=1).update(name='Jane')
        # update_or_create
        # students, created = Student.objects.update_or_create(pk=1, defaults={'name': 'Jane'})
        # bulk_create
        # students = Student.objects.bulk_create([
        #     Student(name='John', department='BBA'),
        #     Student(name='Jane', department='BBA')
        # ])
        # bulk_update
        # students = Student.objects.filter(department='BBA')
        # for student in students:
        #     student.name = 'Jane'
        # Student.objects.bulk_update(students, ['name'])
        # in_bulk
        # students = Student.objects.in_bulk([1, 2, 3])
        # print("Students:", students[1])
        # print("Students Name:", students['name'])
        # print("All students:", students)
        # print("In bulk:", students[1].name)
        
        # delete a specific student by department
        # students = Student.objects.filter(department='BBA').delete()
        # delete a specific student by pk
        # students = Student.objects.filter(pk=1).delete()
        # students = Student.objects.get(pk=2).delete()
        # students = get_object_or_404(Student, pk=3)
        # students.delete()
        # bulk_delete
        # students = Student.objects.bulk_delete([1, 2, 3])
        
        # ================== field lookups queries ==================
        # field lookups is a way to filter queryset based on field values and conditions specifically 
        # for that field where clause, methods like filter(), exclude(), get() etc.
        # syntax: field__lookup=value
        # __lt = less than
        # students = Student.objects.filter(roll__lt=10)
        # __gt = greater than
        # students = Student.objects.filter(roll__gt=5)
        # __lte = less than or equal
        # students = Student.objects.filter(roll__lte=10)
        # __gte = greater than or equal
        # students = Student.objects.filter(roll__gte=5)
        # exact case sentive
        # students = Student.objects.filter(department__exact='BBA')
        # students = Student.objects.filter(name__exact='John')
        # iexact case insensitive
        # students = Student.objects.filter(department__iexact='bba')
        # students = Student.objects.filter(name__iexact='john')
        # contains
        # students = Student.objects.filter(name__contains='John')
        # icontains
        # students = Student.objects.filter(name__icontains='john')
        # startswith
        # students = Student.objects.filter(name__startswith='J')
        # endswith
        # students = Student.objects.filter(name__endswith='n')
        # istartswith
        # students = Student.objects.filter(name__istartswith='j')
        # iendswith
        # students = Student.objects.filter(name__iendswith='n')
        # regex
        # students = Student.objects.filter(name__regex=r'^J')
        # iregex
        # students = Student.objects.filter(name__iregex=r'^j')
        # in_list = [1, 2, 3]
        # students = Student.objects.filter(id__in=[1, 2, 3])
        # students = Student.objects.filter(roll__range=(5, 10))
        
        # ============================= Aggregation queries =============================
        from django.db.models import Count, Avg, Max, Min, Sum
        students = Student.objects.aggregate(Count('id'))
        print("Students:", students)
        
    
        # print("Values:", students)
        # print("SQL:", students.query)

        context = {
            'teacher_form': teacher_form,
            'student_form': student_form,
            # 'teachers': teachers,
            'students': students
        }

        return render(request, 'home.html', context)

    def post(self, request):

        teacher_form = TeacherForm(request.POST)
        student_form = StudentForm(request.POST)

        if 'teacher_submit' in request.POST:
            if teacher_form.is_valpk():
                teacher_form.save()
                return redirect('StudentRegistrationPost')

        if 'student_submit' in request.POST:
            if student_form.is_valpk():
                student_form.save()
                return redirect('StudentRegistrationPost')

        # teachers = Teacher.objects.all()
        students = Student.objects.all()

        context = {
            'teacher_form': teacher_form,
            'student_form': student_form,
            # 'teachers': teachers,
            'students': students
        }

        return render(request, 'home.html', context)