# E-B Global - Multi-Service Marketplace

A comprehensive marketplace platform connecting clients with professional service providers across Lusophone and Anglophone Africa.

## 🌟 Features

- **Multi-Service Platform**: Real Estate, Transportation, Business Consulting, Legal Services, Language Services, Document Recognition, Corporate Catering, and Protocol Services
- **90-Minute Booking Slots**: Standardized service duration for better scheduling
- **Multi-Language Support**: Portuguese and English with auto-detection
- **Location-Based Services**: Auto-detection of user location and language
- **Professional UI/UX**: Modern, responsive design across all platforms
- **Comprehensive Admin Dashboard**: Analytics, partner management, and platform oversight
- **Secure Payment Integration**: Stripe integration with invoice generation
- **Real-time Notifications**: WhatsApp, Email, and Push notifications
- **Advanced Analytics**: Performance metrics and business intelligence

## 🏗️ Technology Stack

### Backend
- **Django 5** with Django REST Framework
- **PostgreSQL** database with optimized queries
- **Redis** for caching and session management
- **Celery** for background tasks and notifications
- **JWT Authentication** with refresh token rotation
- **OpenAPI Documentation** with drf-spectacular
- **AWS S3** for file storage
- **SendGrid** for email services

### Web Frontend
- **Next.js 15** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** with shadcn/ui components
- **Redux Toolkit** with RTK Query for state management
- **Responsive Design** with mobile-first approach

### Mobile App
- **Expo React Native** with TypeScript
- **Expo Router** for navigation
- **Redux Toolkit** for state management
- **Native notifications** and location services
- **Cross-platform compatibility** (iOS/Android)

### DevOps & Infrastructure
- **Docker** and Docker Compose for containerization
- **Nginx** for reverse proxy and load balancing
- **GitHub Actions** for CI/CD
- **Sentry** for error monitoring
- **Cloudflare** for CDN and security
- **SSL/TLS** encryption

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd E-B-global

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

This will start:
- **Backend API**: http://localhost:8000
- **Web Frontend**: http://localhost:3000
- **Database**: PostgreSQL on port 5432
- **Cache**: Redis on port 6379

### Option 2: Manual Setup

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed manual setup instructions.

## 📁 Project Structure

```
E-B-global/
├── backend/                 # Django backend API
│   ├── accounts/           # User management & authentication
│   ├── services/           # Service catalog & categories
│   ├── bookings/           # Booking system & scheduling
│   ├── payments/           # Payment processing & invoices
│   ├── analytics/          # Analytics & reporting
│   └── ebglobal/          # Django project settings
├── web/                    # Next.js web application
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # Reusable UI components
│   │   │   ├── layout/    # Header, Footer, Navigation
│   │   │   ├── sections/  # Homepage sections
│   │   │   └── ui/        # shadcn/ui components
│   │   └── store/         # Redux store & API
├── mobile/                 # Expo React Native app
│   ├── app/               # Expo Router pages
│   ├── store/             # Redux store & API
│   └── assets/            # Images and icons
├── docker-compose.yml     # Development environment
├── DEPLOYMENT.md          # Deployment guide
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=ebglobal
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (SendGrid)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key

# AWS S3 (Production)
USE_S3=False
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket

# Stripe Payments
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key
```

## 📊 API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🎨 Design System

The platform uses a consistent design system across all applications:

- **Primary Color**: Blue (#1E40AF)
- **Typography**: Inter font family
- **Components**: shadcn/ui for web, custom components for mobile
- **Responsive**: Mobile-first design approach
- **Accessibility**: WCAG 2.1 AA compliant

## 🌍 Internationalization

The platform supports multiple languages with API-driven translations:

- **English** (default)
- **Portuguese** (Lusophone Africa)

Translations are managed through the backend API and cached for performance.

## 🔐 Security Features

- **JWT Authentication** with refresh token rotation
- **Role-based Access Control** (Admin, Staff, Partner, Client)
- **CORS Configuration** for cross-origin requests
- **Input Validation** and sanitization
- **SQL Injection Protection** with Django ORM
- **XSS Protection** with Content Security Policy
- **Rate Limiting** for API endpoints
- **SSL/TLS Encryption** in production

## 📱 Mobile Features

- **Cross-platform** iOS and Android support
- **Push Notifications** for booking updates
- **Location Services** for service discovery
- **Offline Support** with cached data
- **Biometric Authentication** support
- **Deep Linking** for sharing services

## 🚀 Deployment

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions including:

- Docker production setup
- Manual server configuration
- Database setup and migrations
- SSL certificate configuration
- Monitoring and logging setup
- Performance optimization

### Mobile App Distribution

- **iOS**: App Store deployment with EAS Build
- **Android**: Google Play Store deployment
- **Beta Testing**: TestFlight and Google Play Console

## 📈 Analytics & Monitoring

- **User Analytics**: Registration, engagement, and retention metrics
- **Business Analytics**: Revenue, bookings, and partner performance
- **System Monitoring**: Performance, errors, and uptime tracking
- **Custom Dashboards**: Real-time insights for admins and partners

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Submit a pull request

### Development Guidelines

- Follow the existing code style and conventions
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure mobile responsiveness
- Test on multiple devices and browsers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

- **Documentation**: Check this README and DEPLOYMENT.md
- **Issues**: Create an issue in the GitHub repository
- **Email**: Contact the development team
- **Community**: Join our developer community

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Core platform setup
- ✅ User authentication and management
- ✅ Service catalog and booking system
- ✅ Basic payment integration
- ✅ Multi-language support

### Phase 2 (Next)
- 🔄 Advanced analytics dashboard
- 🔄 Partner onboarding automation
- 🔄 Advanced search and filtering
- 🔄 Mobile app optimization
- 🔄 Performance improvements

### Phase 3 (Future)
- 📋 AI-powered service recommendations
- 📋 Advanced reporting and insights
- 📋 Third-party integrations
- 📋 Advanced notification system
- 📋 Enterprise features

---

**E-B Global** - Connecting Africa through Professional Services