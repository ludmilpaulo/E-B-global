from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Custom User model with role-based access control"""
    
    class UserRole(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        STAFF = 'STAFF', _('Staff')
        PARTNER = 'PARTNER', _('Partner')
        CLIENT = 'CLIENT', _('Client')
    
    class UserStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        SUSPENDED = 'SUSPENDED', _('Suspended')
        PENDING_VERIFICATION = 'PENDING_VERIFICATION', _('Pending Verification')
    
    # Override default fields
    email = models.EmailField(_('email address'), unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
                               message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Custom fields
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CLIENT,
        help_text=_('User role determining permissions')
    )
    status = models.CharField(
        max_length=25,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
        help_text=_('User account status')
    )
    preferred_language = models.CharField(
        max_length=2,
        choices=[('en', 'English'), ('pt', 'Português')],
        default='en',
        help_text=_('Preferred language for the interface')
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text=_('User profile picture')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # KYC fields for partners
    is_kyc_verified = models.BooleanField(default=False)
    kyc_verified_at = models.DateTimeField(null=True, blank=True)
    kyc_documents = models.JSONField(default=dict, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    @property
    def is_partner(self):
        return self.role == self.UserRole.PARTNER
    
    @property
    def is_client(self):
        return self.role == self.UserRole.CLIENT
    
    @property
    def is_admin_or_staff(self):
        return self.role in [self.UserRole.ADMIN, self.UserRole.STAFF]


class Location(models.Model):
    """Geographic location model for countries, provinces, and cities"""
    
    class LocationType(models.TextChoices):
        COUNTRY = 'COUNTRY', _('Country')
        PROVINCE = 'PROVINCE', _('Province')
        CITY = 'CITY', _('City')
    
    name = models.CharField(max_length=100)
    name_pt = models.CharField(max_length=100, blank=True, help_text=_('Portuguese name'))
    name_en = models.CharField(max_length=100, blank=True, help_text=_('English name'))
    location_type = models.CharField(max_length=10, choices=LocationType.choices)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=10, blank=True, help_text=_('ISO code or abbreviation'))
    is_active = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        ordering = ['name']
        unique_together = ['name', 'location_type', 'parent']
    
    def __str__(self):
        if self.parent:
            return f"{self.name}, {self.parent.name}"
        return self.name
    
    @property
    def full_name(self):
        """Return the full location name with hierarchy"""
        if self.parent:
            return f"{self.name}, {self.parent.full_name}"
        return self.name


class PartnerProfile(models.Model):
    """Extended profile for service providers (partners)"""
    
    class VerificationStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
        SUSPENDED = 'SUSPENDED', _('Suspended')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner_profile')
    business_name = models.CharField(max_length=200)
    business_description = models.TextField()
    business_registration_number = models.CharField(max_length=50, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    
    # Location and coverage
    primary_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='primary_partners')
    service_areas = models.ManyToManyField(Location, related_name='serving_partners', blank=True)
    
    # Business details
    website_url = models.URLField(blank=True)
    business_hours = models.JSONField(default=dict, help_text=_('Business hours by day of week'))
    
    # Verification and ratings
    verification_status = models.CharField(
        max_length=15,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING
    )
    verification_documents = models.JSONField(default=dict, blank=True)
    verification_notes = models.TextField(blank=True)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_partners'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Financial
    bank_account_details = models.JSONField(default=dict, blank=True)
    payout_frequency = models.CharField(
        max_length=20,
        choices=[
            ('WEEKLY', 'Weekly'),
            ('BIWEEKLY', 'Bi-weekly'),
            ('MONTHLY', 'Monthly'),
        ],
        default='WEEKLY'
    )
    
    # Metrics
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completed_bookings = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Partner Profile')
        verbose_name_plural = _('Partner Profiles')
    
    def __str__(self):
        return f"{self.business_name} ({self.user.get_full_name()})"
    
    @property
    def is_verified(self):
        return self.verification_status == self.VerificationStatus.APPROVED


class UserPreference(models.Model):
    """User preferences and settings"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    default_country = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'location_type': 'COUNTRY'}
    )
    default_province = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'location_type': 'PROVINCE'}
    )
    notification_email = models.BooleanField(default=True)
    notification_sms = models.BooleanField(default=False)
    notification_push = models.BooleanField(default=True)
    marketing_emails = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User Preference')
        verbose_name_plural = _('User Preferences')
    
    def __str__(self):
        return f"Preferences for {self.user.get_full_name()}"
