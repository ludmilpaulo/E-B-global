from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User, Location
from services.models import Service, ServiceCategory
from bookings.models import Booking
from payments.models import Payment


class AnalyticsMetric(models.Model):
    """Base analytics metrics tracking"""
    
    class MetricType(models.TextChoices):
        DAILY = 'DAILY', _('Daily')
        WEEKLY = 'WEEKLY', _('Weekly')
        MONTHLY = 'MONTHLY', _('Monthly')
        QUARTERLY = 'QUARTERLY', _('Quarterly')
        YEARLY = 'YEARLY', _('Yearly')
    
    # Time period
    date = models.DateField()
    period_type = models.CharField(max_length=10, choices=MetricType.choices, default=MetricType.DAILY)
    
    # Geographic filters
    country = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        limit_choices_to={'location_type': 'COUNTRY'},
        related_name='analytics_metrics_country'
    )
    province = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        limit_choices_to={'location_type': 'PROVINCE'},
        related_name='analytics_metrics_province'
    )
    
    # Service category filter
    category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    # Booking metrics
    total_bookings = models.PositiveIntegerField(default=0)
    new_bookings = models.PositiveIntegerField(default=0)
    completed_bookings = models.PositiveIntegerField(default=0)
    cancelled_bookings = models.PositiveIntegerField(default=0)
    
    # Financial metrics
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    platform_fees = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    partner_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # User metrics
    active_clients = models.PositiveIntegerField(default=0)
    active_partners = models.PositiveIntegerField(default=0)
    new_clients = models.PositiveIntegerField(default=0)
    new_partners = models.PositiveIntegerField(default=0)
    
    # Performance metrics
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    completion_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Analytics Metric')
        verbose_name_plural = _('Analytics Metrics')
        ordering = ['-date']
        unique_together = ['date', 'period_type', 'country', 'province', 'category']
        indexes = [
            models.Index(fields=['date', 'period_type']),
            models.Index(fields=['country', 'date']),
            models.Index(fields=['category', 'date']),
        ]
    
    def __str__(self):
        return f"{self.date} - {self.get_period_type_display()}"


class PartnerAnalytics(models.Model):
    """Partner-specific analytics and performance metrics"""
    
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics')
    
    # Time period
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Booking metrics
    total_bookings = models.PositiveIntegerField(default=0)
    completed_bookings = models.PositiveIntegerField(default=0)
    cancelled_bookings = models.PositiveIntegerField(default=0)
    no_show_bookings = models.PositiveIntegerField(default=0)
    
    # Revenue metrics
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pending_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    platform_fees_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Performance metrics
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    response_time_minutes = models.PositiveIntegerField(null=True, blank=True)
    completion_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Client metrics
    repeat_clients = models.PositiveIntegerField(default=0)
    new_clients = models.PositiveIntegerField(default=0)
    client_satisfaction_score = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Partner Analytics')
        verbose_name_plural = _('Partner Analytics')
        ordering = ['-period_end']
        unique_together = ['partner', 'period_start', 'period_end']
    
    def __str__(self):
        return f"{self.partner.get_full_name()} - {self.period_start} to {self.period_end}"


class ServicePerformance(models.Model):
    """Service-level performance analytics"""
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='performance_analytics')
    
    # Time period
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Booking metrics
    total_bookings = models.PositiveIntegerField(default=0)
    completed_bookings = models.PositiveIntegerField(default=0)
    cancelled_bookings = models.PositiveIntegerField(default=0)
    
    # Revenue metrics
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    average_booking_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Performance metrics
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    completion_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Popularity metrics
    views_count = models.PositiveIntegerField(default=0)
    favorites_count = models.PositiveIntegerField(default=0)
    conversion_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Service Performance')
        verbose_name_plural = _('Service Performance')
        ordering = ['-period_end']
        unique_together = ['service', 'period_start', 'period_end']
    
    def __str__(self):
        return f"{self.service.name} - {self.period_start} to {self.period_end}"


class ConversionFunnel(models.Model):
    """Conversion funnel analytics"""
    
    class FunnelStage(models.TextChoices):
        VISIT = 'VISIT', _('Visit')
        SERVICE_VIEW = 'SERVICE_VIEW', _('Service View')
        BOOKING_START = 'BOOKING_START', _('Booking Started')
        BOOKING_COMPLETE = 'BOOKING_COMPLETE', _('Booking Completed')
        PAYMENT = 'PAYMENT', _('Payment Made')
        SERVICE_COMPLETED = 'SERVICE_COMPLETED', _('Service Completed')
    
    # Time period
    date = models.DateField()
    
    # Geographic filters
    country = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        limit_choices_to={'location_type': 'COUNTRY'}
    )
    category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    # Funnel metrics
    stage = models.CharField(max_length=20, choices=FunnelStage.choices)
    users_count = models.PositiveIntegerField(default=0)
    conversion_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Conversion Funnel')
        verbose_name_plural = _('Conversion Funnels')
        ordering = ['-date']
        unique_together = ['date', 'country', 'category', 'stage']
    
    def __str__(self):
        return f"{self.date} - {self.get_stage_display()} ({self.users_count} users)"


class UserEngagement(models.Model):
    """User engagement and behavior analytics"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='engagement_analytics')
    
    # Time period
    date = models.DateField()
    
    # Engagement metrics
    page_views = models.PositiveIntegerField(default=0)
    session_duration_minutes = models.PositiveIntegerField(default=0)
    actions_count = models.PositiveIntegerField(default=0)
    
    # Feature usage
    services_viewed = models.PositiveIntegerField(default=0)
    bookings_made = models.PositiveIntegerField(default=0)
    messages_sent = models.PositiveIntegerField(default=0)
    reviews_written = models.PositiveIntegerField(default=0)
    
    # Platform usage
    web_sessions = models.PositiveIntegerField(default=0)
    mobile_sessions = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User Engagement')
        verbose_name_plural = _('User Engagement')
        ordering = ['-date']
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.date}"


class GeographicAnalytics(models.Model):
    """Geographic distribution analytics"""
    
    # Time period
    date = models.DateField()
    period_type = models.CharField(
        max_length=10, 
        choices=AnalyticsMetric.MetricType.choices, 
        default=AnalyticsMetric.MetricType.DAILY
    )
    
    # Geographic location
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='geographic_analytics')
    
    # Metrics
    total_bookings = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    active_partners = models.PositiveIntegerField(default=0)
    active_clients = models.PositiveIntegerField(default=0)
    
    # Popular services
    top_categories = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Geographic Analytics')
        verbose_name_plural = _('Geographic Analytics')
        ordering = ['-date']
        unique_together = ['date', 'period_type', 'location']
    
    def __str__(self):
        return f"{self.location.name} - {self.date}"


class SystemMetrics(models.Model):
    """System performance and operational metrics"""
    
    # Time period
    date = models.DateField()
    hour = models.PositiveIntegerField(null=True, blank=True, help_text=_('Hour of day (0-23)'))
    
    # Performance metrics
    response_time_ms = models.PositiveIntegerField(default=0)
    error_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    uptime_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Usage metrics
    api_requests = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    concurrent_bookings = models.PositiveIntegerField(default=0)
    
    # Resource usage
    cpu_usage_percent = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    memory_usage_percent = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('System Metrics')
        verbose_name_plural = _('System Metrics')
        ordering = ['-date', '-hour']
        unique_together = ['date', 'hour']
    
    def __str__(self):
        if self.hour is not None:
            return f"{self.date} {self.hour:02d}:00 - Response: {self.response_time_ms}ms"
        return f"{self.date} - Response: {self.response_time_ms}ms"
