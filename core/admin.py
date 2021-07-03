from django.contrib import admin

from .models import Department, Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "department", "birthdate")
    list_display_links = ("id", "first_name")
    search_fields = ("first_name",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_display_links = ("title",)
    search_fields = ("title",)
