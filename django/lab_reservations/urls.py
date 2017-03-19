from django.conf.urls import include, url
from lab_reservations.api.timetable_api import (
    BaseTimeTableView, ReservationViewSet, RoomTimeTableView, TimeTableViewSet,
)
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'timetables', TimeTableViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    url(r'^timetable/base/$', BaseTimeTableView.as_view()),
    url(r'^timetable/room/(?P<pk>\d+?)$', RoomTimeTableView.as_view()),
    url(r'^timetable/', include(router.urls, namespace='api')),
]
