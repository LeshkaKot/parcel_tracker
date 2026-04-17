from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostOfficeViewSet, ParcelViewSet

router = DefaultRouter()
router.register(r'offices', PostOfficeViewSet, basename='office')
router.register(r'parcels', ParcelViewSet, basename='parcel')

urlpatterns = [
    path('', include(router.urls)),
]