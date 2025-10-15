from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookingViewSet, BookingSearchView, BookingStatsView, BookingCalendarView
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'list', BookingViewSet, basename='booking')

urlpatterns = [
    # Search and analytics endpoints
    path('search/', BookingSearchView.as_view(), name='booking_search'),
    path('stats/', BookingStatsView.as_view(), name='booking_stats'),
    path('calendar/', BookingCalendarView.as_view(), name='booking_calendar'),
    
    # Include router URLs
    path('', include(router.urls)),
]
