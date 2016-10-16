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
