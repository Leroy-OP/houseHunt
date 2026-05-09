from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import register, login, AgencyViewSet, PropertyViewSet, BookingViewSet, AmenityViewSet

router = DefaultRouter()
router.register(r'agents', AgencyViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'amenities',  AmenityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
