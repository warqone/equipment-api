import re

from django.contrib import admin
from django.core.exceptions import ValidationError

from equipment.models import Equipment, EquipmentType
from equipment.services import mask_to_regex


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "sn_mask")
    search_fields = ("name", "sn_mask")

    def save_model(self, request, obj, form, change):
        """Валидация формата маски SN прямо в админке."""
        try:
            re.compile(mask_to_regex(obj.sn_mask))
        except re.error:
            raise ValidationError("Неверный формат маски SN.")
        super().save_model(request, obj, form, change)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("sn", "equipment_type", "note", "is_deleted")
    list_filter = ("equipment_type", "is_deleted")
    search_fields = ("sn", "note")
    ordering = ("sn",)
