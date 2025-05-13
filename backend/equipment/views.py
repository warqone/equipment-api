from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters, mixins, permissions, response, status, viewsets)

from equipment.models import Equipment, EquipmentType
from equipment.pagination import CustomPagination
from equipment.serializers import EquipmentSerializer, EquipmentTypeSerializer
from equipment.services import create_equipment


class EquipmentViewSet(viewsets.ModelViewSet):
    """CRUD для оборудования.

    POST /equipment/ – позволяет передать сразу список SN:
        {
          "equipment_type_id": 1,
          "serial_nums": ["ABC-01", "ABC-02"],
          "note": "склад №3"
        }
    Другие методы работают стандартно.
    """

    queryset = Equipment.objects.filter(is_deleted=False)
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["equipment_type__id", "is_deleted"]
    search_fields = ["sn", "note", "equipment_type__name"]

    def create(self, request, *args, **kwargs):
        """Множественное создание через сервисный слой."""
        type_id = request.data.get("equipment_type_id")
        serial_nums = request.data.get("serial_nums", [])
        note = request.data.get("note", "")

        if not isinstance(serial_nums, (list, tuple)):
            serial_nums = [serial_nums]

        result = create_equipment(type_id, serial_nums, note)
        status_code = (
            status.HTTP_201_CREATED if not result[
                "errors"] else status.HTTP_400_BAD_REQUEST
        )
        return response.Response(result, status=status_code)

    def destroy(self, request, *args, **kwargs):
        """Мягкое удаление (is_deleted=True)."""
        instance = self.get_object()
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def handle_exception(self, exc):
        """Обработка исключений."""
        if isinstance(exc, EquipmentType.DoesNotExist):
            return response.Response(
                {"equipment_type_id": "Неверный тип оборудования"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().handle_exception(exc)


class EquipmentTypeViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    """Справочник типов оборудования."""
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "sn_mask"]
