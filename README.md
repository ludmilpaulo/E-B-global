# E-B Global - Multi-Service Marketplace

A comprehensive marketplace platform serving Lusophone and Anglophone Africa, enabling clients to discover, compare, and book professional services from vetted partners.

## 🚀 Project Overview

E-B Global is a multi-service marketplace offering:
- **Imobiliária** (Real Estate Consulting)
- **Transportes/Transfers** (Transportation Services)
- **Consultoria de Negócios/Jurídica** (Business/Legal Consulting)
- **Serviços Linguísticos** (Language Services)
- **Reconhecimento de Documentos** (Document Recognition - Notary, MIREX, Embassies)
- **Catering Corporativo** (Corporate Catering)
- **Protocolo** (Protocol Services)

## 🏗️ Architecture

### Backend (Django + DRF)
- Django 5 with Django REST Framework
- PostgreSQL database
- Redis for caching and task queues
- Celery for background tasks
- JWT authentication
- OpenAPI documentation with drf-spectacular

### Web Frontend (Next.js)
- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Redux Toolkit with RTK Query

### Mobile App (Expo React Native)
- Expo SDK 50+
- React Native with TypeScript
- Expo Router for navigation
- Redux Toolkit with RTK Query
- Native localization support

## 🌍 Internationalization

- **Portuguese** (default for PT locales)
- **English** (default for EN locales)
- User-overridable language selection
- API-driven i18n system

## 📱 Key Features

### For Clients
- Service discovery with smart filtering
- 90-minute booking slots
- Real-time chat with partners
- Multi-language support
- Secure payments
- Order tracking and timeline

### For Partners
- Service catalog management
- Availability scheduling
- Order management
- Financial dashboard
- Performance analytics

### For Admins
- Partner verification and approval
- Analytics dashboard with charts
- Dispute resolution
- Financial management
- System configuration

## 🔧 Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Web Setup
```bash
cd web
npm install
npm run dev
```

### Mobile Setup
```bash
cd mobile
npm install
npx expo start
```

## 🚀 Deployment

The application is configured for deployment with:
- Docker containers
- Nginx reverse proxy
- CI/CD with GitHub Actions
- Environment-based configuration

## 📊 Business Rules

- **90-minute slots**: All bookings must respect minimum 1h30 windows
- **Geo-scoping**: Default to user's country/province with manual override
- **Partner verification**: KYC process for all service providers
- **Multi-currency**: Support for local payment methods

## 🔐 Security

- JWT authentication with refresh tokens
- Rate limiting and CORS protection
- File upload security
- PII data protection
- Audit trails for admin actions

## 📈 Analytics

Admin dashboard includes:
- GMV and booking metrics
- Conversion funnels
- Geographic distribution maps
- Partner performance analytics
- Financial reporting

## 🌟 Logo Design

The E-B Global logo features a professional circular design with:
- Stylized globe in blue tones
- "E.B GLOBAL" branding
- "We are One" tagline
- Modern, clean aesthetic representing global reach and unity

---

**Built with ❤️ for Lusophone and Anglophone Africa**
