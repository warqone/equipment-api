from django.urls import path, include
from rest_framework import routers

from equipment import views

router = routers.DefaultRouter()
router.register(
    r'equipment', views.EquipmentViewSet, basename='equipment')
router.register(
    r'equipment-types', views.EquipmentTypeViewSet, basename='equipment-type')

urlpatterns = [
    path('', include(router.urls)),
]
