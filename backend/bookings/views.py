from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.core.paginator import Paginator
from django.db import transaction
from .models import (
    Booking, BookingStatusHistory, BookingMessage, BookingDocument,
    BookingDispute, RecurringBooking
)
from .serializers import (
    BookingListSerializer, BookingDetailSerializer, BookingCreateSerializer,
    BookingUpdateSerializer, BookingStatusUpdateSerializer,
    BookingMessageSerializer, BookingDocumentSerializer, BookingDisputeSerializer,
    RecurringBookingSerializer, BookingSearchSerializer
)


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for bookings"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter bookings based on user role"""
        user = self.request.user
        
        if user.role == 'ADMIN' or user.role == 'STAFF':
            # Admin and staff can see all bookings
            queryset = Booking.objects.all()
        elif user.role == 'PARTNER':
            # Partners can see their own bookings
            queryset = Booking.objects.filter(partner=user)
        else:
            # Clients can see their own bookings
            queryset = Booking.objects.filter(client=user)
        
        return queryset.select_related(
            'client', 'partner', 'service', 'location'
        ).prefetch_related(
            'status_history', 'messages', 'documents', 'disputes'
        )
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BookingListSerializer
        elif self.action == 'create':
            return BookingCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BookingUpdateSerializer
        else:
            return BookingDetailSerializer
    
    def perform_create(self, serializer):
        """Create booking with proper context"""
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update booking status with validation"""
        booking = self.get_object()
        serializer = BookingStatusUpdateSerializer(
            data=request.data,
            context={'booking': booking, 'request': request}
        )
        
        if serializer.is_valid():
            old_status = booking.status
            new_status = serializer.validated_data['status']
            notes = serializer.validated_data.get('notes', '')
            
            # Update booking status
            booking.status = new_status
            booking.save()
            
            # Create status history entry
            BookingStatusHistory.objects.create(
                booking=booking,
                status=new_status,
                notes=notes or f"Status changed from {old_status} to {new_status}",
                created_by=request.user
            )
            
            return Response({
                'message': 'Booking status updated successfully',
                'booking': BookingDetailSerializer(booking).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send message in booking chat"""
        booking = self.get_object()
        
        # Verify user is part of the booking
        if request.user not in [booking.client, booking.partner]:
            return Response(
                {'error': 'You are not authorized to send messages for this booking'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = BookingMessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(
                booking=booking,
                sender=request.user
            )
            
            return Response({
                'message': 'Message sent successfully',
                'data': BookingMessageSerializer(message).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def upload_document(self, request, pk=None):
        """Upload document for booking"""
        booking = self.get_object()
        
        # Verify user is part of the booking
        if request.user not in [booking.client, booking.partner]:
            return Response(
                {'error': 'You are not authorized to upload documents for this booking'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = BookingDocumentSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save(
                booking=booking,
                uploaded_by=request.user
            )
            
            return Response({
                'message': 'Document uploaded successfully',
                'data': BookingDocumentSerializer(document).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def create_dispute(self, request, pk=None):
        """Create dispute for booking"""
        booking = self.get_object()
        
        # Only client or partner can create disputes
        if request.user not in [booking.client, booking.partner]:
            return Response(
                {'error': 'You are not authorized to create disputes for this booking'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = BookingDisputeSerializer(data=request.data)
        if serializer.is_valid():
            dispute = serializer.save(
                booking=booking,
                created_by=request.user
            )
            
            # Update booking status to disputed
            booking.status = 'DISPUTED'
            booking.save()
            
            # Create status history
            BookingStatusHistory.objects.create(
                booking=booking,
                status='DISPUTED',
                notes=f'Dispute created: {dispute.description}',
                created_by=request.user
            )
            
            return Response({
                'message': 'Dispute created successfully',
                'data': BookingDisputeSerializer(dispute).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def rate_service(self, request, pk=None):
        """Rate the service after completion"""
        booking = self.get_object()
        
        # Only client can rate the service
        if request.user != booking.client:
            return Response(
                {'error': 'Only the client can rate the service'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Only completed bookings can be rated
        if booking.status != 'COMPLETED':
            return Response(
                {'error': 'Only completed bookings can be rated'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')
        
        if not rating or not (1 <= int(rating) <= 5):
            return Response(
                {'error': 'Rating must be between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.client_rating = int(rating)
        booking.client_comment = comment
        booking.save()
        
        return Response({
            'message': 'Service rated successfully',
            'booking': BookingDetailSerializer(booking).data
        })
    
    @action(detail=True, methods=['post'])
    def rate_client(self, request, pk=None):
        """Rate the client after completion"""
        booking = self.get_object()
        
        # Only partner can rate the client
        if request.user != booking.partner:
            return Response(
                {'error': 'Only the partner can rate the client'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Only completed bookings can be rated
        if booking.status != 'COMPLETED':
            return Response(
                {'error': 'Only completed bookings can be rated'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')
        
        if not rating or not (1 <= int(rating) <= 5):
            return Response(
                {'error': 'Rating must be between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.partner_rating = int(rating)
        booking.partner_comment = comment
        booking.save()
        
        return Response({
            'message': 'Client rated successfully',
            'booking': BookingDetailSerializer(booking).data
        })


class BookingSearchView(APIView):
    """Advanced booking search endpoint"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = BookingSearchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        user = request.user
        
        # Build queryset based on user role
        if user.role == 'ADMIN' or user.role == 'STAFF':
            queryset = Booking.objects.all()
        elif user.role == 'PARTNER':
            queryset = Booking.objects.filter(partner=user)
        else:
            queryset = Booking.objects.filter(client=user)
        
        # Apply filters
        if data.get('status'):
            queryset = queryset.filter(status=data['status'])
        
        if data.get('date_from'):
            queryset = queryset.filter(scheduled_start__date__gte=data['date_from'])
        
        if data.get('date_to'):
            queryset = queryset.filter(scheduled_start__date__lte=data['date_to'])
        
        if data.get('partner_id'):
            queryset = queryset.filter(partner_id=data['partner_id'])
        
        if data.get('client_id'):
            queryset = queryset.filter(client_id=data['client_id'])
        
        if data.get('service_id'):
            queryset = queryset.filter(service_id=data['service_id'])
        
        if data.get('location_id'):
            queryset = queryset.filter(location_id=data['location_id'])
        
        # Apply sorting
        sort_by = data.get('sort_by', 'date_desc')
        if sort_by == 'date_asc':
            queryset = queryset.order_by('scheduled_start')
        elif sort_by == 'date_desc':
            queryset = queryset.order_by('-scheduled_start')
        elif sort_by == 'amount_asc':
            queryset = queryset.order_by('total_amount')
        elif sort_by == 'amount_desc':
            queryset = queryset.order_by('-total_amount')
        elif sort_by == 'status':
            queryset = queryset.order_by('status')
        
        # Pagination
        page = data.get('page', 1)
        page_size = data.get('page_size', 20)
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = BookingListSerializer(page_obj, many=True)
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'filters_applied': data
        })


class BookingStatsView(APIView):
    """Booking statistics endpoint"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Build queryset based on user role
        if user.role == 'ADMIN' or user.role == 'STAFF':
            queryset = Booking.objects.all()
        elif user.role == 'PARTNER':
            queryset = Booking.objects.filter(partner=user)
        else:
            queryset = Booking.objects.filter(client=user)
        
        # Calculate statistics
        total_bookings = queryset.count()
        pending_bookings = queryset.filter(status='PENDING').count()
        confirmed_bookings = queryset.filter(status='CONFIRMED').count()
        completed_bookings = queryset.filter(status='COMPLETED').count()
        cancelled_bookings = queryset.filter(status='CANCELLED').count()
        
        # Calculate average rating
        avg_rating = queryset.filter(
            status='COMPLETED',
            client_rating__isnull=False
        ).aggregate(avg_rating=Avg('client_rating'))['avg_rating']
        
        # Calculate total revenue (for partners)
        total_revenue = 0
        if user.role == 'PARTNER':
            total_revenue = queryset.filter(
                status='COMPLETED'
            ).aggregate(total=models.Sum('total_amount'))['total'] or 0
        
        return Response({
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'confirmed_bookings': confirmed_bookings,
            'completed_bookings': completed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'average_rating': round(avg_rating, 1) if avg_rating else 0.0,
            'total_revenue': float(total_revenue),
            'completion_rate': round(
                (completed_bookings / total_bookings * 100) if total_bookings > 0 else 0, 1
            )
        })


class BookingCalendarView(APIView):
    """Booking calendar view for partners"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.role not in ['PARTNER', 'ADMIN', 'STAFF']:
            return Response(
                {'error': 'Only partners can view booking calendar'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get date range
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'start_date and end_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Build queryset
        if user.role == 'PARTNER':
            queryset = Booking.objects.filter(partner=user)
        else:
            queryset = Booking.objects.all()
        
        queryset = queryset.filter(
            scheduled_start__date__gte=start_date,
            scheduled_start__date__lte=end_date
        ).order_by('scheduled_start')
        
        serializer = BookingListSerializer(queryset, many=True)
        return Response(serializer.data)