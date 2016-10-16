from rest_framework import viewsets

from lab_reservations.models import TimeTable
from lab_reservations.serializers import TimeTableSerializer


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all().order_by('block_start')
    serializer_class = TimeTableSerializer
