from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:category_slug>', views.home, name='posts_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/',
         views.post_detail, name='post_detail'),
    path('allblogs/', views.all_posts, name='all_posts'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('about/', views.about, name='about'),
]
