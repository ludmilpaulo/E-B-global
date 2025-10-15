from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from accounts.models import User, Location
from bookings.models import Booking


class Payment(models.Model):
    """Payment transactions for bookings"""
    
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')
        CANCELLED = 'CANCELLED', _('Cancelled')
        REFUNDED = 'REFUNDED', _('Refunded')
        PARTIALLY_REFUNDED = 'PARTIALLY_REFUNDED', _('Partially Refunded')
    
    class PaymentMethod(models.TextChoices):
        CARD = 'CARD', _('Credit/Debit Card')
        BANK_TRANSFER = 'BANK_TRANSFER', _('Bank Transfer')
        MOBILE_MONEY = 'MOBILE_MONEY', _('Mobile Money')
        WALLET = 'WALLET', _('Digital Wallet')
        CASH = 'CASH', _('Cash Payment')
        OTHER = 'OTHER', _('Other')
    
    # Basic payment information
    payment_id = models.CharField(max_length=50, unique=True)
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name='payments')
    payer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments_made')
    recipient = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments_received')
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    
    # Payment gateway information
    gateway = models.CharField(max_length=50, blank=True, help_text=_('Payment gateway used (Stripe, Paystack, etc.)'))
    gateway_transaction_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Fees and taxes
    gateway_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Metadata
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_id']),
            models.Index(fields=['booking', 'status']),
            models.Index(fields=['payer', 'created_at']),
        ]
    
    def __str__(self):
        return f"Payment {self.payment_id} - {self.amount} {self.currency}"
    
    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = self.generate_payment_id()
        super().save(*args, **kwargs)
    
    def generate_payment_id(self):
        """Generate unique payment ID"""
        import uuid
        return f"PAY{uuid.uuid4().hex[:12].upper()}"
    
    @property
    def is_successful(self):
        return self.status == self.PaymentStatus.COMPLETED


class Invoice(models.Model):
    """Invoices for bookings"""
    
    class InvoiceStatus(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        SENT = 'SENT', _('Sent')
        PAID = 'PAID', _('Paid')
        OVERDUE = 'OVERDUE', _('Overdue')
        CANCELLED = 'CANCELLED', _('Cancelled')
    
    invoice_number = models.CharField(max_length=20, unique=True)
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name='invoices')
    
    # Invoice details
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=15,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.DRAFT
    )
    
    # Billing information
    bill_to = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='invoices_received',
        help_text=_('Client receiving the invoice')
    )
    bill_from = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='invoices_sent',
        help_text=_('Partner sending the invoice')
    )
    
    # Amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Payment information
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # File information
    pdf_url = models.URLField(blank=True)
    pdf_generated_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    terms_conditions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.total_amount} {self.currency}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)
    
    def generate_invoice_number(self):
        """Generate unique invoice number"""
        import uuid
        return f"INV{uuid.uuid4().hex[:8].upper()}"
    
    @property
    def is_paid(self):
        return self.status == self.InvoiceStatus.PAID
    
    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.due_date < timezone.now().date() and not self.is_paid


class Payout(models.Model):
    """Partner payouts from completed bookings"""
    
    class PayoutStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')
        CANCELLED = 'CANCELLED', _('Cancelled')
    
    payout_id = models.CharField(max_length=50, unique=True)
    partner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payouts')
    
    # Payout details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(
        max_length=15,
        choices=PayoutStatus.choices,
        default=PayoutStatus.PENDING
    )
    
    # Bank account details (encrypted)
    bank_account_details = models.JSONField(default=dict, blank=True)
    
    # Related payments
    payments = models.ManyToManyField(Payment, related_name='payouts', blank=True)
    
    # Processing information
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Metadata
    description = models.TextField(blank=True)
    failure_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('Payout')
        verbose_name_plural = _('Payouts')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payout {self.payout_id} - {self.amount} {self.currency}"
    
    def save(self, *args, **kwargs):
        if not self.payout_id:
            self.payout_id = self.generate_payout_id()
        super().save(*args, **kwargs)
    
    def generate_payout_id(self):
        """Generate unique payout ID"""
        import uuid
        return f"OUT{uuid.uuid4().hex[:12].upper()}"
    
    @property
    def is_completed(self):
        return self.status == self.PayoutStatus.COMPLETED


class Refund(models.Model):
    """Refunds for cancelled or disputed bookings"""
    
    class RefundStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')
        CANCELLED = 'CANCELLED', _('Cancelled')
    
    class RefundType(models.TextChoices):
        FULL = 'FULL', _('Full Refund')
        PARTIAL = 'PARTIAL', _('Partial Refund')
        CHARGEBACK = 'CHARGEBACK', _('Chargeback')
        DISPUTE = 'DISPUTE', _('Dispute Resolution')
    
    refund_id = models.CharField(max_length=50, unique=True)
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name='refunds')
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name='refunds')
    
    # Refund details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='USD')
    refund_type = models.CharField(max_length=15, choices=RefundType.choices)
    status = models.CharField(
        max_length=15,
        choices=RefundStatus.choices,
        default=RefundStatus.PENDING
    )
    
    # Reason and approval
    reason = models.TextField()
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_refunds'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Gateway information
    gateway_refund_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Metadata
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('Refund')
        verbose_name_plural = _('Refunds')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Refund {self.refund_id} - {self.amount} {self.currency}"
    
    def save(self, *args, **kwargs):
        if not self.refund_id:
            self.refund_id = self.generate_refund_id()
        super().save(*args, **kwargs)
    
    def generate_refund_id(self):
        """Generate unique refund ID"""
        import uuid
        return f"REF{uuid.uuid4().hex[:12].upper()}"
    
    @property
    def is_completed(self):
        return self.status == self.RefundStatus.COMPLETED


class PaymentMethod(models.Model):
    """Stored payment methods for users"""
    
    class MethodType(models.TextChoices):
        CARD = 'CARD', _('Credit/Debit Card')
        BANK_ACCOUNT = 'BANK_ACCOUNT', _('Bank Account')
        MOBILE_MONEY = 'MOBILE_MONEY', _('Mobile Money')
        WALLET = 'WALLET', _('Digital Wallet')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    method_type = models.CharField(max_length=15, choices=MethodType.choices)
    
    # Encrypted payment method details
    encrypted_details = models.JSONField(default=dict, blank=True)
    
    # Display information
    last_four = models.CharField(max_length=4, blank=True)
    brand = models.CharField(max_length=20, blank=True)
    expiry_month = models.PositiveIntegerField(null=True, blank=True)
    expiry_year = models.PositiveIntegerField(null=True, blank=True)
    
    # Status
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Gateway information
    gateway_customer_id = models.CharField(max_length=100, blank=True)
    gateway_method_id = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Payment Method')
        verbose_name_plural = _('Payment Methods')
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        if self.method_type == self.MethodType.CARD:
            return f"{self.brand} ****{self.last_four}"
        return f"{self.get_method_type_display()} - {self.user.get_full_name()}"
