from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Location, PartnerProfile, UserPreference


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin with role-based fields"""
    
    list_display = ('email', 'first_name', 'last_name', 'role', 'status', 'is_kyc_verified', 'date_joined')
    list_filter = ('role', 'status', 'is_kyc_verified', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture', 'preferred_language')
        }),
        (_('Role & Status'), {
            'fields': ('role', 'status', 'is_kyc_verified', 'kyc_verified_at', 'kyc_documents')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'last_login_ip')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login', 'kyc_verified_at')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Location Admin for countries, provinces, and cities"""
    
    list_display = ('name', 'name_pt', 'name_en', 'location_type', 'parent', 'code', 'is_active')
    list_filter = ('location_type', 'is_active', 'parent')
    search_fields = ('name', 'name_pt', 'name_en', 'code')
    ordering = ('location_type', 'name')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'name_pt', 'name_en', 'location_type', 'parent', 'code')
        }),
        (_('Geographic Data'), {
            'fields': ('latitude', 'longitude', 'is_active')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')


@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    """Partner Profile Admin"""
    
    list_display = ('business_name', 'user', 'verification_status', 'primary_location', 'average_rating', 'total_earnings')
    list_filter = ('verification_status', 'primary_location', 'payout_frequency')
    search_fields = ('business_name', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('Business Information'), {
            'fields': ('user', 'business_name', 'business_description', 'business_registration_number', 'tax_id')
        }),
        (_('Location & Coverage'), {
            'fields': ('primary_location', 'service_areas')
        }),
        (_('Business Details'), {
            'fields': ('website_url', 'business_hours', 'payout_frequency')
        }),
        (_('Verification'), {
            'fields': ('verification_status', 'verification_documents', 'verification_notes', 'verified_by', 'verified_at')
        }),
        (_('Financial'), {
            'fields': ('bank_account_details', 'total_earnings', 'completed_bookings', 'average_rating')
        }),
    )
    
    readonly_fields = ('total_earnings', 'completed_bookings', 'average_rating', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'primary_location', 'verified_by')


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    """User Preferences Admin"""
    
    list_display = ('user', 'default_country', 'default_province', 'notification_email', 'notification_push')
    list_filter = ('notification_email', 'notification_sms', 'notification_push', 'marketing_emails')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    
    fieldsets = (
        (_('User'), {
            'fields': ('user',)
        }),
        (_('Location Preferences'), {
            'fields': ('default_country', 'default_province')
        }),
        (_('Notification Preferences'), {
            'fields': ('notification_email', 'notification_sms', 'notification_push', 'marketing_emails')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'default_country', 'default_province')
