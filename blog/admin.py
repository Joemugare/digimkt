# blog/admin.py - Quick fix version

from django.contrib import admin
from .models import Category, Post, Tag, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'is_featured', 'created_at']  # changed 'created' to 'created_at'
    list_filter = ['status', 'category', 'is_featured', 'created_at']  # changed 'created' to 'created_at'
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'is_approved']  # changed 'name' to 'post', 'created' to 'created_at', 'active' to 'is_approved'
    list_filter = ['is_approved', 'created_at']  # changed 'active' to 'is_approved', 'created' to 'created_at'
    search_fields = ['content', 'author__username']