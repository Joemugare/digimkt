from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Category, Post

class CategoryFeed(Feed):
    def get_object(self, request, slug):
        return Category.objects.get(slug=slug)

    def title(self, obj):
        return f"Posts in {obj.name}"

    def link(self, obj):
        return f"/category/{obj.slug}/"

    def description(self, obj):
        return f"Latest posts in {obj.name}"

    def items(self, obj):
        # Fetch the latest 10 published posts
        return Post.objects.filter(category=obj, status='published').order_by("-created_at")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt

    def item_link(self, item):
        # Absolute URL to the post
        return reverse('blog:post_detail', kwargs={
            'category_slug': item.category.slug,
            'slug': item.slug
        })

    def item_pubdate(self, item):
        return item.published_at
