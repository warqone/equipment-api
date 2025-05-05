from rest_framework import serializers

from equipment.models import Equipment, EquipmentType


class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ('id', 'name', 'sn_mask')


class EquipmentSerializer(serializers.ModelSerializer):
    equipment_type = EquipmentTypeSerializer(read_only=True)
    equipment_type_id = serializers.PrimaryKeyRelatedField(
        queryset=EquipmentType.objects.all(),
        source='equipment_type',
        write_only=True
    )

    class Meta:
        model = Equipment
        fields = (
            'id', 'equipment_type', 'equipment_type_id',
            'sn', 'note', 'is_deleted')
