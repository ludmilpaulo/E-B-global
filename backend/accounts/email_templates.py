"""
Email templates for user notifications
"""

def get_welcome_email_template(user, language='en'):
    """Generate welcome email template"""
    if language == 'pt':
        return {
            'subject': 'Bem-vindo ao E-B Global!',
            'html_content': f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #2563eb; margin: 0;">E-B Global</h1>
                        <p style="color: #666; margin: 5px 0;">Conectando África através da excelência profissional</p>
                    </div>
                    
                    <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h2 style="color: #1e40af; margin-top: 0;">Bem-vindo, {user.first_name}!</h2>
                        <p>Obrigado por se juntar ao E-B Global, a plataforma líder para serviços profissionais em África.</p>
                        
                        <p><strong>Os seus dados de conta:</strong></p>
                        <ul>
                            <li><strong>Email:</strong> {user.email}</li>
                            <li><strong>Tipo de conta:</strong> {user.get_role_display()}</li>
                            <li><strong>Data de registo:</strong> {user.date_joined.strftime('%d/%m/%Y')}</li>
                        </ul>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3 style="color: #1e40af;">Próximos passos:</h3>
                        <ul>
                            <li>Complete o seu perfil</li>
                            <li>Explore os nossos serviços</li>
                            <li>Conecte-se com parceiros verificados</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:3000/dashboard" 
                           style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                            Aceder ao Painel
                        </a>
                    </div>
                    
                    <div style="border-top: 1px solid #e5e7eb; padding-top: 20px; margin-top: 30px; font-size: 14px; color: #666;">
                        <p>Se tiver alguma questão, não hesite em contactar-nos:</p>
                        <p>📧 info@ebglobal.com | 📞 +244 912 345 678</p>
                        <p style="margin-top: 20px;">© 2025 E-B Global. Todos os direitos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
            """,
            'text_content': f"""
            Bem-vindo ao E-B Global, {user.first_name}!
            
            Obrigado por se juntar à nossa plataforma.
            
            Os seus dados de conta:
            - Email: {user.email}
            - Tipo de conta: {user.get_role_display()}
            - Data de registo: {user.date_joined.strftime('%d/%m/%Y')}
            
            Próximos passos:
            - Complete o seu perfil
            - Explore os nossos serviços
            - Conecte-se com parceiros verificados
            
            Aceda ao seu painel: http://localhost:3000/dashboard
            
            Se tiver alguma questão, contacte-nos:
            Email: info@ebglobal.com
            Telefone: +244 912 345 678
            
            © 2025 E-B Global. Todos os direitos reservados.
            """
        }
    else:
        return {
            'subject': 'Welcome to E-B Global!',
            'html_content': f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #2563eb; margin: 0;">E-B Global</h1>
                        <p style="color: #666; margin: 5px 0;">Connecting Africa through professional excellence</p>
                    </div>
                    
                    <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h2 style="color: #1e40af; margin-top: 0;">Welcome, {user.first_name}!</h2>
                        <p>Thank you for joining E-B Global, the leading platform for professional services in Africa.</p>
                        
                        <p><strong>Your account details:</strong></p>
                        <ul>
                            <li><strong>Email:</strong> {user.email}</li>
                            <li><strong>Account Type:</strong> {user.get_role_display()}</li>
                            <li><strong>Registration Date:</strong> {user.date_joined.strftime('%m/%d/%Y')}</li>
                        </ul>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3 style="color: #1e40af;">Next Steps:</h3>
                        <ul>
                            <li>Complete your profile</li>
                            <li>Explore our services</li>
                            <li>Connect with verified partners</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:3000/dashboard" 
                           style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                            Access Dashboard
                        </a>
                    </div>
                    
                    <div style="border-top: 1px solid #e5e7eb; padding-top: 20px; margin-top: 30px; font-size: 14px; color: #666;">
                        <p>If you have any questions, please don't hesitate to contact us:</p>
                        <p>📧 info@ebglobal.com | 📞 +244 912 345 678</p>
                        <p style="margin-top: 20px;">© 2025 E-B Global. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """,
            'text_content': f"""
            Welcome to E-B Global, {user.first_name}!
            
            Thank you for joining our platform.
            
            Your account details:
            - Email: {user.email}
            - Account Type: {user.get_role_display()}
            - Registration Date: {user.date_joined.strftime('%m/%d/%Y')}
            
            Next Steps:
            - Complete your profile
            - Explore our services
            - Connect with verified partners
            
            Access your dashboard: http://localhost:3000/dashboard
            
            If you have any questions, contact us:
            Email: info@ebglobal.com
            Phone: +244 912 345 678
            
            © 2025 E-B Global. All rights reserved.
            """
        }

