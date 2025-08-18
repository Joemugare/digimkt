from django.urls import path
from . import views

app_name = 'affiliate'

urlpatterns = [
    path('go/<int:link_id>/', views.redirect_affiliate_link, name='redirect'),
    path('links/', views.affiliate_link_list, name='link_list'),
]