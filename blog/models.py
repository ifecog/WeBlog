from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=45, unique=True)
    description = RichTextField()
    image = models.ImageField(
        upload_to='category_photos/%y/%m/%d/', blank=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('posts_by_category', args=[self.slug])


class Post(models.Model):
    writer = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, unique=True)
    photo = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    body = RichTextField()
    trending = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True)
    upload_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('post_detail', args=[self.category.slug, self.slug])
    
class View(models.Model):
    viewer = models.TextField(default=None)
    
    def __str__(self):
        return self.viewer


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = RichTextField()
    upload_time = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        ordering = ['-upload_time']

    def __str__(self):
        return self.comment
    

class Team(models.Model):
    first_name = models.CharField(max_length=45, unique=True)
    last_name = models.CharField(max_length=45, unique=True)
    role = models.CharField(max_length=45, unique=True)
    photo = models.ImageField(upload_to='team_photos/%y/%m/%d/', blank=True)
    facebook_link = models.URLField(max_length=100)
    twitter_link = models.URLField(max_length=100)
    google_link = models.URLField(max_length=100)
    upload_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.first_name

class About(models.Model):
    body = RichTextField()
    