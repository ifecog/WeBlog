from django.contrib import admin
from .models import Contact, Newsletter

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'date_sent')
    list_display_links = ('id', 'first_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    list_per_page = 25


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ['email']
    list_per_page = 25


admin.site.register(Contact, ContactAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
