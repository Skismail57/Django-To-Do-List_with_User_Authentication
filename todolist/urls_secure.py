"""
Secure URL configuration for todolist project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# Custom admin site with enhanced security
class SecureAdminSite(admin.AdminSite):
    site_header = 'TaskMaster Pro Admin'
    site_title = 'TaskMaster Pro Administration'
    index_title = 'Welcome to TaskMaster Pro Admin'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                'logout/',
                self.admin_view(
                    auth_views.LogoutView.as_view(
                        next_page='secure_login',
                        template_name='registration/logged_out.html'
                    )
                ),
                name='logout',
            ),
        ]
        return custom_urls + urls

# Create secure admin instance
secure_admin = SecureAdminSite()

# Register default admin models with secure admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

secure_admin.register(User, UserAdmin)
secure_admin.register(Group, GroupAdmin)

# Register your models with the secure admin site
from todos.models import Todo, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 20

class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "completed", "due_date", "created_at", "owner")
    list_filter = ("completed", "category", "due_date", "created_at")
    search_fields = ("title", "description")
    autocomplete_fields = ("category", "owner")
    list_per_page = 20
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

secure_admin.register(Category, CategoryAdmin)
secure_admin.register(Todo, TodoAdmin)

# Authentication URL patterns
auth_patterns = [
    path('login/', 
         auth_views.LoginView.as_view(
             template_name='registration/secure_login.html',
             redirect_authenticated_user=True
         ), 
         name='secure_login'),
    path('logout/', 
         auth_views.LogoutView.as_view(
             next_page='secure_login',
             template_name='registration/logged_out.html'
         ), 
         name='secure_logout'),
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change.html',
             success_url='password_change_done/'
         ), 
         name='password_change'),
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'
         ), 
         name='password_change_done'),
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             success_url='done/'
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url='/accounts/reset/done/'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]

# Main URL patterns
urlpatterns = [
    # Main app
    path('', include('todos.urls')),
    
    # Secure admin
    path('admin/', secure_admin.urls),
    
    # Authentication
    path('accounts/', include((auth_patterns, 'auth'))),
    
    # Redirect root /admin/ to our secure admin
    path('admin', RedirectView.as_view(url='/admin/', permanent=True)),
    
    # API endpoints (if any)
    # path('api/', include('api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler400 = 'todos.views.handler400'
handler403 = 'todos.views.handler403'
handler404 = 'todos.views.handler404'
handler500 = 'todos.views.handler500'
