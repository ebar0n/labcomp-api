from rest_framework import generics, views, viewsets
from rest_framework.response import Response

from lab_reservations.models import CHOICES_BLOCKS, CHOICES_DAYS, Reservation, TimeTable
from lab_reservations.serializers import ReservationSerializer, RoomTimeTableSerializer, TimeTableSerializer
from lab_rooms.models import Room, RoomCharacteristic, TypeCharacteristic, TypeInfrastructure


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

        json = {}
        types = TypeInfrastructure.objects.all()
        for type in types:
            json[type.id] = {}
            json[type.id]['name'] = type.name
            json[type.id]['icon'] = type.icon
            json[type.id]['rooms'] = {}
            for room in Room.objects.filter(type=type.id):
                json[type.id]['rooms'][room.id] = {}
                json[type.id]['rooms'][room.id]['name'] = room.name
                json[type.id]['rooms'][room.id]['characteristics'] = []
                for typesc in TypeCharacteristic.objects.all():
                    json1 = {}
                    json1[typesc.name] = {}
                    json1[typesc.name]['icon'] = typesc.icon
                    characteristics = RoomCharacteristic.objects.filter(
                        characteristic__type=typesc.id,
                        room=room.id)
                    arrayObj = []
                    for characteristic in characteristics:
                        json2 = {}
                        json2[characteristic.characteristic.name] = {}
                        json2[characteristic.characteristic.name]['icon'] = characteristic.characteristic.icon
                        json2[characteristic.characteristic.name]['value'] = characteristic.value
                        arrayObj.append(json2)
                    json1[typesc.name]['characteristics'] = arrayObj
                    json[type.id]['rooms'][room.id]['characteristics'].append(json1)

        base['infrastructures'] = json
        return Response(base)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
