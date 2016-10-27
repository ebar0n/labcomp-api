from rest_framework import serializers

from .models import TimeTable


class TimeTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeTable

    def validate(self, data):
        block_start = data['block_start']
        block_end = data['block_end']
        if block_start != block_end:
            if block_start < block_end:
                if TimeTable.get_block_valid(
                    block_start,
                    block_end,
                    data['day'],
                    data['room']) is False:
                    raise serializers.ValidationError(
                        {'block_end': 'Colisión de horas'})
            else:
                raise serializers.ValidationError(
                    {'block_end': 'El bloque de hora final no debe ser menor al bloque de hora inicial'})
        else:
            raise serializers.ValidationError(
                {'block_end': 'El bloque de hora final debe ser diferente al inicial'})
        return data


class BlocksTimeTableSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = TimeTable
        fields = ('section', 'day', 'blocks')
    
    def get_blocks(self, obj):
        return [x for x in range(obj.block_start, obj.block_end)]


class RoomTimeTableSerializer(serializers.Serializer):
    rows = serializers.SerializerMethodField()
    
    def get_rows(self, obj):
        timetables = TimeTable.objects.filter(room=obj)
        return [BlocksTimeTableSerializer(x).data for x in timetables]