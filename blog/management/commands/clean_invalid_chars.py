# blog/management/commands/clean_invalid_chars.py
from django.core.management.base import BaseCommand
from django.utils.encoding import smart_str
from blog.models import Post, Category, Tag
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cleans invalid UTF-8 characters from database'

    def handle(self, *args, **kwargs):
        for post in Post.objects.all():
            try:
                post.title = smart_str(post.title or '', encoding='utf-8', errors='replace')
                post.excerpt = smart_str(post.excerpt or '', encoding='utf-8', errors='replace')
                post.content = smart_str(post.content or '', encoding='utf-8', errors='replace')
                post.slug = smart_str(post.slug or '', encoding='utf-8', errors='replace')
                post.meta_description = smart_str(post.meta_description or '', encoding='utf-8', errors='replace')
                post.meta_keywords = smart_str(post.meta_keywords or '', encoding='utf-8', errors='replace')
                post.save()
                self.stdout.write(self.style.SUCCESS(f'Cleaned Post {post.id}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error cleaning Post {post.id}: {e}'))
                post.delete()
        for category in Category.objects.all():
            try:
                category.name = smart_str(category.name or '', encoding='utf-8', errors='replace')
                category.description = smart_str(category.description or '', encoding='utf-8', errors='replace')
                category.slug = smart_str(category.slug or '', encoding='utf-8', errors='replace')
                category.save()
                self.stdout.write(self.style.SUCCESS(f'Cleaned Category {category.id}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error cleaning Category {category.id}: {e}'))
        for tag in Tag.objects.all():
            try:
                tag.name = smart_str(tag.name or '', encoding='utf-8', errors='replace')
                tag.slug = smart_str(tag.slug or '', encoding='utf-8', errors='replace')
                tag.save()
                self.stdout.write(self.style.SUCCESS(f'Cleaned Tag {tag.id}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error cleaning Tag {tag.id}: {e}'))
        for user in User.objects.all():
            try:
                user.first_name = smart_str(user.first_name or '', encoding='utf-8', errors='replace')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Cleaned User {user.id}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error cleaning User {user.id}: {e}'))