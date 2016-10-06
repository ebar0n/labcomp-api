from django.contrib import admin
from django.utils.html import format_html

from lab_subjects.models import Color, Department, ReservationPermission, Semester, Subject


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(ReservationPermission)
class ReservationPermissionAdmin(admin.ModelAdmin):
    list_display = ('department', 'block_limit', 'weekly_limit', 'biweekly_limit', 'monthly_limit')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_color')

    def get_color(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            obj.code,
            obj.code
        )
    get_color.short_description = 'Color'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department')


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('code', 'start_date', 'end_date', 'present')
