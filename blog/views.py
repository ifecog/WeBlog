from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment, Team, About, View
from .forms import CommentForm
from django.core.paginator import Paginator
from django.db.models import Q
from contact.models import Newsletter
from django.core.mail import send_mail
from weblog import settings
from django.contrib import messages
from django.urls import reverse


# Create your views here.


def home(request, category_slug=None):
    categories = None
    posts = None

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.all().filter(category=categories).order_by('-upload_time')
        trends = Post.objects.filter(
            trending=True).order_by(-'upload_time')[:3]
        recents = Post.objects.all().order_by('-upload_time')[:4]
        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    else:
        posts = Post.objects.all().order_by('-upload_time')
        trends = Post.objects.all().filter(trending=True)[:3]
        recents = Post.objects.all().order_by('-upload_time')[:4]
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
    teams = Team.objects.all().order_by('upload_time')
    detail = About.objects.all()

    context = {
        'teams': teams,
        'detail': detail,
    }

    return render(request, 'pages/about.html', context)


def post_detail(request, category_slug, product_slug):
    single_post = get_object_or_404(
        Post, category__slug=category_slug, slug=product_slug)

    comments = single_post.comment_set.all()
    comments_count = Comment.objects.all().filter(post=single_post).count()
    form = CommentForm()
    new_comment = None
 
    if request.method == 'POST':
        form = CommentForm(request.POST)
        new_comment = form.save(commit=False)
        new_comment.post = single_post
        new_comment.save()

        return redirect(reverse('post_detail', kwargs={'category_slug': category_slug, 'product_slug': product_slug}))

    recents = Post.objects.all().order_by('upload_time')[:6]

    def get_ip(request):
        address = request.META.get('HTTP_X_FORWARDED_FOR')
        if address:
            ip = address.split[','][-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    ip = get_ip(request)
    user = View(viewer=ip)
    result = View.objects.filter(Q(viewer__icontains=ip))
    if len(result) >= 1:
        pass
    else:
        user.save()
    view_count = View.objects.all().count()

    context = {
        'single_post': single_post,
        'recents': recents,
        'comments': comments,
        'form': form,
        'count': comments_count,
        'view_count': view_count,
    }

    return render(request, 'pages/post_detail.html', context)


def newsletter(request):
    if request.method == 'POST':
        email = request.POST['email']

        newsletter = Newsletter(email=email)

        #  Email
        subject = 'Newsletter Subscription'
        message = 'Hi reader! Thank you for subscribing for WeBlog\'s weekly newsletter collection'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=False)

        newsletter.save()
        messages.success(
            request, 'Thank you for subscribing for \WeBlog\'s weekly newsletter collection. Check your email inbox for more info')
        redirect('home')

    return render(request, 'pages/home.html')
