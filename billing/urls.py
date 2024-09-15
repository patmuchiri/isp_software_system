from django.urls import path
from . import views
from .views import landing, login_view, register_user, register_client, admin_dashboard, view_clients

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', register_user, name='register_user'),
    path('register_client/', register_client, name='register_client'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('view_clients/', view_clients, name='view_clients'),
]
