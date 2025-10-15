from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User, Location


class ServiceCategory(models.Model):
    """Service categories for organizing different types of services"""
    
    name = models.CharField(max_length=100)
    name_pt = models.CharField(max_length=100, blank=True, help_text=_('Portuguese name'))
    name_en = models.CharField(max_length=100, blank=True, help_text=_('English name'))
    description = models.TextField(blank=True)
    description_pt = models.TextField(blank=True, help_text=_('Portuguese description'))
    description_en = models.TextField(blank=True, help_text=_('English description'))
    
    # Category hierarchy
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    # Display settings
    icon = models.CharField(max_length=50, blank=True, help_text=_('Icon class or identifier'))
    color = models.CharField(max_length=7, default='#007bff', help_text=_('Hex color code'))
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Service Category')
        verbose_name_plural = _('Service Categories')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def full_name(self):
        """Return the full category name with hierarchy"""
        if self.parent:
            return f"{self.parent.full_name} > {self.name}"
        return self.name


class Service(models.Model):
    """Individual service offered by partners"""
    
    class ServiceStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        SUSPENDED = 'SUSPENDED', _('Suspended')
        PENDING_APPROVAL = 'PENDING_APPROVAL', _('Pending Approval')
    
    class PricingType(models.TextChoices):
        FIXED = 'FIXED', _('Fixed Price')
        HOURLY = 'HOURLY', _('Hourly Rate')
        PER_UNIT = 'PER_UNIT', _('Per Unit')
        CUSTOM = 'CUSTOM', _('Custom Quote')
    
    # Basic information
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name='services')
    
    name = models.CharField(max_length=200)
    name_pt = models.CharField(max_length=200, blank=True, help_text=_('Portuguese name'))
    name_en = models.CharField(max_length=200, blank=True, help_text=_('English name'))
    
    description = models.TextField()
    description_pt = models.TextField(blank=True, help_text=_('Portuguese description'))
    description_en = models.TextField(blank=True, help_text=_('English description'))
    
    # Pricing
    pricing_type = models.CharField(max_length=10, choices=PricingType.choices, default=PricingType.FIXED)
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_('Base price in local currency')
    )
    currency = models.CharField(max_length=3, default='USD', help_text=_('Currency code (USD, EUR, etc.)')
    
    # Service details
    duration_minutes = models.PositiveIntegerField(
        default=90,
        validators=[MinValueValidator(30), MaxValueValidator(1440)],
        help_text=_('Minimum duration in minutes (must be at least 90 for 1.5h slots)')
    )
    max_duration_hours = models.PositiveIntegerField(
        default=8,
        validators=[MinValueValidator(1), MaxValueValidator(24)],
        help_text=_('Maximum duration in hours')
    )
    
    # Location and coverage
    primary_location = models.ForeignKey(
        Location, 
        on_delete=models.PROTECT, 
        related_name='primary_services'
    )
    service_areas = models.ManyToManyField(Location, related_name='available_services', blank=True)
    
    # Service attributes
    is_online_available = models.BooleanField(default=False, help_text=_('Can be provided online'))
    is_home_service = models.BooleanField(default=False, help_text=_('Can be provided at client location'))
    requires_equipment = models.BooleanField(default=False)
    equipment_provided = models.BooleanField(default=True)
    
    # Status and approval
    status = models.CharField(
        max_length=20,
        choices=ServiceStatus.choices,
        default=ServiceStatus.PENDING_APPROVAL
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_services'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Media
    images = models.JSONField(default=list, blank=True, help_text=_('List of image URLs'))
    
    # Metrics
    total_bookings = models.PositiveIntegerField(default=0)
    completed_bookings = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.partner.get_full_name()}"
    
    @property
    def is_approved(self):
        return self.status == self.ServiceStatus.ACTIVE
    
    @property
    def completion_rate(self):
        """Calculate service completion rate"""
        if self.total_bookings == 0:
            return 0
        return (self.completed_bookings / self.total_bookings) * 100


class ServiceAttribute(models.Model):
    """Custom attributes for services (e.g., vehicle type for transport)"""
    
    class AttributeType(models.TextChoices):
        TEXT = 'TEXT', _('Text')
        NUMBER = 'NUMBER', _('Number')
        SELECT = 'SELECT', _('Select')
        MULTISELECT = 'MULTISELECT', _('Multi-select')
        BOOLEAN = 'BOOLEAN', _('Boolean')
        FILE = 'FILE', _('File Upload')
    
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=100)
    name_pt = models.CharField(max_length=100, blank=True)
    name_en = models.CharField(max_length=100, blank=True)
    
    attribute_type = models.CharField(max_length=15, choices=AttributeType.choices)
    is_required = models.BooleanField(default=False)
    is_filterable = models.BooleanField(default=False)
    
    # For select/multiselect options
    options = models.JSONField(default=list, blank=True, help_text=_('Available options for select fields'))
    options_pt = models.JSONField(default=list, blank=True, help_text=_('Portuguese options'))
    options_en = models.JSONField(default=list, blank=True, help_text=_('English options'))
    
    # Validation rules
    min_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_length = models.PositiveIntegerField(null=True, blank=True)
    
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Service Attribute')
        verbose_name_plural = _('Service Attributes')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"


class ServiceAttributeValue(models.Model):
    """Values for service attributes"""
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='attribute_values')
    attribute = models.ForeignKey(ServiceAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.JSONField(help_text=_('The actual attribute value'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Service Attribute Value')
        verbose_name_plural = _('Service Attribute Values')
        unique_together = ['service', 'attribute']
    
    def __str__(self):
        return f"{self.service.name} - {self.attribute.name}: {self.value}"


class AvailabilitySlot(models.Model):
    """90-minute availability slots for services"""
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='availability_slots')
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability_slots')
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    # Slot status
    is_available = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    block_reason = models.CharField(max_length=200, blank=True)
    
    # Pricing override for this slot
    price_override = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text=_('Override service price for this slot')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Availability Slot')
        verbose_name_plural = _('Availability Slots')
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['start_time', 'end_time']),
            models.Index(fields=['service', 'start_time']),
        ]
    
    def __str__(self):
        return f"{self.service.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    def clean(self):
        """Validate slot duration is exactly 90 minutes"""
        from django.core.exceptions import ValidationError
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            if duration.total_seconds() != 5400:  # 90 minutes in seconds
                raise ValidationError('Availability slots must be exactly 90 minutes (1h30)')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def duration_minutes(self):
        """Return slot duration in minutes"""
        if self.start_time and self.end_time:
            return int((self.end_time - self.start_time).total_seconds() / 60)
        return 0
    
    @property
    def effective_price(self):
        """Return the effective price for this slot"""
        return self.price_override if self.price_override else self.service.base_price
