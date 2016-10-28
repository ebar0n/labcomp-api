from rest_framework import viewsets, generics, views

from lab_reservations.models import TimeTable, Reservation
from lab_rooms.models import Room

from lab_reservations.serializers import TimeTableSerializer, RoomTimeTableSerializer, ReservationSerializer
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
            obj[0]: obj[1]
            for obj in CHOICES_BLOCKS
        }
        base['days'] = {
            obj[0]: obj[1]
            for obj in CHOICES_DAYS
        }
        base['rooms'] = {
            obj.pk: obj.name
            for obj in Room.objects.all()
        }
        return Response(base)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
