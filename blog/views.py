from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.


def home(request, category_slug=None):
    categories = None
    posts = None

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.all().filter(category=categories).order_by('upload_time')
        trends = Post.objects.all().filter(trending=True)
        recents = Post.objects.all().order_by('upload_time')[:4]
        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    else:
        posts = Post.objects.all().order_by('upload_time')
        trends = Post.objects.all().filter(trending=True)
        recents = Post.objects.all().order_by('upload_time')[:4]
        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'trends': trends,
        'recents': recents,
    }

    return render(request, 'pages/home.html', context)


def all_posts(request):
    posts = Post.objects.all().order_by('upload_time')
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
    }

    return render(request, 'pages/all_posts.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            posts = Post.objects.order_by(
                '-upload_time').filter(Q(body__icontains=keyword) | Q(title__icontains=keyword))
            # posts_count = posts.count()

    context = {
        'posts': posts,
        # 'posts_count': posts_count,
    }

    return render(request, 'pages/home.html', context)


def about(request):

    return render(request, 'pages/about.html')


def post_detail(request, category_slug, product_slug):
    try:
        single_post = Post.objects.get(
            category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    context = {
        'single_post': single_post,
    }

    return render(request, 'pages/post_detail.html', context)
