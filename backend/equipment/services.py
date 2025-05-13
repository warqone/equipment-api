import re
from typing import Sequence

from django.db import transaction
from rest_framework import serializers

from equipment.models import Equipment, EquipmentType

MASK_MAP = {
    'N': r'[0-9]',
    'A': r'[A-Z]',
    'a': r'[a-z]',
    'X': r'[A-Z0-9]',
    'Z': r'[-_@]',
}


def mask_to_regex(mask: str) -> str:
    """Преобразует символьную маску в regex-строку."""
    regex = ''.join(MASK_MAP.get(ch, re.escape(ch)) for ch in mask)
    return fr'^{regex}$'


def validate_sn_mask(sn: str, mask: str) -> bool:
    """Проверяет, что SN соответствует маске."""
    return re.fullmatch(mask_to_regex(mask), sn) is not None


def create_equipment(
    type_id: int,
    sn_list: Sequence[str],
    note: str | None = "",
) -> dict[str, list[str]]:
    """Создаёт оборудование пачкой, атомарно.

    Возвращает {'created': [...], 'errors': [...]}.
    При наличии ошибок все изменения откатываются.
    """
    eq_type = EquipmentType.objects.filter(pk=type_id).first()
    if not eq_type:
        raise serializers.ValidationError(
            {"equipment_type_id": "Тип не найден"}
        )

    errors, created_objs = [], []

    with transaction.atomic():
        for sn in sn_list:
            if not validate_sn_mask(sn, eq_type.sn_mask):
                errors.append(f"{sn}: неверный формат SN")
                continue
            if Equipment.objects.filter(
                sn=sn,
                equipment_type=eq_type,
                is_deleted=False,
            ).exists():
                errors.append(f"{sn}: уже существует")
                continue
            created_objs.append(
                Equipment(equipment_type=eq_type, sn=sn, note=note)
            )

        if errors:
            raise serializers.ValidationError(errors)

        Equipment.objects.bulk_create(created_objs)

    return {"created": [obj.sn for obj in created_objs], "errors": []}
