from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import (
    UserRegistrationView, UserLoginView, UserProfileView,
    PartnerProfileView, UserPreferencesView, PasswordChangeView,
    LocationListView, logout_view
)

# Create router for ViewSets
router = DefaultRouter()

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Authentication endpoints
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', logout_view, name='user_logout'),
    
    # User profile endpoints
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('partner-profile/', PartnerProfileView.as_view(), name='partner_profile'),
    path('preferences/', UserPreferencesView.as_view(), name='user_preferences'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
    
    # Location endpoints
    path('locations/', LocationListView.as_view(), name='location_list'),
    
    # Include router URLs
    path('', include(router.urls)),
]
