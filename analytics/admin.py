# analytics/admin.py
from django.contrib import admin
from .models import PageView, NewsletterSubscriber

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('url', 'ip_address', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('url', 'ip_address')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'subscribed_date', 'is_active')
    list_filter = ('is_active', 'subscribed_date')
    search_fields = ('email', 'name')