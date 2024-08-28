from django.contrib import admin

from .models import Assessment, Class, Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "name",
        "credits",
        "program",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["code", "name"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = [
        "section",
        "course",
        "semester",
        "class_instructor",
        "max_students",
        "is_active",
    ]
    list_filter = ["is_active"]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "class_instance", "enrollment_date", "status"]
    list_filter = ["status"]


admin.site.register(Assessment)
