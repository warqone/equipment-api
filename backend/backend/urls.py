from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('equipment.urls')),
    path('api/user/login/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
