from rest_framework import serializers

from equipment.models import Equipment, EquipmentType
from equipment.services import validate_sn_mask


class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ("id", "name", "sn_mask")


class EquipmentSerializer(serializers.ModelSerializer):
    equipment_type = EquipmentTypeSerializer(read_only=True)
    equipment_type_id = serializers.PrimaryKeyRelatedField(
        queryset=EquipmentType.objects.all(),
        source="equipment_type",
        write_only=True,
    )
    sn = serializers.CharField(max_length=255)

    class Meta:
        model = Equipment
        fields = (
            "id",
            "equipment_type",
            "equipment_type_id",
            "sn",
            "note",
            "is_deleted",
        )
        read_only_fields = ("is_deleted",)

    # ----------- ВАЛИДАЦИЯ ------------

    def validate(self, attrs):
        """Комплексная валидация SN: маска и уникальность."""
        equipment_type = (
            attrs.get("equipment_type") or getattr(
                self.instance, "equipment_type", None)
        )
        sn = attrs.get("sn") or getattr(self.instance, "sn", None)

        if not equipment_type or not sn:
            return attrs

        if not validate_sn_mask(sn, equipment_type.sn_mask):
            raise serializers.ValidationError(
                {"sn": "SN не соответствует маске"}
            )

        qs = Equipment.objects.filter(
            sn=sn, equipment_type=equipment_type, is_deleted=False
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                {"sn": "Такой SN уже существует"}
            )

        return attrs
