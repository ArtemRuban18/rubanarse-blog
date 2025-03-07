from django.contrib import admin
from .models import Category, Post, Comment
# Register your models here.
admin.site.register(Category)
admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'views', 'created_at', 'status')
    search_fields = ('author', 'title')
    ordering = ['status']

admin.site.register(Post, PostAdmin)