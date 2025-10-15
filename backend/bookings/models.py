from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User, Location
from services.models import Service, AvailabilitySlot


class Booking(models.Model):
    """Main booking model for service appointments"""
    
    class BookingStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        CONFIRMED = 'CONFIRMED', _('Confirmed')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')
        RESCHEDULED = 'RESCHEDULED', _('Rescheduled')
        DISPUTED = 'DISPUTED', _('Disputed')
        REFUNDED = 'REFUNDED', _('Refunded')
    
    class BookingType(models.TextChoices):
        REGULAR = 'REGULAR', _('Regular Booking')
        URGENT = 'URGENT', _('Urgent Booking')
        RECURRING = 'RECURRING', _('Recurring Booking')
    
    # Basic booking information
    booking_number = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_bookings')
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partner_bookings')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='bookings')
    availability_slot = models.ForeignKey(
        AvailabilitySlot, 
        on_delete=models.PROTECT, 
        related_name='bookings',
        null=True,
        blank=True
    )
    
    # Scheduling
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    
    # Location details
    service_location = models.ForeignKey(
        Location, 
        on_delete=models.PROTECT, 
        related_name='service_bookings',
        null=True,
        blank=True
    )
    location_address = models.TextField(blank=True)
    location_coordinates = models.JSONField(default=dict, blank=True)
    is_online_service = models.BooleanField(default=False)
    
    # Booking details
    booking_type = models.CharField(max_length=15, choices=BookingType.choices, default=BookingType.REGULAR)
    status = models.CharField(
        max_length=15,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )
    
    # Pricing and payment
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    additional_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Service-specific data
    service_data = models.JSONField(default=dict, blank=True, help_text=_('Service-specific booking data'))
    
    # Special requirements
    special_requirements = models.TextField(blank=True)
    client_notes = models.TextField(blank=True)
    partner_notes = models.TextField(blank=True)
    
    # Status tracking
    confirmed_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    # Ratings and feedback
    client_rating = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    client_review = models.TextField(blank=True)
    partner_rating = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    partner_review = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['booking_number']),
            models.Index(fields=['client', 'status']),
            models.Index(fields=['partner', 'status']),
            models.Index(fields=['scheduled_start']),
        ]
    
    def __str__(self):
        return f"Booking #{self.booking_number} - {self.service.name}"
    
    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = self.generate_booking_number()
        super().save(*args, **kwargs)
    
    def generate_booking_number(self):
        """Generate unique booking number"""
        import uuid
        return f"EB{uuid.uuid4().hex[:8].upper()}"
    
    @property
    def duration_minutes(self):
        """Calculate booking duration in minutes"""
        if self.actual_start and self.actual_end:
            return int((self.actual_end - self.actual_start).total_seconds() / 60)
        return int((self.scheduled_end - self.scheduled_start).total_seconds() / 60)
    
    @property
    def is_active(self):
        """Check if booking is currently active"""
        return self.status in [self.BookingStatus.CONFIRMED, self.BookingStatus.IN_PROGRESS]
    
    @property
    def is_completed(self):
        """Check if booking is completed"""
        return self.status == self.BookingStatus.COMPLETED


class BookingStatusHistory(models.Model):
    """Track booking status changes"""
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=15, choices=Booking.BookingStatus.choices, blank=True)
    new_status = models.CharField(max_length=15, choices=Booking.BookingStatus.choices)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Booking Status History')
        verbose_name_plural = _('Booking Status Histories')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.booking.booking_number}: {self.old_status} → {self.new_status}"


class BookingMessage(models.Model):
    """Messages between client and partner for a booking"""
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    
    message = models.TextField()
    message_type = models.CharField(
        max_length=20,
        choices=[
            ('TEXT', 'Text Message'),
            ('SYSTEM', 'System Message'),
            ('STATUS_UPDATE', 'Status Update'),
            ('FILE', 'File Attachment'),
        ],
        default='TEXT'
    )
    
    # File attachments
    attachments = models.JSONField(default=list, blank=True, help_text=_('List of file URLs'))
    
    # Message status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Booking Message')
        verbose_name_plural = _('Booking Messages')
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.get_full_name()} for booking #{self.booking.booking_number}"


class BookingDocument(models.Model):
    """Documents and files related to a booking"""
    
    class DocumentType(models.TextChoices):
        INVOICE = 'INVOICE', _('Invoice')
        RECEIPT = 'RECEIPT', _('Receipt')
        CONTRACT = 'CONTRACT', _('Contract')
        PROOF_OF_SERVICE = 'PROOF_OF_SERVICE', _('Proof of Service')
        CLIENT_DOCUMENT = 'CLIENT_DOCUMENT', _('Client Document')
        OTHER = 'OTHER', _('Other')
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    
    document_type = models.CharField(max_length=20, choices=DocumentType.choices)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # File information
    file_url = models.URLField()
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    file_type = models.CharField(max_length=100)
    
    # Access control
    is_public = models.BooleanField(default=False)
    is_client_visible = models.BooleanField(default=True)
    is_partner_visible = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Booking Document')
        verbose_name_plural = _('Booking Documents')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.booking.booking_number}"


class BookingDispute(models.Model):
    """Dispute resolution for bookings"""
    
    class DisputeStatus(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        IN_REVIEW = 'IN_REVIEW', _('In Review')
        RESOLVED = 'RESOLVED', _('Resolved')
        CLOSED = 'CLOSED', _('Closed')
    
    class DisputeType(models.TextChoices):
        SERVICE_NOT_PROVIDED = 'SERVICE_NOT_PROVIDED', _('Service Not Provided')
        POOR_QUALITY = 'POOR_QUALITY', _('Poor Quality')
        BILLING_ISSUE = 'BILLING_ISSUE', _('Billing Issue')
        CANCELLATION = 'CANCELLATION', _('Cancellation Issue')
        OTHER = 'OTHER', _('Other')
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='dispute')
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='raised_disputes')
    disputed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disputed_against')
    
    dispute_type = models.CharField(max_length=25, choices=DisputeType.choices)
    status = models.CharField(
        max_length=15,
        choices=DisputeStatus.choices,
        default=DisputeStatus.OPEN
    )
    
    description = models.TextField()
    evidence_documents = models.JSONField(default=list, blank=True)
    
    # Resolution
    resolution = models.TextField(blank=True)
    resolution_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    resolved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='resolved_disputes'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Booking Dispute')
        verbose_name_plural = _('Booking Disputes')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Dispute for booking #{self.booking.booking_number} - {self.dispute_type}"


class RecurringBooking(models.Model):
    """Recurring booking patterns"""
    
    class RecurrenceType(models.TextChoices):
        DAILY = 'DAILY', _('Daily')
        WEEKLY = 'WEEKLY', _('Weekly')
        MONTHLY = 'MONTHLY', _('Monthly')
        CUSTOM = 'CUSTOM', _('Custom')
    
    parent_booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='recurring_pattern')
    
    recurrence_type = models.CharField(max_length=10, choices=RecurrenceType.choices)
    recurrence_interval = models.PositiveIntegerField(default=1, help_text=_('Every X days/weeks/months'))
    recurrence_days = models.JSONField(default=list, blank=True, help_text=_('Days of week for weekly recurrence'))
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    max_occurrences = models.PositiveIntegerField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Recurring Booking')
        verbose_name_plural = _('Recurring Bookings')
    
    def __str__(self):
        return f"Recurring booking for {self.parent_booking.service.name}"
