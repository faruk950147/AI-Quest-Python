from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from task.forms import StudentForm
from task.models import Student