from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_views, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_views, name='logout'),
    path('create_post/', views.create_post, name='create_post'),
    path('post_detail/<int:post_id>', views.post_detail, name='post_detail'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
]