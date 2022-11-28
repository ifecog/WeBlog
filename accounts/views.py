from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# verification emails
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from weblog import settings

# Create your views here.


def signup(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username already taken')
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email already used')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(
                        first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                    auth.login(request, user)
                    messages.success(request, 'Signup Successful!')
                    user.save()

                    # user activation
                    current_site = get_current_site(request)
                    email_subject = 'Please activate your account',
                    message = render_to_string('accounts/account_verification_email.html', {
                        'user': user,
                        'domain': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user)
                    })
                    from_email = settings.EMAIL_HOST_USER
                    recipient = [email]
                    send_email = EmailMessage(
                        email_subject, message, from_email, recipient)
                    send_email.send(fail_silently=False)

                    return redirect('/accounts/login/?command=verification&email='+email)

        else:
            messages.error(request, 'passwords do not match')
            return redirect('signup')

    return render(request, 'accounts/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')

        else:
            messages.error(
                request, 'Incorrect email or password, try again!')
            return redirect('signin')

    return render(request, 'accounts/signin.html')


@login_required(login_url='signin')
def signout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are successfully logged out')
        return redirect('home')

    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Conratulations! Your account has been activated')
        return redirect('signin')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('signup')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # forgot password reset
            current_site = get_current_site(request)
            email_subject = 'Reset your Password',
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            from_email = settings.EMAIL_HOST_USER
            recipient = [email]
            send_email = EmailMessage(
                email_subject, message, from_email, recipient)
            send_email.send(fail_silently=False)

            messages.success(
                request, "Password reset email has been sent to your email")
            return redirect('signin')

        else:
            messages.error(
                request, "There is no user with this email. Please, correct email")
            return redirect('forgotpassword')

    return render(request, 'accounts/forgotpassword.html')


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(
            request, 'Please reset your password')
        return redirect('password_reset')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('forgotpassword')

def password_reset(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password Reset Successful!")
            return redirect('signin')
        else:
            messages.error(request, "Passwords do not match. Try again")
            return redirect('password_reset')

    return render(request, 'accounts/password_reset.html')