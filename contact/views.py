from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages

# verification emails
from django.core.mail import send_mail
from weblog import settings

# Create your views here.


def contact(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['first_name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = Contact(first_name=first_name, last_name=last_name,
                          email=email, subject=subject, message=message)

        subject = [subject]
        message = [message]
        from_email = email
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=False)

        contact.save()

        messages.success(
            request, 'Your inquiry has been submitted. We will get back to you shortly')
        return redirect('contact')

    return render(request, 'pages/contact.html')

