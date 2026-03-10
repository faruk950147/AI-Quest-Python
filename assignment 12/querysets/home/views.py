from django.shortcuts import render, redirect
from django.views import View
from home.forms import TeacherForm, StudentForm
from home.models import Student, Teacher


class StudentRegistrationPost(View):

    def get(self, request):
        teacher_form = TeacherForm()
        student_form = StudentForm()
        # Get all students from default database
        # students = Student.objects.all() # return all students objects
        # ================== lookup for filter methods ==================
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
        # order by id
        # students = Student.objects.order_by('id').reverse()[:5]
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
        
        # get by id
        # students = Student.objects.get(id=1)
        # get by name
        # students = Student.objects.get(name='John')
        # get by department
        # students = Student.objects.get(department='BBA')
        # first by
        # students = Student.objects.first()
        # students = Student.objects.order_by('id').first()
        # last
        # students = Student.objects.order_by('-id').first()
        # last by
        # students = Student.objects.last()
        # lastest
        students = Student.objects.latest('created_at')
        
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
            if teacher_form.is_valid():
                teacher_form.save()
                return redirect('StudentRegistrationPost')

        if 'student_submit' in request.POST:
            if student_form.is_valid():
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