def get_login_notification_template(user, language='en'):
    """Generate login notification email template"""
    if language == 'pt':
        return {
            'subject': 'Início de sessão no E-B Global',
            'html_content': f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #2563eb; margin: 0;">E-B Global</h1>
                    </div>
                    
                    <div style="background: #f8fafc; padding: 20px; border-radius: 8px;">
                        <h2 style="color: #1e40af; margin-top: 0;">Início de sessão detectado</h2>
                        <p>Olá {user.first_name},</p>
                        <p>Detectámos um novo início de sessão na sua conta E-B Global.</p>
                        
                        <p><strong>Detalhes do início de sessão:</strong></p>
                        <ul>
                            <li><strong>Email:</strong> {user.email}</li>
                            <li><strong>Data e hora:</strong> {user.last_login.strftime('%d/%m/%Y às %H:%M') if user.last_login else 'Agora'}</li>
                        </ul>
                        
                        <p>Se não foi você, por favor altere a sua palavra-passe imediatamente.</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:3000/dashboard" 
                           style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                            Aceder ao Painel
                        </a>
                    </div>
                    
                    <div style="border-top: 1px solid #e5e7eb; padding-top: 20px; font-size: 14px; color: #666;">
                        <p>© 2025 E-B Global. Todos os direitos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
            """,
            'text_content': f"""
            Início de sessão no E-B Global
            
            Olá {user.first_name},
            
            Detectámos um novo início de sessão na sua conta.
            
            Detalhes:
            - Email: {user.email}
            - Data e hora: {user.last_login.strftime('%d/%m/%Y às %H:%M') if user.last_login else 'Agora'}
            
            Se não foi você, altere a sua palavra-passe imediatamente.
            
            © 2025 E-B Global. Todos os direitos reservados.
            """
        }
    else:
        return {
            'subject': 'E-B Global Login Notification',
            'html_content': f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #2563eb; margin: 0;">E-B Global</h1>
                    </div>
                    
                    <div style="background: #f8fafc; padding: 20px; border-radius: 8px;">
                        <h2 style="color: #1e40af; margin-top: 0;">Login Detected</h2>
                        <p>Hello {user.first_name},</p>
                        <p>We detected a new login to your E-B Global account.</p>
                        
                        <p><strong>Login Details:</strong></p>
                        <ul>
                            <li><strong>Email:</strong> {user.email}</li>
                            <li><strong>Date & Time:</strong> {user.last_login.strftime('%m/%d/%Y at %H:%M') if user.last_login else 'Now'}</li>
                        </ul>
                        
                        <p>If this wasn't you, please change your password immediately.</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:3000/dashboard" 
                           style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                            Access Dashboard
                        </a>
                    </div>
                    
                    <div style="border-top: 1px solid #e5e7eb; padding-top: 20px; font-size: 14px; color: #666;">
                        <p>© 2025 E-B Global. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """,
            'text_content': f"""
            E-B Global Login Notification
            
            Hello {user.first_name},
            
            We detected a new login to your account.
            
            Details:
            - Email: {user.email}
            - Date & Time: {user.last_login.strftime('%m/%d/%Y at %H:%M') if user.last_login else 'Now'}
            
            If this wasn't you, please change your password immediately.
            
            © 2025 E-B Global. All rights reserved.
            """
        }

