from rest_framework import viewsets, status, filters, response, permissions

from equipment.models import Equipment, EquipmentType
from equipment.serializers import EquipmentSerializer, EquipmentTypeSerializer
from equipment.services import create_equipment


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.filter(is_deleted=False)
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['sn', 'note', 'equipment_type__name']

    def create(self, request, *args, **kwargs):
        type_id = request.data.get('equipment_type_id')
        serial_nums = request.data.get('serial_nums', [])
        note = request.data.get('note', '')
        if not isinstance(serial_nums, list):
            serial_nums = [serial_nums]
        result = create_equipment(type_id, serial_nums, note)
        return response.Response(
            result,
            status=status.HTTP_201_CREATED
        ) if not result['errors'] else response.Response(
            result, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class EquipmentTypeViewSet(viewsets.ModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'sn_mask']
