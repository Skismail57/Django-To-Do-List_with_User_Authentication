"""
URL configuration for todolist project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('todos.urls')),
    path('admin/', admin.site.urls),
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login_updated.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # Add a GET method handler for logout for better compatibility
    path('accounts/logout/get/', auth_views.LogoutView.as_view(next_page='/'), name='logout_get'),
]

# Add this to handle 404 errors
handler404 = 'todos.views.handler404'
