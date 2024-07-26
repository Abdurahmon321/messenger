from django.urls import path
from .views import register, user_login, user_logout, index, verify_email, profile_view, chat_view, start_chat, \
    search_users, profile_edit

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('verify-email/', verify_email, name='verify_email'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/<str:username>/', profile_view, name='profile_view'),
    path('chat/<slug:slug>/', chat_view, name='chat_view'),
    path('start_chat/<int:user_id>/', start_chat, name='start_chat'),
    path('search/', search_users, name='search_users'),
    path('profile/edit/<str:username>', profile_edit, name='profile_edit'),
]
