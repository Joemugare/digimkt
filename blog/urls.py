# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<slug:category_slug>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/comment/', views.post_comment, name='post_comment'),
    path('category/<slug:slug>/', views.CategoryPostsView.as_view(), name='category_posts'),
    path('category/<slug:slug>/rss/', views.CategoryRSSFeed(), name='category_rss'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('api/search/', views.search, name='search'),
    path('api/popular-posts/', views.popular_posts, name='popular_posts'),
    path('newsletter/subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('featured-insights/', views.featured_insights, name='featured_insights'),
    path('api/posts/<int:post_id>/bookmark/', views.bookmark_post, name='bookmark_post'),
    path('api/posts/<int:post_id>/like/', views.like_post, name='like_post'),
]