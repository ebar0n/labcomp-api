from django.contrib import admin

from .models import Section


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass
