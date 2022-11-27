from django.contrib import admin
from . models import Post, Category, Comment
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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
