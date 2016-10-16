from rest_framework import routers

from lab_reservations.api.timetable_api import TimeTableViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'timetables', TimeTableViewSet)