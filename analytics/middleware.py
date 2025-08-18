from django.urls import resolve

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Import models here so they load after app registry is ready
        from analytics.models import PageView
        from blog.models import Post

        self.PageView = PageView
        self.Post = Post

    def __call__(self, request):
        response = self.get_response(request)
        
        if not request.path.startswith(('/admin/', '/static/', '/media/', '/summernote/')):
            post = None
            if 'blog' in resolve(request.path).app_names:
                slug = resolve(request.path).kwargs.get('slug')
                if slug:
                    post = self.Post.objects.filter(slug=slug, status='published').first()
            
            self.PageView.objects.create(
                post=post,
                url=request.build_absolute_uri(),
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                referrer=request.META.get('HTTP_REFERER', '')
            )
        
        return response
