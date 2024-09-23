from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import landing, login_view, register_user, register_client, admin_dashboard, view_clients, edit_client, delete_client
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', register_user, name='register_user'),
    path('register_client/', register_client, name='register_client'),
    path('edit_client/<int:client_id>/', views.edit_client, name='edit_client'),
    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user_home/', views.user_home, name='user_home'),
    path('view_clients/', view_clients, name='view_clients'),
    path('view_users/', views.view_users, name='view_users'),
    path('logout/', LogoutView.as_view(next_page='landing'), name='logout'),

    # Password reset URLs using Django's built-in views
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
