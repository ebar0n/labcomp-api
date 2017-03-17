from django.contrib import admin

from .models import Section, Reservation


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'user')