def get_booking_confirmation_template(booking, language='en'):
    """Generate booking confirmation email template"""
    if language == 'pt':
        return {
            'subject': f'Confirmação de Reserva - {booking.booking_number}',
            'html_content': f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #2563eb; margin: 0;">E-B Global</h1>
                    </div>
                    
                    <div style="background: #f8fafc; padding: 20px; border-radius: 8px;">
                        <h2 style="color: #1e40af; margin-top: 0;">Reserva Confirmada!</h2>
                        <p>Olá {booking.client.first_name},</p>
                        <p>A sua reserva foi confirmada com sucesso.</p>
                        
                        <p><strong>Detalhes da Reserva:</strong></p>
                        <ul>
                            <li><strong>Número da Reserva:</strong> {booking.booking_number}</li>
                            <li><strong>Serviço:</strong> {booking.service.name}</li>
                            <li><strong>Parceiro:</strong> {booking.partner.get_full_name()}</li>
                            <li><strong>Data:</strong> {booking.scheduled_start.strftime('%d/%m/%Y')}</li>
                            <li><strong>Hora:</strong> {booking.scheduled_start.strftime('%H:%M')} - {booking.scheduled_end.strftime('%H:%M')}</li>
                            <li><strong>Total:</strong> {booking.total_amount} {booking.service.currency}</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:3000/dashboard" 
                           style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                            Ver Reserva
                        </a>
                    </div>
                    
                    <div style="border-top: 1px solid #e5e7eb; padding-top: 20px; font-size: 14px; color: #666;">
                        <p>© 2025 E-B Global. Todos os direitos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
            """,
            'text_content': f"""
            Confirmação de Reserva - {booking.booking_number}
            
            Olá {booking.client.first_name},
            
            A sua reserva foi confirmada com sucesso.
            
            Detalhes:
            - Número: {booking.booking_number}
            - Serviço: {booking.service.name}
            - Parceiro: {booking.partner.get_full_name()}
            - Data: {booking.scheduled_start.strftime('%d/%m/%Y')}
            - Hora: {booking.scheduled_start.strftime('%H:%M')} - {booking.scheduled_end.strftime('%H:%M')}
            - Total: {booking.total_amount} {booking.service.currency}
            
            © 2025 E-B Global. Todos os direitos reservados.
            """
        }
    else:
        return {
            'subject': f'Booking Confirmation - {booking.booking_number}',
            'html_content': f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #2563eb; margin: 0;">E-B Global</h1>
                    </div>
                    
                    <div style="background: #f8fafc; padding: 20px; border-radius: 8px;">
                        <h2 style="color: #1e40af; margin-top: 0;">Booking Confirmed!</h2>
                        <p>Hello {booking.client.first_name},</p>
                        <p>Your booking has been successfully confirmed.</p>
                        
                        <p><strong>Booking Details:</strong></p>
                        <ul>
                            <li><strong>Booking Number:</strong> {booking.booking_number}</li>
                            <li><strong>Service:</strong> {booking.service.name}</li>
                            <li><strong>Partner:</strong> {booking.partner.get_full_name()}</li>
                            <li><strong>Date:</strong> {booking.scheduled_start.strftime('%m/%d/%Y')}</li>
                            <li><strong>Time:</strong> {booking.scheduled_start.strftime('%H:%M')} - {booking.scheduled_end.strftime('%H:%M')}</li>
                            <li><strong>Total:</strong> {booking.total_amount} {booking.service.currency}</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:3000/dashboard" 
                           style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                            View Booking
                        </a>
                    </div>
                    
                    <div style="border-top: 1px solid #e5e7eb; padding-top: 20px; font-size: 14px; color: #666;">
                        <p>© 2025 E-B Global. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """,
            'text_content': f"""
            Booking Confirmation - {booking.booking_number}
            
            Hello {booking.client.first_name},
            
            Your booking has been successfully confirmed.
            
            Details:
            - Number: {booking.booking_number}
            - Service: {booking.service.name}
            - Partner: {booking.partner.get_full_name()}
            - Date: {booking.scheduled_start.strftime('%m/%d/%Y')}
            - Time: {booking.scheduled_start.strftime('%H:%M')} - {booking.scheduled_end.strftime('%H:%M')}
            - Total: {booking.total_amount} {booking.service.currency}
            
            © 2025 E-B Global. All rights reserved.
            """
        }
