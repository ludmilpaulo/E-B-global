from rest_framework import serializers
from django.utils import timezone
from django.db import transaction
from .models import (
    Booking, BookingStatusHistory, BookingMessage, BookingDocument,
    BookingDispute, RecurringBooking
)
from accounts.serializers import UserProfileSerializer, LocationSerializer
from services.serializers import ServiceDetailSerializer, AvailabilitySlotSerializer


class BookingStatusHistorySerializer(serializers.ModelSerializer):
    """Serializer for booking status history"""
    
    class Meta:
        model = BookingStatusHistory
        fields = [
            'id', 'status', 'timestamp', 'notes', 'created_by',
            'created_at'
        ]
        read_only_fields = ['id', 'timestamp', 'created_at']


class BookingMessageSerializer(serializers.ModelSerializer):
    """Serializer for booking messages"""
    sender = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = BookingMessage
        fields = [
            'id', 'booking', 'sender', 'message', 'message_type',
            'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'created_at']


class BookingDocumentSerializer(serializers.ModelSerializer):
    """Serializer for booking documents"""
    uploaded_by = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = BookingDocument
        fields = [
            'id', 'booking', 'document_type', 'file', 'description',
            'uploaded_by', 'created_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'created_at']


class BookingDisputeSerializer(serializers.ModelSerializer):
    """Serializer for booking disputes"""
    created_by = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = BookingDispute
        fields = [
            'id', 'booking', 'dispute_type', 'description', 'status',
            'resolution_notes', 'created_by', 'resolved_by', 'created_at',
            'resolved_at'
        ]
        read_only_fields = [
            'id', 'created_by', 'resolved_by', 'created_at', 'resolved_at'
        ]


class BookingListSerializer(serializers.ModelSerializer):
    """Serializer for booking list view (optimized)"""
    client = UserProfileSerializer(read_only=True)
    partner = UserProfileSerializer(read_only=True)
    service = ServiceDetailSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_number', 'client', 'partner', 'service',
            'location', 'scheduled_start', 'scheduled_end', 'status',
            'total_amount', 'currency', 'created_at'
        ]
        read_only_fields = ['id', 'booking_number', 'created_at']


class BookingDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed booking view"""
    client = UserProfileSerializer(read_only=True)
    partner = UserProfileSerializer(read_only=True)
    service = ServiceDetailSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    status_history = BookingStatusHistorySerializer(many=True, read_only=True)
    messages = BookingMessageSerializer(many=True, read_only=True)
    documents = BookingDocumentSerializer(many=True, read_only=True)
    disputes = BookingDisputeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_number', 'client', 'partner', 'service',
            'location', 'scheduled_start', 'scheduled_end', 'status',
            'total_amount', 'currency', 'service_fee', 'platform_fee',
            'tax_amount', 'special_requirements', 'client_notes',
            'partner_notes', 'client_rating', 'client_comment',
            'partner_rating', 'partner_comment', 'status_history',
            'messages', 'documents', 'disputes', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'booking_number', 'created_at', 'updated_at'
        ]


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings"""
    slot_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'service', 'slot_id', 'location', 'special_requirements',
            'client_notes'
        ]
    
    def validate_slot_id(self, value):
        """Validate that the slot exists and is available"""
        from services.models import AvailabilitySlot
        
        try:
            slot = AvailabilitySlot.objects.get(id=value)
        except AvailabilitySlot.DoesNotExist:
            raise serializers.ValidationError("Invalid slot ID")
        
        if not slot.is_available:
            raise serializers.ValidationError("Slot is not available")
        
        if slot.start_time <= timezone.now():
            raise serializers.ValidationError("Cannot book past time slots")
        
        return value
    
    def validate(self, attrs):
        """Validate booking constraints"""
        slot_id = attrs.get('slot_id')
        service = attrs.get('service')
        
        if slot_id and service:
            from services.models import AvailabilitySlot
            
            try:
                slot = AvailabilitySlot.objects.get(id=slot_id)
                if slot.service != service:
                    raise serializers.ValidationError(
                        "Slot does not belong to the selected service"
                    )
            except AvailabilitySlot.DoesNotExist:
                raise serializers.ValidationError("Invalid slot")
        
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        """Create booking with slot validation"""
        slot_id = validated_data.pop('slot_id')
        
        # Get the slot and validate 90-minute duration
        from services.models import AvailabilitySlot
        slot = AvailabilitySlot.objects.get(id=slot_id)
        
        # Calculate 90-minute duration
        scheduled_start = slot.start_time
        scheduled_end = slot.start_time + timezone.timedelta(minutes=90)
        
        # Validate slot duration matches 90 minutes
        if (slot.end_time - slot.start_time).total_seconds() != 5400:  # 90 minutes
            raise serializers.ValidationError(
                "Booking slots must be exactly 90 minutes"
            )
        
        # Create booking
        booking = Booking.objects.create(
            client=self.context['request'].user,
            partner=validated_data['service'].partner,
            service=validated_data['service'],
            location=validated_data.get('location'),
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            special_requirements=validated_data.get('special_requirements', ''),
            client_notes=validated_data.get('client_notes', ''),
            total_amount=validated_data['service'].base_price,
            currency=validated_data['service'].currency,
            status='PENDING'
        )
        
        # Mark slot as unavailable
        slot.is_available = False
        slot.save()
        
        # Create initial status history
        BookingStatusHistory.objects.create(
            booking=booking,
            status='PENDING',
            notes='Booking created',
            created_by=self.context['request'].user
        )
        
        return booking


class BookingUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating bookings"""
    
    class Meta:
        model = Booking
        fields = [
            'special_requirements', 'client_notes', 'partner_notes',
            'client_rating', 'client_comment', 'partner_rating', 'partner_comment'
        ]
    
    def validate_client_rating(self, value):
        """Validate client rating"""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
    
    def validate_partner_rating(self, value):
        """Validate partner rating"""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value


class BookingStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating booking status"""
    status = serializers.ChoiceField(choices=Booking.BookingStatus.choices)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_status(self, value):
        """Validate status transition"""
        booking = self.context['booking']
        current_status = booking.status
        
        # Define valid status transitions
        valid_transitions = {
            'PENDING': ['CONFIRMED', 'CANCELLED'],
            'CONFIRMED': ['IN_PROGRESS', 'CANCELLED'],
            'IN_PROGRESS': ['COMPLETED', 'CANCELLED'],
            'COMPLETED': ['DISPUTED'],
            'CANCELLED': [],
            'DISPUTED': ['RESOLVED'],
            'RESOLVED': []
        }
        
        if value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Cannot transition from {current_status} to {value}"
            )
        
        return value


class RecurringBookingSerializer(serializers.ModelSerializer):
    """Serializer for recurring bookings"""
    
    class Meta:
        model = RecurringBooking
        fields = [
            'id', 'booking', 'frequency', 'interval', 'end_date',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookingSearchSerializer(serializers.Serializer):
    """Serializer for booking search parameters"""
    status = serializers.ChoiceField(
        choices=Booking.BookingStatus.choices,
        required=False
    )
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    partner_id = serializers.IntegerField(required=False)
    client_id = serializers.IntegerField(required=False)
    service_id = serializers.IntegerField(required=False)
    location_id = serializers.IntegerField(required=False)
    sort_by = serializers.ChoiceField(
        choices=['date_asc', 'date_desc', 'amount_asc', 'amount_desc', 'status'],
        default='date_desc'
    )
    page = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(default=20, min_value=1, max_value=100)
