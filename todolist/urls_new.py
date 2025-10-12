"""
URL configuration for todolist project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

# Custom admin site with logout override
class CustomAdminSite(admin.AdminSite):
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
                        next_page='login',
                        template_name='registration/logged_out.html'
                    )
                ),
                name='logout',
            ),
        ]
        return custom_urls + urls

# Create custom admin instance
custom_admin = CustomAdminSite()

# Register default admin models
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

custom_admin.register(User, UserAdmin)
custom_admin.register(Group, GroupAdmin)

# Register your models with the custom admin site
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

custom_admin.register(Category, CategoryAdmin)
custom_admin.register(Todo, TodoAdmin)

# Authentication URL patterns
auth_patterns = [
    path('login/', 
         auth_views.LoginView.as_view(
             template_name='registration/secure_login.html',
             redirect_authenticated_user=True
         ), 
         name='login'),
    path('logout/', 
         auth_views.LogoutView.as_view(
             next_page='login',
             template_name='registration/logged_out.html'
         ), 
         name='logout'),
]

# Main URL patterns
urlpatterns = [
    # Main app
    path('', include('todos.urls')),
    
    # Secure admin
    path('admin/', custom_admin.urls),
    
    # Authentication
    path('accounts/', include((auth_patterns, 'auth'))),
    
    # Redirect root /admin/ to our secure admin
    path('admin', RedirectView.as_view(url='/admin/', permanent=True)),
]

# Add error handlers
handler400 = 'todos.views.handler400'
handler403 = 'todos.views.handler403'
handler404 = 'todos.views.handler404'
handler500 = 'todos.views.handler500'
