from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create router for ViewSets
router = DefaultRouter()

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
]
