from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Location, UserPreference
from services.models import ServiceCategory, Service, ServiceAttribute
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data for development'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create locations
        self.create_locations()
        
        # Create service categories
        self.create_service_categories()
        
        # Create sample users
        self.create_sample_users()
        
        # Create sample services
        self.create_sample_services()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )

    def create_locations(self):
        """Create sample locations"""
        self.stdout.write('Creating locations...')
        
        # Countries
        angola = Location.objects.create(
            name_pt='Angola',
            name_en='Angola',
            location_type='COUNTRY',
            is_active=True
        )
        
        mozambique = Location.objects.create(
            name_pt='Moçambique',
            name_en='Mozambique',
            location_type='COUNTRY',
            is_active=True
        )
        
        # Provinces for Angola
        luanda = Location.objects.create(
            name_pt='Luanda',
            name_en='Luanda',
            location_type='PROVINCE',
            parent=angola,
            is_active=True
        )
        
        huila = Location.objects.create(
            name_pt='Huíla',
            name_en='Huila',
            location_type='PROVINCE',
            parent=angola,
            is_active=True
        )
        
        # Provinces for Mozambique
        maputo = Location.objects.create(
            name_pt='Maputo',
            name_en='Maputo',
            location_type='PROVINCE',
            parent=mozambique,
            is_active=True
        )
        
        # Cities
        Location.objects.create(
            name_pt='Luanda',
            name_en='Luanda',
            location_type='CITY',
            parent=luanda,
            is_active=True
        )
        
        Location.objects.create(
            name_pt='Lubango',
            name_en='Lubango',
            location_type='CITY',
            parent=huila,
            is_active=True
        )
        
        Location.objects.create(
            name_pt='Maputo',
            name_en='Maputo',
            location_type='CITY',
            parent=maputo,
            is_active=True
        )

    def create_service_categories(self):
        """Create service categories"""
        self.stdout.write('Creating service categories...')
        
        categories_data = [
            {
                'name_pt': 'Consultoria Imobiliária',
                'name_en': 'Real Estate Consulting',
                'description_pt': 'Serviços de consultoria imobiliária e gestão de propriedades',
                'description_en': 'Real estate consulting and property management services',
                'icon': 'business',
                'color': '#3B82F6'
            },
            {
                'name_pt': 'Transportes',
                'name_en': 'Transportation',
                'description_pt': 'Serviços de transporte, transferências e aluguer de viaturas',
                'description_en': 'Transportation, transfers and vehicle rental services',
                'icon': 'car',
                'color': '#10B981'
            },
            {
                'name_pt': 'Consultoria de Negócios',
                'name_en': 'Business Consulting',
                'description_pt': 'Consultoria empresarial e gestão de negócios',
                'description_en': 'Business consulting and management services',
                'icon': 'briefcase',
                'color': '#8B5CF6'
            },
            {
                'name_pt': 'Serviços Jurídicos',
                'name_en': 'Legal Services',
                'description_pt': 'Serviços jurídicos e consultoria legal',
                'description_en': 'Legal services and legal consulting',
                'icon': 'scale',
                'color': '#EF4444'
            },
            {
                'name_pt': 'Serviços Linguísticos',
                'name_en': 'Language Services',
                'description_pt': 'Tradução, interpretação e aulas de línguas',
                'description_en': 'Translation, interpretation and language lessons',
                'icon': 'language',
                'color': '#F59E0B'
            },
            {
                'name_pt': 'Reconhecimento de Documentos',
                'name_en': 'Document Recognition',
                'description_pt': 'Notário, MIREX, Embaixadas e reconhecimento de documentos',
                'description_en': 'Notary, MIREX, Embassies and document recognition',
                'icon': 'document-text',
                'color': '#6366F1'
            },
            {
                'name_pt': 'Catering Corporativo',
                'name_en': 'Corporate Catering',
                'description_pt': 'Serviços de catering para eventos corporativos',
                'description_en': 'Catering services for corporate events',
                'icon': 'restaurant',
                'color': '#F97316'
            },
            {
                'name_pt': 'Protocolo',
                'name_en': 'Protocol',
                'description_pt': 'Serviços de protocolo e organização de eventos',
                'description_en': 'Protocol services and event organization',
                'icon': 'ribbon',
                'color': '#EC4899'
            }
        ]
        
        for category_data in categories_data:
            ServiceCategory.objects.create(**category_data)

    def create_sample_users(self):
        """Create sample users"""
        self.stdout.write('Creating sample users...')
        
        # Admin user
        admin_user = User.objects.create_user(
            email='admin@ebglobal.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            role=User.UserRole.ADMIN,
            phone_number='+244900000000'
        )
        UserPreference.objects.create(user=admin_user)
        
        # Partner users
        partner1 = User.objects.create_user(
            email='partner1@ebglobal.com',
            password='partner123',
            first_name='João',
            last_name='Silva',
            role=User.UserRole.PARTNER,
            phone_number='+244900000001'
        )
        UserPreference.objects.create(user=partner1)
        
        partner2 = User.objects.create_user(
            email='partner2@ebglobal.com',
            password='partner123',
            first_name='Maria',
            last_name='Santos',
            role=User.UserRole.PARTNER,
            phone_number='+258900000002'
        )
        UserPreference.objects.create(user=partner2)
        
        # Client users
        client1 = User.objects.create_user(
            email='client1@ebglobal.com',
            password='client123',
            first_name='Carlos',
            last_name='Ferreira',
            role=User.UserRole.CLIENT,
            phone_number='+244900000003'
        )
        UserPreference.objects.create(user=client1)
        
        client2 = User.objects.create_user(
            email='client2@ebglobal.com',
            password='client123',
            first_name='Ana',
            last_name='Costa',
            role=User.UserRole.CLIENT,
            phone_number='+258900000004'
        )
        UserPreference.objects.create(user=client2)

    def create_sample_services(self):
        """Create sample services"""
        self.stdout.write('Creating sample services...')
        
        # Get locations and categories
        luanda = Location.objects.get(name_pt='Luanda', location_type='PROVINCE')
        maputo = Location.objects.get(name_pt='Maputo', location_type='PROVINCE')
        
        real_estate = ServiceCategory.objects.get(name_en='Real Estate Consulting')
        transport = ServiceCategory.objects.get(name_en='Transportation')
        business = ServiceCategory.objects.get(name_en='Business Consulting')
        
        partner1 = User.objects.get(email='partner1@ebglobal.com')
        partner2 = User.objects.get(email='partner2@ebglobal.com')
        
        # Sample services
        services_data = [
            {
                'title_pt': 'Consultoria Imobiliária em Luanda',
                'title_en': 'Real Estate Consulting in Luanda',
                'description_pt': 'Consultoria especializada em imóveis residenciais e comerciais em Luanda',
                'description_en': 'Specialized consulting for residential and commercial properties in Luanda',
                'partner': partner1,
                'category': real_estate,
                'location': luanda,
                'base_price': 50000.00,
                'currency': 'AOA',
                'duration_minutes': 90
            },
            {
                'title_pt': 'Serviço de Transporte Executivo',
                'title_en': 'Executive Transportation Service',
                'description_pt': 'Transporte executivo com motorista profissional em Maputo',
                'description_en': 'Executive transportation with professional driver in Maputo',
                'partner': partner2,
                'category': transport,
                'location': maputo,
                'base_price': 2500.00,
                'currency': 'MZN',
                'duration_minutes': 90
            },
            {
                'title_pt': 'Consultoria de Negócios',
                'title_en': 'Business Consulting',
                'description_pt': 'Consultoria para startups e pequenas empresas',
                'description_en': 'Consulting for startups and small businesses',
                'partner': partner1,
                'category': business,
                'location': luanda,
                'base_price': 75000.00,
                'currency': 'AOA',
                'duration_minutes': 90
            }
        ]
        
        for service_data in services_data:
            service = Service.objects.create(**service_data)
            
            # Create some availability slots for the next 7 days
            for i in range(7):
                date = timezone.now().date() + timedelta(days=i)
                
                # Create morning slot (9:00-10:30)
                morning_start = timezone.datetime.combine(date, timezone.time(9, 0))
                morning_end = timezone.datetime.combine(date, timezone.time(10, 30))
                
                # Create afternoon slot (14:00-15:30)
                afternoon_start = timezone.datetime.combine(date, timezone.time(14, 0))
                afternoon_end = timezone.datetime.combine(date, timezone.time(15, 30))
                
                # Create evening slot (17:00-18:30)
                evening_start = timezone.datetime.combine(date, timezone.time(17, 0))
                evening_end = timezone.datetime.combine(date, timezone.time(18, 30))
                
                # Create slots
                from services.models import AvailabilitySlot
                AvailabilitySlot.objects.create(
                    service=service,
                    start_time=morning_start,
                    end_time=morning_end,
                    is_available=True
                )
                
                AvailabilitySlot.objects.create(
                    service=service,
                    start_time=afternoon_start,
                    end_time=afternoon_end,
                    is_available=True
                )
                
                AvailabilitySlot.objects.create(
                    service=service,
                    start_time=evening_start,
                    end_time=evening_end,
                    is_available=True
                )
