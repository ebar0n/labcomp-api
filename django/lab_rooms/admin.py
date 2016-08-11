from django.contrib import admin
from lab_rooms.models import TypeCharacteristic, Characteristic, TypeInfrastructure, Room, RoomCharacteristic


@admin.register(TypeCharacteristic)
class TypeCharacteristicAdmin(admin.ModelAdmin):
    pass

@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    pass

@admin.register(TypeInfrastructure)
class TypeInfrastructureAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(RoomCharacteristic)
class RoomCharacteristicAdmin(admin.ModelAdmin):
    pass
