# blog/serializers.py
from rest_framework import serializers
from .models import Post, Category

class PostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'content', 'created_at', 'published_at', 'category', 'author', 'views']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']