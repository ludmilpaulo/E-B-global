"""
Notification service for sending emails and push notifications
"""

import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .email_templates import get_welcome_email_template, get_login_notification_template, get_booking_confirmation_template

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for handling all types of notifications"""
    
    @staticmethod
    def send_welcome_email(user):
        """Send welcome email to new user"""
        try:
            language = user.preferred_language or 'en'
            template = get_welcome_email_template(user, language)
            
            send_mail(
                subject=template['subject'],
                message=template['text_content'],
                html_message=template['html_content'],
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            logger.info(f"Welcome email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_login_notification(user):
        """Send login notification email"""
        try:
            language = user.preferred_language or 'en'
            template = get_login_notification_template(user, language)
            
            send_mail(
                subject=template['subject'],
                message=template['text_content'],
                html_message=template['html_content'],
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            logger.info(f"Login notification sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send login notification to {user.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_booking_confirmation(booking):
        """Send booking confirmation email"""
        try:
            language = booking.client.preferred_language or 'en'
            template = get_booking_confirmation_template(booking, language)
            
            send_mail(
                subject=template['subject'],
                message=template['text_content'],
                html_message=template['html_content'],
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.client.email],
                fail_silently=False,
            )
            
            logger.info(f"Booking confirmation sent to {booking.client.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send booking confirmation to {booking.client.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_partner_notification(booking):
        """Send notification to partner about new booking"""
        try:
            language = booking.partner.preferred_language or 'en'
            
            if language == 'pt':
                subject = f'Nova Reserva Recebida - {booking.booking_number}'
                message = f"""
                Olá {booking.partner.first_name},
                
                Recebeu uma nova reserva!
                
                Detalhes:
                - Número: {booking.booking_number}
                - Cliente: {booking.client.get_full_name()}
                - Serviço: {booking.service.name}
                - Data: {booking.scheduled_start.strftime('%d/%m/%Y')}
                - Hora: {booking.scheduled_start.strftime('%H:%M')} - {booking.scheduled_end.strftime('%H:%M')}
                - Total: {booking.total_amount} {booking.service.currency}
                
                Aceda ao seu painel para mais detalhes.
                """
            else:
                subject = f'New Booking Received - {booking.booking_number}'
                message = f"""
                Hello {booking.partner.first_name},
                
                You have received a new booking!
                
                Details:
                - Number: {booking.booking_number}
                - Client: {booking.client.get_full_name()}
                - Service: {booking.service.name}
                - Date: {booking.scheduled_start.strftime('%m/%d/%Y')}
                - Time: {booking.scheduled_start.strftime('%H:%M')} - {booking.scheduled_end.strftime('%H:%M')}
                - Total: {booking.total_amount} {booking.service.currency}
                
                Access your dashboard for more details.
                """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.partner.email],
                fail_silently=False,
            )
            
            logger.info(f"Partner notification sent to {booking.partner.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send partner notification to {booking.partner.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_password_reset_email(user, reset_token):
        """Send password reset email"""
        try:
            language = user.preferred_language or 'en'
            
            if language == 'pt':
                subject = 'Redefinir Palavra-passe - E-B Global'
                message = f"""
                Olá {user.first_name},
                
                Recebeu este email porque solicitou a redefinição da sua palavra-passe.
                
                Use o seguinte código para redefinir a sua palavra-passe:
                {reset_token}
                
                Este código expira em 1 hora.
                
                Se não solicitou esta redefinição, ignore este email.
                """
            else:
                subject = 'Password Reset - E-B Global'
                message = f"""
                Hello {user.first_name},
                
                You received this email because you requested a password reset.
                
                Use the following code to reset your password:
                {reset_token}
                
                This code expires in 1 hour.
                
                If you didn't request this reset, please ignore this email.
                """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            logger.info(f"Password reset email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user.email}: {str(e)}")
            return False
