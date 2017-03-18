from django.contrib import admin
from django.utils.translation import ugettext as _
from django.conf.urls import url
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from datetime import datetime

from .models import Section, Reservation, StatusReservationHistoric, CHOICES_STATUS_RESERVATIONS


class StatusFilter(SimpleListFilter):
    title = _('status')
    parameter_name = _('status')

    def lookups(self, request, model_admin):
        return CHOICES_STATUS_RESERVATIONS

    def queryset(self, request, queryset):
        reservations = StatusReservationHistoric.objects.filter(
            status=self.value(),
            end_date=None).values_list('reservation', flat=True)

        if self.value():
            return queryset.filter(id__in=list(reservations))
        else:
            return queryset


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display_links = None
    list_display = (
        'date', 'user', 'get_room', 'get_section', 'get_day',
        'get_block_start', 'get_block_end', 'type', 'action')
    list_filter = (StatusFilter,)

    def get_room(self, obj):
        return obj.timetable.room

    def get_section(self, obj):
        return obj.timetable.section

    def get_day(self, obj):
        return obj.timetable.get_day()

    def get_block_start(self, obj):
        return obj.timetable.get_block_start()

    def get_block_end(self, obj):
        return obj.timetable.get_block_end()

    def action(self, obj):
        if obj.get_status()[0] == 2:
            return format_html(
                '<a class="button" href="{}">Aceptar</a>&nbsp;'
                '<a class="button" style="background: #ba2121;" href="{}">Rechazar</a>',
                reverse('admin:change-status-approved', args=[obj.pk]),
                reverse('admin:change-status-rejected', args=[obj.pk])
            )
        return obj.get_status()[1]

    get_room.short_description = _('room')
    get_section.short_description = _('section')
    get_day.short_description = _('day')
    get_block_start.short_description = _('block start')
    get_block_end.short_description = _('block end')
    action.short_description = _('action')

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<reservation_id>.+)/approved/$',
                self.admin_site.admin_view(self.change_status_approved),
                name='change-status-approved',
            ),
            url(
                r'^(?P<reservation_id>.+)/rejected/$',
                self.admin_site.admin_view(self.change_status_rejected),
                name='change-status-rejected',
            ),
        ]
        return custom_urls + urls

    def change_status_approved(self, request, reservation_id, *args, **kwargs):
        reservation = StatusReservationHistoric.objects.get(reservation=reservation_id, end_date=None)
        reservation.end_date = datetime.now()
        reservation.save(update_fields=['end_date'])

        StatusReservationHistoric.objects.create(
            reservation=reservation.reservation,
            start_date=datetime.now(),
            status=1
        )
        return super(ReservationAdmin, self).changelist_view(request)

    def change_status_rejected(self, request, reservation_id, *args, **kwargs):
        reservation = StatusReservationHistoric.objects.get(reservation=reservation_id, end_date=None)
        reservation.end_date = datetime.now()
        reservation.save(update_fields=['end_date'])

        StatusReservationHistoric.objects.create(
            reservation=reservation.reservation,
            start_date=datetime.now(),
            status=3
        )
        return super(ReservationAdmin, self).changelist_view(request)
