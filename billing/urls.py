from django.urls import path
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
]
