import re
from django.db import transaction

from equipment.models import Equipment, EquipmentType


MASK_MAP = {
    'N': r'[0-9]',
    'A': r'[A-Z]',
    'a': r'[a-z]',
    'X': r'[A-Z0-9]',
    'Z': r'[-_@]',
}


def mask_to_regex(mask):
    regex = ''
    for char in mask:
        regex += MASK_MAP.get(char, re.escape(char))
    return '^' + regex + '$'


def validate_sn(sn, mask):
    regex = mask_to_regex(mask)
    return re.match(regex, sn) is not None


def create_equipment(equipment_type, sn, note):
    errors = []
    created = []
    eq_type = EquipmentType.objects.get(pk=equipment_type)
    for s in sn:
        if not validate_sn(s, eq_type.sn_mask):
            errors.append(s + ' is not valid')
            continue
        if Equipment.objects.filter(sn=s).exists():
            errors.append(s + ' already exists')
            continue
        created.append(Equipment(equipment_type=eq_type, sn=s, note=note))
    with transaction.atomic():
        Equipment.objects.bulk_create(created)
    return {'created': [e.sn for e in created], 'errors': errors}
