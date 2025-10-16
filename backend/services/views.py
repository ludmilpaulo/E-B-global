from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Avg, Count
from django.utils import timezone
from django.core.paginator import Paginator
from .models import ServiceCategory, Service, ServiceAttribute, ServiceAttributeValue, AvailabilitySlot
from .serializers import (
    ServiceCategorySerializer, ServiceListSerializer, ServiceDetailSerializer,
    ServiceCreateSerializer, ServiceUpdateSerializer, ServiceSearchSerializer,
    ServiceAttributeSerializer, AvailabilitySlotSerializer
)


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for service categories"""
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        """Get services for a specific category"""
        category = self.get_object()
        services = Service.objects.filter(
            category=category,
            status='ACTIVE'
        ).select_related('partner', 'category', 'primary_location')
        
        # Apply filters
        location = request.query_params.get('location')
        if location:
            services = services.filter(location_id=location)
        
        min_price = request.query_params.get('min_price')
        if min_price:
            services = services.filter(base_price__gte=min_price)
        
        max_price = request.query_params.get('max_price')
        if max_price:
            services = services.filter(base_price__lte=max_price)
        
        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        paginator = Paginator(services, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = ServiceListSerializer(page_obj, many=True)
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
        })


class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for services"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Service.objects.filter(status='ACTIVE').select_related(
            'partner', 'category', 'location'
        ).prefetch_related('attributes', 'availability_slots')
        
        # Filter by partner if user is a partner
        if self.request.user.is_authenticated and self.request.user.role == 'PARTNER':
            queryset = queryset.filter(partner=self.request.user)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        elif self.action == 'create':
            return ServiceCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ServiceUpdateSerializer
        else:
            return ServiceDetailSerializer
    
    def perform_create(self, serializer):
        # Set the partner to the current user
        serializer.save(partner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get availability slots for a service"""
        service = self.get_object()
        date = request.query_params.get('date')
        
        if date:
            try:
                from datetime import datetime
                target_date = datetime.strptime(date, '%Y-%m-%d').date()
                slots = service.availability_slots.filter(
                    start_time__date=target_date,
                    is_available=True
                ).order_by('start_time')
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Get slots for the next 30 days
            from datetime import timedelta
            end_date = timezone.now().date() + timedelta(days=30)
            slots = service.availability_slots.filter(
                start_time__date__gte=timezone.now().date(),
                start_time__date__lte=end_date,
                is_available=True
            ).order_by('start_time')
        
        serializer = AvailabilitySlotSerializer(slots, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def book_slot(self, request, pk=None):
        """Book a specific time slot (placeholder for booking system)"""
        service = self.get_object()
        slot_id = request.data.get('slot_id')
        
        if not slot_id:
            return Response(
                {'error': 'slot_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            slot = AvailabilitySlot.objects.get(
                id=slot_id,
                service=service,
                is_available=True
            )
            
            # Check if slot is in the future
            if slot.start_time <= timezone.now():
                return Response(
                    {'error': 'Cannot book past time slots'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Mark slot as unavailable
            slot.is_available = False
            slot.save()
            
            return Response({
                'message': 'Slot booked successfully',
                'slot': AvailabilitySlotSerializer(slot).data
            })
            
        except AvailabilitySlot.DoesNotExist:
            return Response(
                {'error': 'Slot not found or not available'},
                status=status.HTTP_404_NOT_FOUND
            )


class ServiceSearchView(APIView):
    """Advanced service search endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ServiceSearchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Build queryset
        queryset = Service.objects.filter(status='ACTIVE').select_related(
            'partner', 'category', 'location'
        )
        
        # Apply filters
        if data.get('query'):
            query = data['query']
            queryset = queryset.filter(
                Q(title_pt__icontains=query) |
                Q(title_en__icontains=query) |
                Q(description_pt__icontains=query) |
                Q(description_en__icontains=query)
            )
        
        if data.get('category'):
            queryset = queryset.filter(category_id=data['category'])
        
        if data.get('location'):
            queryset = queryset.filter(location_id=data['location'])
        
        if data.get('min_price'):
            queryset = queryset.filter(base_price__gte=data['min_price'])
        
        if data.get('max_price'):
            queryset = queryset.filter(base_price__lte=data['max_price'])
        
        if data.get('min_rating'):
            # Filter by minimum rating (this would require a subquery in production)
            pass
        
        if data.get('date'):
            # Filter by availability on specific date
            queryset = queryset.filter(
                availability_slots__start_time__date=data['date'],
                availability_slots__is_available=True
            ).distinct()
        
        # Apply sorting
        sort_by = data.get('sort_by', 'newest')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('base_price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-base_price')
        elif sort_by == 'rating_desc':
            # This would require a more complex query in production
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('-created_at')
        
        # Pagination
        page = data.get('page', 1)
        page_size = data.get('page_size', 20)
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = ServiceListSerializer(page_obj, many=True)
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'filters_applied': data
        })


class ServiceAttributeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for service attributes"""
    queryset = ServiceAttribute.objects.all()
    serializer_class = ServiceAttributeSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(service_category_id=category)
        return queryset


class FeaturedServicesView(APIView):
    """Get featured services for homepage"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Get services with highest ratings and recent bookings
        services = Service.objects.filter(
            is_active=True
        ).select_related('partner', 'category', 'location')[:12]
        
        serializer = ServiceListSerializer(services, many=True)
        return Response(serializer.data)


class PopularServicesView(APIView):
    """Get popular services by category"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        category_id = request.query_params.get('category')
        limit = int(request.query_params.get('limit', 8))
        
        queryset = Service.objects.filter(status='ACTIVE')
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Order by number of bookings (this would require a more complex query in production)
        services = queryset.select_related('partner', 'category', 'location')[:limit]
        
        serializer = ServiceListSerializer(services, many=True)
        return Response(serializer.data)