from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceCategoryViewSet, ServiceViewSet, ServiceAttributeViewSet,
    ServiceSearchView, FeaturedServicesView, PopularServicesView
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet, basename='servicecategory')
router.register(r'list', ServiceViewSet, basename='service')
router.register(r'attributes', ServiceAttributeViewSet, basename='serviceattribute')

urlpatterns = [
    # Search and discovery endpoints
    path('search/', ServiceSearchView.as_view(), name='service_search'),
    path('featured/', FeaturedServicesView.as_view(), name='featured_services'),
    path('popular/', PopularServicesView.as_view(), name='popular_services'),
    
    # Include router URLs
    path('', include(router.urls)),
]
