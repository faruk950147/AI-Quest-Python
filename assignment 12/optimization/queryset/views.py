from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from queryset.models import Author, Post
from django.db.models import Count, Avg, Max, Min, Sum, Q, F
from django.db import connection


class PostListView(View):
    '''Without Optimization select_related'''
    def get(self, request):
        posts = Post.objects.all()
        for post in posts:
            print(post.author.name)
        for query in connection.queries:
            print(query['sql'])
        print(f"Total Number of queries: {len(connection.queries)}")
        return HttpResponse("Hello World")

class PostListViewOptimazed(View):
    '''With Optimization select_related'''
    def get(self, request):
        posts = Post.objects.select_related('author')
        for post in posts:
            print(post.author.name)
        for query in connection.queries:
            print(query['sql'])
        print(f"Total Number of queries: {len(connection.queries)}")
        return HttpResponse("Hello World")

