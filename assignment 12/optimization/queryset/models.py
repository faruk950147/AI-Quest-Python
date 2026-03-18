from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "author"
        ordering = ["-created_at"]
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "post"
        ordering = ["-created_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"