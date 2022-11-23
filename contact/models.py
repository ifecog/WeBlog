from django.db import models
from datetime import datetime

# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=25, blank=True)
    message = models.TextField(blank=True)
    date_sent = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.email

class Newsletter(models.Model):
    email = models.EmailField(max_length=254)
    
    def __str__(self):
        return self.email