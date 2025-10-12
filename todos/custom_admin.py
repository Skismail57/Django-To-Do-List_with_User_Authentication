from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class CustomAdminSite(AdminSite):
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        # Override the admin logout URL
        custom_urls = [
            path(
                'logout/',
                self.admin_view(
                    LogoutView.as_view(
                        next_page=reverse_lazy('login')
                    )
                ),
                name='logout',
            ),
        ]
        return custom_urls + urls

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite()

# Register your models with the custom admin site
from .models import Todo, Category

@admin.register(Category, site=custom_admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Todo, site=custom_admin_site)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "completed", "due_date", "created_at", "owner")
    list_filter = ("completed", "category", "due_date", "created_at")
    search_fields = ("title", "description")
    autocomplete_fields = ("category", "owner")
