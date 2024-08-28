from django.contrib import admin

from .models import AcademicYear, Department, Program, Semester


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(AcademicYear)
admin.site.register(Semester)
