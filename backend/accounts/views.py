from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Location, PartnerProfile, UserPreference
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserUpdateSerializer, PartnerProfileSerializer, PartnerProfileUpdateSerializer,
    UserPreferenceSerializer, PasswordChangeSerializer, LocationSerializer
)


class I18nView(APIView):
    """API-driven internationalization endpoint"""
    
    def get(self, request, language):
        """Return translations for the specified language"""
        
        # Default translations for English
        en_translations = {
            "common": {
                "loading": "Loading...",
                "error": "Error",
                "success": "Success",
                "cancel": "Cancel",
                "save": "Save",
                "edit": "Edit",
                "delete": "Delete",
                "confirm": "Confirm",
                "back": "Back",
                "next": "Next",
                "previous": "Previous",
                "search": "Search",
                "filter": "Filter",
                "sort": "Sort",
                "view": "View",
                "close": "Close",
                "yes": "Yes",
                "no": "No"
            },
            "navigation": {
                "home": "Home",
                "services": "Services",
                "bookings": "Bookings",
                "profile": "Profile",
                "settings": "Settings",
                "help": "Help",
                "contact": "Contact",
                "about": "About"
            },
            "auth": {
                "login": "Login",
                "logout": "Logout",
                "register": "Register",
                "email": "Email",
                "password": "Password",
                "confirm_password": "Confirm Password",
                "forgot_password": "Forgot Password?",
                "remember_me": "Remember Me",
                "sign_in": "Sign In",
                "sign_up": "Sign Up",
                "create_account": "Create Account"
            },
            "services": {
                "categories": "Service Categories",
                "imobiliaria": "Real Estate Consulting",
                "transportes": "Transportation Services",
                "negocios": "Business Consulting",
                "juridica": "Legal Services",
                "linguistica": "Language Services",
                "documentos": "Document Recognition",
                "catering": "Corporate Catering",
                "protocolo": "Protocol Services",
                "book_now": "Book Now",
                "view_details": "View Details",
                "price": "Price",
                "duration": "Duration",
                "location": "Location",
                "rating": "Rating",
                "reviews": "Reviews"
            },
            "booking": {
                "select_date": "Select Date",
                "select_time": "Select Time",
                "special_requirements": "Special Requirements",
                "book_service": "Book Service",
                "booking_summary": "Booking Summary",
                "total_amount": "Total Amount",
                "payment_method": "Payment Method",
                "confirm_booking": "Confirm Booking",
                "booking_confirmed": "Booking Confirmed"
            },
            "profile": {
                "personal_info": "Personal Information",
                "business_info": "Business Information",
                "contact_info": "Contact Information",
                "preferences": "Preferences",
                "notifications": "Notifications",
                "security": "Security",
                "privacy": "Privacy"
            }
        }
        
        # Portuguese translations
        pt_translations = {
            "common": {
                "loading": "A carregar...",
                "error": "Erro",
                "success": "Sucesso",
                "cancel": "Cancelar",
                "save": "Guardar",
                "edit": "Editar",
                "delete": "Eliminar",
                "confirm": "Confirmar",
                "back": "Voltar",
                "next": "Seguinte",
                "previous": "Anterior",
                "search": "Pesquisar",
                "filter": "Filtrar",
                "sort": "Ordenar",
                "view": "Ver",
                "close": "Fechar",
                "yes": "Sim",
                "no": "Não"
            },
            "navigation": {
                "home": "Início",
                "services": "Serviços",
                "bookings": "Reservas",
                "profile": "Perfil",
                "settings": "Configurações",
                "help": "Ajuda",
                "contact": "Contacto",
                "about": "Sobre"
            },
            "auth": {
                "login": "Entrar",
                "logout": "Sair",
                "register": "Registar",
                "email": "Email",
                "password": "Palavra-passe",
                "confirm_password": "Confirmar Palavra-passe",
                "forgot_password": "Esqueceu-se da palavra-passe?",
                "remember_me": "Lembrar-me",
                "sign_in": "Entrar",
                "sign_up": "Registar",
                "create_account": "Criar Conta"
            },
            "services": {
                "categories": "Categorias de Serviços",
                "imobiliaria": "Consultoria Imobiliária",
                "transportes": "Serviços de Transporte",
                "negocios": "Consultoria de Negócios",
                "juridica": "Serviços Jurídicos",
                "linguistica": "Serviços Linguísticos",
                "documentos": "Reconhecimento de Documentos",
                "catering": "Catering Corporativo",
                "protocolo": "Serviços de Protocolo",
                "book_now": "Reservar Agora",
                "view_details": "Ver Detalhes",
                "price": "Preço",
                "duration": "Duração",
                "location": "Localização",
                "rating": "Avaliação",
                "reviews": "Avaliações"
            },
            "booking": {
                "select_date": "Selecionar Data",
                "select_time": "Selecionar Hora",
                "special_requirements": "Requisitos Especiais",
                "book_service": "Reservar Serviço",
                "booking_summary": "Resumo da Reserva",
                "total_amount": "Valor Total",
                "payment_method": "Método de Pagamento",
                "confirm_booking": "Confirmar Reserva",
                "booking_confirmed": "Reserva Confirmada"
            },
            "profile": {
                "personal_info": "Informações Pessoais",
                "business_info": "Informações do Negócio",
                "contact_info": "Informações de Contacto",
                "preferences": "Preferências",
                "notifications": "Notificações",
                "security": "Segurança",
                "privacy": "Privacidade"
            }
        }
        
        # Return translations based on language
        if language == 'pt':
            return Response(pt_translations)
        else:
            return Response(en_translations)


class UserRegistrationView(APIView):
    """User registration endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create user preferences
            UserPreference.objects.create(user=user)
            
            # Create partner profile if role is PARTNER
            if user.role == User.UserRole.PARTNER:
                PartnerProfile.objects.create(user=user)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """User profile management"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': UserProfileSerializer(request.user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnerProfileView(APIView):
    """Partner profile management"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            partner_profile = request.user.partner_profile
            serializer = PartnerProfileSerializer(partner_profile)
            return Response(serializer.data)
        except PartnerProfile.DoesNotExist:
            return Response(
                {'error': 'Partner profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request):
        try:
            partner_profile = request.user.partner_profile
            serializer = PartnerProfileUpdateSerializer(
                partner_profile, 
                data=request.data, 
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Partner profile updated successfully',
                    'profile': PartnerProfileSerializer(partner_profile).data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PartnerProfile.DoesNotExist:
            return Response(
                {'error': 'Partner profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class UserPreferencesView(APIView):
    """User preferences management"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        preferences, created = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(preferences)
        return Response(serializer.data)
    
    def put(self, request):
        preferences, created = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(preferences, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Preferences updated successfully',
                'preferences': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    """Password change endpoint"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationListView(APIView):
    """List locations for dropdowns"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        location_type = request.query_params.get('type', None)
        parent_id = request.query_params.get('parent', None)
        
        queryset = Location.objects.filter(is_active=True)
        
        if location_type:
            queryset = queryset.filter(location_type=location_type)
        
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logout endpoint"""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Logout successful'})
    except Exception as e:
        return Response(
            {'error': 'Invalid token'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
