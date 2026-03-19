from django.shortcuts import render
from django.views import View
from queryset.models import Author, Post
from django.db.models import Count, Avg, Max, Min, Sum, Q, F


class PostListView(View):
    def get(self, request):
        context = {}
        return render(request, "home/home.html", context)

    def post(self, request):

        context = {}
        return render(request, 'home/home.html', context)