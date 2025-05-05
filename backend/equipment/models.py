from django.db import models

from equipment.constants import (
    LIMIT_SELF_NAME, NAME_MAX_LENGTH, SN_MAX_LENGTH, NOTE_MAX_LENGTH)


class EquipmentType(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    sn_mask = models.CharField(max_length=SN_MAX_LENGTH)

    def __str__(self):
        return self.name[:LIMIT_SELF_NAME]

    class Meta:
        verbose_name = 'Equipment Type'
        verbose_name_plural = 'Equipment Types'
        ordering = ['name']


class Equipment(models.Model):
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.PROTECT)
    sn = models.CharField(max_length=SN_MAX_LENGTH)
    note = models.CharField(blank=True, max_length=NOTE_MAX_LENGTH)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'
        unique_together = ('equipment_type', 'sn')

    def __str__(self):
        return f'{self.equipment_type} {self.sn}'
