from django.contrib import admin

from lab_subjects.models import Color, Department, ReservationPermission, Semester, Subject


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(ReservationPermission)
class ReservationPermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    pass
