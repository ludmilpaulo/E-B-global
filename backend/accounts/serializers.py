from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, Location, PartnerProfile, UserPreference


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model"""
    
    class Meta:
        model = Location
        fields = ['id', 'name_pt', 'name_en', 'location_type', 'parent', 'is_active']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.UserRole.choices, default=User.UserRole.CLIENT)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'first_name', 'last_name',
            'phone_number', 'role', 'preferred_language'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError('Invalid email or password')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password')


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    location = LocationSerializer(source='preferences.default_province', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'role', 'status', 'preferred_language',
            'profile_picture', 'is_kyc_verified', 'date_joined',
            'last_login', 'location'
        ]
        read_only_fields = [
            'id', 'email', 'role', 'status', 'is_kyc_verified',
            'date_joined', 'last_login'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number',
            'preferred_language', 'profile_picture'
        ]


class PartnerProfileSerializer(serializers.ModelSerializer):
    """Serializer for partner profile"""
    user = UserProfileSerializer(read_only=True)
    service_areas = LocationSerializer(many=True, read_only=True)
    
    class Meta:
        model = PartnerProfile
        fields = [
            'id', 'user', 'business_name', 'business_description',
            'business_license', 'tax_id', 'service_areas', 'is_verified',
            'verification_status', 'rating', 'total_bookings',
            'total_earnings', 'response_time_avg', 'completion_rate',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'is_verified', 'verification_status',
            'rating', 'total_bookings', 'total_earnings',
            'response_time_avg', 'completion_rate', 'created_at', 'updated_at'
        ]


class PartnerProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating partner profile"""
    service_area_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = PartnerProfile
        fields = [
            'business_name', 'business_description', 'business_license',
            'tax_id', 'service_area_ids'
        ]
    
    def update(self, instance, validated_data):
        service_area_ids = validated_data.pop('service_area_ids', None)
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update service areas if provided
        if service_area_ids is not None:
            service_areas = Location.objects.filter(
                id__in=service_area_ids,
                location_type='PROVINCE'
            )
            instance.service_areas.set(service_areas)
        
        instance.save()
        return instance


class UserPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for user preferences"""
    default_country = LocationSerializer(read_only=True)
    default_province = LocationSerializer(read_only=True)
    default_country_id = serializers.IntegerField(write_only=True, required=False)
    default_province_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = UserPreference
        fields = [
            'default_country', 'default_province', 'default_country_id',
            'default_province_id', 'notification_email', 'notification_sms',
            'notification_push', 'marketing_emails'
        ]
    
    def update(self, instance, validated_data):
        default_country_id = validated_data.pop('default_country_id', None)
        default_province_id = validated_data.pop('default_province_id', None)
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update location preferences
        if default_country_id:
            try:
                country = Location.objects.get(
                    id=default_country_id,
                    location_type='COUNTRY'
                )
                instance.default_country = country
            except Location.DoesNotExist:
                raise serializers.ValidationError('Invalid country ID')
        
        if default_province_id:
            try:
                province = Location.objects.get(
                    id=default_province_id,
                    location_type='PROVINCE'
                )
                instance.default_province = province
            except Location.DoesNotExist:
                raise serializers.ValidationError('Invalid province ID')
        
        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect')
        return value
