from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.views.generic import TemplateView
from django.views.static import serve

# Sitemaps dictionary
sitemaps = {
    'posts': PostSitemap,
}

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),  # Ensure app_name = 'blog' in blog/urls.py
    path('affiliate/', include('affiliate.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('favicon.ico', serve, {'document_root': settings.STATIC_ROOT, 'path': 'images/favicon.ico'}),
    path('accounts/', include('django.contrib.auth.urls'))

]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
