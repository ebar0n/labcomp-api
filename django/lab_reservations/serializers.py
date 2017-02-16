from rest_framework import serializers

from lab_rooms.models import RoomCharacteristic, TypeCharacteristic

from .models import Reservation, Section, TimeTable


class TimeTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeTable
        fields = '__all__'

    def validate(self, data):
        block_start = data['block_start']
        block_end = data['block_end']
        if block_start != block_end:
            if block_start < block_end:
                if TimeTable.get_block_valid(
                        block_start, block_end, data['day'], data['room']) is False:
                    raise serializers.ValidationError(
                        {'block_end': 'Colisión de horas'})
            else:
                raise serializers.ValidationError(
                    {'block_end': 'El bloque de hora final no debe ser menor al bloque de hora inicial'})
        else:
            raise serializers.ValidationError(
                {'block_end': 'El bloque de hora final debe ser diferente al inicial'})
        return data


class SectionSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    subject_code = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ('code', 'subject', 'subject_code', 'color')

    def get_subject(self, obj):
        return obj.subject.name

    def get_subject_code(self, obj):
        return obj.subject.code

    def get_color(self, obj):
        return obj.subject.color.code


class BlocksTimeTableSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField()
    section = SectionSerializer()

    class Meta:
        model = TimeTable
        fields = ('section', 'day', 'blocks')

    def get_blocks(self, obj):
        return [x for x in range(obj.block_start, obj.block_end)]


class RoomTimeTableSerializer(serializers.Serializer):
    rows = serializers.SerializerMethodField()
    characteristics = serializers.SerializerMethodField()

    def get_rows(self, obj):
        timetables = TimeTable.objects.filter(room=obj)
        return [BlocksTimeTableSerializer(x).data for x in timetables]

    def get_characteristics(self, obj):
        json = {}
        types = TypeCharacteristic.objects.all()
        for type in types:
            json[type.name] = {}
            json[type.name]['icon'] = type.icon
            arrayObj = []
            characteristics = RoomCharacteristic.objects.filter(room=obj)
            for characteristic in characteristics:
                json1 = {}
                json1[characteristic.characteristic.name] = {}
                json1[characteristic.characteristic.name]['icon'] = characteristic.characteristic.icon
                json1[characteristic.characteristic.name]['value'] = characteristic.value
                arrayObj.append(json1)
            json[type.name]['characteristics'] = arrayObj
        return json


class ReservationSerializer(serializers.ModelSerializer):
    timetable = TimeTableSerializer()

    class Meta:
        model = Reservation
        fields = '__all__'
