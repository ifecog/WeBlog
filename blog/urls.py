from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:category_slug>', views.home, name='posts_by_category'),
    path('allblogs/', views.all_posts, name='all_posts'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
]
