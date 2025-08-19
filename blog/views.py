import json
import logging
import os

# Third-party imports
import requests
from dotenv import load_dotenv

# Django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.db.models import Q, Count
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

# Local imports
from .forms import PostForm
from .models import Bookmark, PostLike, Post, Category, Tag, NewsletterSubscription, Comment

logger = logging.getLogger(__name__)
load_dotenv()

# ------------------- Featured News ------------------- #
def get_featured_news():
    """Fetch top 5 technology news articles from NewsAPI."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        logger.error("Missing NEWS_API_KEY in environment variables")
        return []

    url = f"https://newsapi.org/v2/top-headlines?country=us&category=technology&pageSize=5&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return [
            {
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "image": article.get("urlToImage", ""),
                "source": article.get("source", {}).get("name", ""),
            }
            for article in articles
        ]
    except requests.RequestException as e:
        logger.error(f"Failed to fetch NewsAPI articles: {str(e)}")
        return []

# ------------------- Home Page ------------------- #
def home(request):
    """Render the homepage with featured news, latest posts, and categories."""
    try:
        context = {
            'featured_posts': get_featured_news(),
            'latest_posts': Post.objects.filter(status='published').select_related('author', 'category').order_by('-published_at')[:6],
            'categories': Category.objects.all()[:6],
        }
        return render(request, 'blog/home.html', context)
    except Exception as e:
        logger.error(f"Error in home view: {str(e)}", exc_info=True)
        context = {
            'featured_posts': [],
            'latest_posts': [],
            'categories': [],
            'error_message': 'Unable to load content at this time.'
        }
        return render(request, 'blog/home.html', context)

# ------------------- Post Detail ------------------- #
def post_detail(request, category_slug: str, slug: str):
    """Render a single post with related content and approved comments."""
    try:
        post = get_object_or_404(
            Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments'),
            category__slug=category_slug,
            slug=slug,
            status='published'
        )
        
        # Increment view count
        post.views = (post.views or 0) + 1
        post.save(update_fields=['views'])
        
        # JSON-LD structured data
        post_json_ld = {
            '@context': 'https://schema.org',
            '@type': 'BlogPosting',
            'headline': post.title,
            'description': post.excerpt or '',
            'author': {
                '@type': 'Person',
                'name': post.author.get_full_name() or post.author.username if post.author else 'Unknown'
            },
            'datePublished': post.created_at.isoformat(),
            'dateModified': post.updated_at.isoformat(),
            'url': request.build_absolute_uri(),
            'publisher': {
                '@type': 'Organization',
                'name': 'DigitalHub'
            }
        }
        
        if post.featured_image and hasattr(post.featured_image, 'url'):
            post_json_ld['image'] = request.build_absolute_uri(post.featured_image.url)
        
        # Related and popular posts
        related_posts = Post.objects.filter(
            category=post.category,
            status='published'
        ).exclude(id=post.id).select_related('author', 'category').order_by('-published_at')[:3]
        
        popular_posts = Post.objects.filter(
            status='published'
        ).select_related('author', 'category').order_by('-views', '-published_at')[:5]
        
        # Comments
        comments = post.comments.filter(is_approved=True).order_by('-created_at')
        comment_count = comments.count()
        
        context = {
            'post': post,
            'post_json': json.dumps(post_json_ld),
            'full_image_url': request.build_absolute_uri(post.featured_image.url) if post.featured_image and hasattr(post.featured_image, 'url') else '/static/images/default.png',
            'related_posts': related_posts,
            'popular_posts': popular_posts,
            'comments': comments,
            'comment_count': comment_count,
        }
        
        return render(request, 'blog/post_detail.html', context)
        
    except Post.DoesNotExist:
        logger.error(f"No Post matches category_slug={category_slug}, slug={slug}, status='published'")
        raise Http404("Post not found")
    except Exception as e:
        logger.error(f"Error in post_detail view for {category_slug}/{slug}: {str(e)}", exc_info=True)
        messages.error(request, 'Error loading the post.')
        return redirect('blog:home')

# ------------------- Post Comment ------------------- #
@require_http_methods(["POST"])
@login_required
def post_comment(request, slug: str):
    """Handle comment submission for a post."""
    try:
        post = get_object_or_404(Post, slug=slug, status='published')
        content = request.POST.get('content', '').strip()

        if not content:
            messages.error(request, 'Comment cannot be empty.')
            return redirect('blog:post_detail', category_slug=post.category.slug, slug=post.slug)

        Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            is_approved=True  # Set to False if moderation is needed
        )
        messages.success(request, 'Your comment has been posted.')
        return redirect('blog:post_detail', category_slug=post.category.slug, slug=post.slug)

    except Exception as e:
        logger.error(f"Error in post_comment view for {slug}: {str(e)}", exc_info=True)
        messages.error(request, 'Error posting comment. Please try again.')
        return redirect('blog:home')

# ------------------- Category Posts ------------------- #
class CategoryPostsView(ListView):
    """Display posts for a specific category with filtering and sorting."""
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        """Filter posts by category, search, tag, and sort order."""
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        queryset = Post.objects.filter(
            category=self.category, 
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')

        # Search functionality
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        # Tag filtering
        tag_slug = self.request.GET.get('tag', '').strip()
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        # Sorting - FIXED: Proper handling of sort parameters
        sort = self.request.GET.get('sort', 'latest').strip()
        
        # Define valid sort options
        sort_mapping = {
            'latest': '-published_at',
            'oldest': 'published_at', 
            'title': 'title',
            'popular': '-views'
        }
        
        # Get the sort field, default to latest
        sort_field = sort_mapping.get(sort, '-published_at')
        
        # Apply sorting
        if sort == 'popular':
            # For popular posts, also order by published_at as secondary
            queryset = queryset.order_by('-views', '-published_at')
        else:
            queryset = queryset.order_by(sort_field)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        """Add category-related context data."""
        context = super().get_context_data(**kwargs)
        
        # Get all posts in this category for statistics
        all_posts = Post.objects.filter(category=self.category, status='published')
        
        # Calculate total views safely
        total_views = 0
        try:
            for post in all_posts:
                if hasattr(post, 'views') and post.views:
                    total_views += post.views
        except (AttributeError, TypeError):
            total_views = 0
        
        context.update({
            'category': self.category,
            'related_categories': Category.objects.exclude(slug=self.category.slug).order_by('name')[:5],
            'popular_tags': Tag.objects.filter(posts__category=self.category).annotate(
                post_count=Count('posts')).order_by('-post_count')[:5],
            'total_articles': all_posts.count(),
            'featured_count': all_posts.filter(is_featured=True).count(),
            'total_views': total_views,
            'current_search': self.request.GET.get('search', ''),
            'current_tag': self.request.GET.get('tag', ''),
            'current_sort': self.request.GET.get('sort', 'latest'),
        })
        return context

# ------------------- Tag Posts ------------------- #
def tag_posts(request, slug: str):
    """Display posts associated with a specific tag."""
    try:
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(
            tags=tag, 
            status='published'
        ).select_related('author', 'category').order_by('-published_at')
        
        paginator = Paginator(posts, 6)
        page_obj = paginator.get_page(request.GET.get('page'))

        context = {
            'tag': tag,
            'posts': page_obj,
            'total_posts': posts.count(),
        }
        return render(request, 'blog/tag_posts.html', context)
    except Exception as e:
        logger.error(f"Error in tag_posts view for {slug}: {str(e)}", exc_info=True)
        messages.error(request, 'Error loading tag posts.')
        return redirect('blog:home')

# ------------------- Search ------------------- #
def search(request):
    """Handle search queries for posts."""
    query = request.GET.get('q', '').strip()
    posts = Post.objects.none()  # Start with empty queryset
    
    if query and len(query) >= 2:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(tags__name__icontains=query),
            status='published'
        ).select_related('author', 'category').distinct().order_by('-published_at')

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'posts': page_obj,
        'query': query,
        'total_results': posts.count() if query else 0,
    }
    return render(request, 'blog/search.html', context)

# ------------------- Popular Posts API ------------------- #
def popular_posts(request):
    """API endpoint for popular posts (missing in original views)."""
    try:
        posts = Post.objects.filter(
            status='published'
        ).select_related('author', 'category').order_by('-views', '-published_at')[:10]
        
        posts_data = []
        for post in posts:
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'slug': post.slug,
                'category_slug': post.category.slug,
                'excerpt': post.excerpt or '',
                'views': post.views or 0,
                'published_at': post.published_at.isoformat() if post.published_at else post.created_at.isoformat(),
                'author': post.author.get_full_name() or post.author.username if post.author else 'Unknown',
                'url': reverse('blog:post_detail', kwargs={
                    'category_slug': post.category.slug,
                    'slug': post.slug
                })
            })
        
        return JsonResponse({
            'success': True,
            'posts': posts_data,
            'count': len(posts_data)
        })
    except Exception as e:
        logger.error(f"Error in popular_posts API: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'Unable to fetch popular posts'
        }, status=500)

# ------------------- Newsletter ------------------- #
@csrf_exempt
@require_http_methods(["POST"])
def subscribe_newsletter(request):
    """Handle newsletter subscription."""
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        email = data.get('email', '').strip()
        category_slug = data.get('category', '').strip()

        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required.'}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'}, status=400)

        subscriber, created = NewsletterSubscription.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )

        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                subscriber.categories.add(category)
            except Category.DoesNotExist:
                logger.warning(f"Category {category_slug} not found for newsletter subscription")

        message = (
            'Successfully subscribed to our newsletter!' if created else
            'Welcome back! Your subscription has been reactivated.' if not subscriber.is_active else
            'This email is already subscribed to our newsletter.'
        )
        
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save()

        return JsonResponse({'success': True, 'message': message}, status=200)

    except json.JSONDecodeError:
        logger.error("Invalid JSON data in newsletter subscription request", exc_info=True)
        return JsonResponse({'success': False, 'message': 'Invalid data format.'}, status=400)
    except Exception as e:
        logger.error(f"Error in subscribe_newsletter view: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again later.'}, status=500)

# ------------------- Featured Insights ------------------- #
def featured_insights(request):
    """Render featured news articles."""
    try:
        return render(request, 'blog/featured_insights.html', {'articles': get_featured_news()})
    except Exception as e:
        logger.error(f"Error in featured_insights view: {str(e)}", exc_info=True)
        return render(request, 'blog/featured_insights.html', {
            'articles': [],
            'error_message': 'Unable to load insights at this time.'
        })

# ------------------- RSS Feed ------------------- #
class CategoryRSSFeed(Feed):
    """RSS feed for category posts."""
    def get_object(self, request, slug: str):
        return get_object_or_404(Category, slug=slug)

    def title(self, obj):
        return f"DigitalHub: {obj.name or 'Latest Posts'}"

    def link(self, obj):
        return reverse('blog:category_posts', args=[obj.slug])

    def description(self, obj):
        return obj.description or f"Latest posts in {obj.name or 'this category'}"

    def items(self, obj):
        return Post.objects.filter(
            category=obj, 
            status='published'
        ).select_related('author', 'category').order_by('-published_at')[:10]

    def item_title(self, item):
        return item.title or 'Untitled Post'

    def item_description(self, item):
        return item.excerpt or 'No description available'

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.published_at or item.created_at

# ------------------- Bookmark Post ------------------- #
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def bookmark_post(request, post_id: int):
    """Toggle bookmark status for a post."""
    try:
        post = get_object_or_404(Post, id=post_id)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            bookmark.delete()
            bookmarked = False
        else:
            bookmarked = True
            
        return JsonResponse({'success': True, 'bookmarked': bookmarked}, status=200)
    except Exception as e:
        logger.error(f"Error in bookmark_post view for post {post_id}: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'bookmarked': False, 'error': 'Bookmark action failed.'}, status=400)

# ------------------- Like Post ------------------- #
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def like_post(request, post_id: int):
    """Toggle like status for a post."""
    try:
        post = get_object_or_404(Post, id=post_id)
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
            
        likes_count = PostLike.objects.filter(post=post).count()
        return JsonResponse({'success': True, 'liked': liked, 'likes_count': likes_count}, status=200)
    except Exception as e:
        logger.error(f"Error in like_post view for post {post_id}: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'liked': False, 'likes_count': 0, 'error': 'Like action failed.'}, status=400)

# ------------------- Create Post ------------------- #
@login_required
def create_post(request):
    """Handle post creation."""
    try:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.status = 'published'
                post.published_at = post.published_at or timezone.now()
                post.save()
                form.save_m2m()
                
                logger.debug(f"Post created: {post.slug}, category: {post.category.slug}, status: {post.status}")
                messages.success(request, 'Post created successfully!')
                return redirect('blog:post_detail', category_slug=post.category.slug, slug=post.slug)
            else:
                logger.warning(f"Post creation failed due to invalid form: {form.errors}")
                messages.error(request, f"Error creating post: {form.errors.as_text()}")
        else:
            form = PostForm(initial={'status': 'published'})
            
        return render(request, 'blog/create_post.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in create_post view: {str(e)}", exc_info=True)
        messages.error(request, 'Error creating post. Please try again.')
        return render(request, 'blog/create_post.html', {'form': PostForm()})
    
def search(request):
    query = request.GET.get('q', '')
    return JsonResponse({"results": [], "query": query, "message": "Search endpoint under construction"})

def search(request):
    query = request.GET.get('q', '')
    return JsonResponse({"results": [], "query": query, "message": "Search endpoint under construction"})