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
