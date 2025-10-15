from rest_framework import serializers
from django.db.models import Avg, Count
from .models import ServiceCategory, Service, ServiceAttribute, ServiceAttributeValue, AvailabilitySlot
from accounts.serializers import UserProfileSerializer, LocationSerializer


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Serializer for ServiceCategory model"""
    service_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceCategory
        fields = [
            'id', 'name_pt', 'name_en', 'description_pt', 'description_en',
            'icon', 'color', 'parent', 'is_active', 'service_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_service_count(self, obj):
        return obj.services.filter(is_active=True).count()


class ServiceAttributeSerializer(serializers.ModelSerializer):
    """Serializer for ServiceAttribute model"""
    
    class Meta:
        model = ServiceAttribute
        fields = [
            'id', 'name_pt', 'name_en', 'attribute_type', 'is_required',
            'options_pt', 'options_en', 'service_category'
        ]
        read_only_fields = ['id']


class ServiceAttributeValueSerializer(serializers.ModelSerializer):
    """Serializer for ServiceAttributeValue model"""
    attribute = ServiceAttributeSerializer(read_only=True)
    
    class Meta:
        model = ServiceAttributeValue
        fields = ['id', 'attribute', 'value', 'created_at']
        read_only_fields = ['id', 'created_at']


class AvailabilitySlotSerializer(serializers.ModelSerializer):
    """Serializer for AvailabilitySlot model"""
    
    class Meta:
        model = AvailabilitySlot
        fields = [
            'id', 'start_time', 'end_time', 'is_available',
            'price_override', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServiceListSerializer(serializers.ModelSerializer):
    """Serializer for listing services (optimized for list views)"""
    partner = UserProfileSerializer(read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    is_available_today = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id', 'title_pt', 'title_en', 'description_pt', 'description_en',
            'partner', 'category', 'location', 'base_price', 'currency',
            'duration_minutes', 'rating', 'review_count', 'is_available_today',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_rating(self, obj):
        # Calculate average rating from bookings
        from bookings.models import Booking
        avg_rating = Booking.objects.filter(
            service=obj,
            status='COMPLETED',
            client_rating__isnull=False
        ).aggregate(avg_rating=Avg('client_rating'))['avg_rating']
        return round(avg_rating, 1) if avg_rating else 0.0
    
    def get_review_count(self, obj):
        # Count completed bookings with ratings
        from bookings.models import Booking
        return Booking.objects.filter(
            service=obj,
            status='COMPLETED',
            client_rating__isnull=False
        ).count()
    
    def get_is_available_today(self, obj):
        # Check if service has available slots today
        from django.utils import timezone
        today = timezone.now().date()
        return obj.availability_slots.filter(
            start_time__date=today,
            is_available=True
        ).exists()


class ServiceDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed service view"""
    partner = UserProfileSerializer(read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    attributes = ServiceAttributeValueSerializer(many=True, read_only=True)
    availability_slots = AvailabilitySlotSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    recent_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id', 'title_pt', 'title_en', 'description_pt', 'description_en',
            'partner', 'category', 'location', 'base_price', 'currency',
            'duration_minutes', 'max_participants', 'requirements_pt',
            'requirements_en', 'cancellation_policy_pt', 'cancellation_policy_en',
            'attributes', 'availability_slots', 'rating', 'review_count',
            'recent_reviews', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_rating(self, obj):
        from bookings.models import Booking
        avg_rating = Booking.objects.filter(
            service=obj,
            status='COMPLETED',
            client_rating__isnull=False
        ).aggregate(avg_rating=Avg('client_rating'))['avg_rating']
        return round(avg_rating, 1) if avg_rating else 0.0
    
    def get_review_count(self, obj):
        from bookings.models import Booking
        return Booking.objects.filter(
            service=obj,
            status='COMPLETED',
            client_rating__isnull=False
        ).count()
    
    def get_recent_reviews(self, obj):
        from bookings.models import Booking
        recent_bookings = Booking.objects.filter(
            service=obj,
            status='COMPLETED',
            client_rating__isnull=False
        ).order_by('-updated_at')[:5]
        
        return [
            {
                'rating': booking.client_rating,
                'comment': booking.client_comment,
                'client_name': booking.client.get_full_name(),
                'date': booking.updated_at
            }
            for booking in recent_bookings
        ]


class ServiceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating services"""
    attribute_values = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Service
        fields = [
            'title_pt', 'title_en', 'description_pt', 'description_en',
            'category', 'location', 'base_price', 'currency',
            'duration_minutes', 'max_participants', 'requirements_pt',
            'requirements_en', 'cancellation_policy_pt', 'cancellation_policy_en',
            'attribute_values'
        ]
    
    def create(self, validated_data):
        attribute_values = validated_data.pop('attribute_values', [])
        service = Service.objects.create(**validated_data)
        
        # Create attribute values
        for attr_data in attribute_values:
            attribute_id = attr_data.get('attribute_id')
            value = attr_data.get('value')
            
            if attribute_id and value:
                try:
                    attribute = ServiceAttribute.objects.get(id=attribute_id)
                    ServiceAttributeValue.objects.create(
                        service=service,
                        attribute=attribute,
                        value=value
                    )
                except ServiceAttribute.DoesNotExist:
                    pass
        
        return service


class ServiceUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating services"""
    attribute_values = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Service
        fields = [
            'title_pt', 'title_en', 'description_pt', 'description_en',
            'category', 'location', 'base_price', 'currency',
            'duration_minutes', 'max_participants', 'requirements_pt',
            'requirements_en', 'cancellation_policy_pt', 'cancellation_policy_en',
            'is_active', 'attribute_values'
        ]
    
    def update(self, instance, validated_data):
        attribute_values = validated_data.pop('attribute_values', None)
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update attribute values if provided
        if attribute_values is not None:
            # Clear existing attribute values
            instance.attributes.all().delete()
            
            # Create new attribute values
            for attr_data in attribute_values:
                attribute_id = attr_data.get('attribute_id')
                value = attr_data.get('value')
                
                if attribute_id and value:
                    try:
                        attribute = ServiceAttribute.objects.get(id=attribute_id)
                        ServiceAttributeValue.objects.create(
                            service=instance,
                            attribute=attribute,
                            value=value
                        )
                    except ServiceAttribute.DoesNotExist:
                        pass
        
        return instance


class ServiceSearchSerializer(serializers.Serializer):
    """Serializer for service search parameters"""
    query = serializers.CharField(required=False, allow_blank=True)
    category = serializers.IntegerField(required=False)
    location = serializers.IntegerField(required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_rating = serializers.FloatField(required=False)
    date = serializers.DateField(required=False)
    time = serializers.TimeField(required=False)
    sort_by = serializers.ChoiceField(
        choices=['price_asc', 'price_desc', 'rating_desc', 'newest', 'distance'],
        default='newest'
    )
    page = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(default=20, min_value=1, max_value=100)
