from django.contrib import admin
from .models import Todo, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "completed", "due_date", "created_at", "owner")
    list_filter = ("completed", "category", "due_date", "created_at")
    search_fields = ("title", "description")
    autocomplete_fields = ("category", "owner")


