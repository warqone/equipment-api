from django.db import models

from equipment.constants import (
    LIMIT_SELF_NAME,
    NAME_MAX_LENGTH,
    SN_MAX_LENGTH,
    NOTE_MAX_LENGTH,
)


class EquipmentType(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    sn_mask = models.CharField(max_length=SN_MAX_LENGTH)

    class Meta:
        ordering = ["name"]
        verbose_name = "Equipment Type"
        verbose_name_plural = "Equipment Types"

    def __str__(self) -> str:
        return self.name[:LIMIT_SELF_NAME]


class Equipment(models.Model):
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.PROTECT)
    sn = models.CharField(max_length=SN_MAX_LENGTH)
    note = models.CharField(max_length=NOTE_MAX_LENGTH, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("equipment_type", "sn")
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"

    def __str__(self) -> str:
        return f"{self.equipment_type} {self.sn}"
