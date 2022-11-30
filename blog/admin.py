from django.contrib import admin
from . models import Post, Category, Comment, Team, About, View
from django.utils.html import format_html

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.image.url))

    thumbnail.short_description = 'photo'

    list_display = ('id', 'thumbnail', 'name')
    list_display_links = ('name', 'thumbnail')
    search_fields = ['name']


class PostAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        try:
            return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.photo.url))
        except:
            pass

    thumbnail.short_description = 'photo'

    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'thumbnail', 'category',
                    'title', 'writer', 'trending')
    list_display_links = ('id', 'title', 'thumbnail')
    search_fields = ('title', 'writer', 'body')
    list_editable = ('trending',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'comment']
    list_display_links = ['post', 'comment']
    search_fields = ['post', 'comment']


class TeamAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.photo.url))

    thumbnail.short_description = 'photo'

    list_display = ('id', 'thumbnail', 'first_name', 'role', 'upload_time')
    list_display_links = ('id', 'first_name', 'thumbnail')
    search_fields = ('first_name', 'last_name', 'role')
    list_filter = ['role']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(About)
admin.site.register(View)
