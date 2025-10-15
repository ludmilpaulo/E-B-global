from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse


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
