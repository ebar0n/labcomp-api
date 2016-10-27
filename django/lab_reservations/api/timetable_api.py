from rest_framework import viewsets, generics, views

from lab_reservations.models import TimeTable
from lab_rooms.models import Room

from lab_reservations.serializers import TimeTableSerializer, RoomTimeTableSerializer
from lab_reservations.models import CHOICES_BLOCKS, CHOICES_DAYS
from rest_framework.response import Response


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all().order_by('block_start')
    serializer_class = TimeTableSerializer


class RoomTimeTableView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomTimeTableSerializer


class BaseTimeTableView(views.APIView):

    def get(self, request, format=None):
        base = {}
        base['blocks'] = {
            array[0]: array[1]
            for array in CHOICES_BLOCKS
        }
        base['days'] = {
            array[0]: array[1]
            for array in CHOICES_DAYS
        }
        return Response(base)
