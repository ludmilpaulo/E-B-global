# E-B Global Deployment Guide

## 🚀 Production Deployment Configuration

This guide covers the complete deployment setup for the E-B Global application with the production domain `www.e-b-global.online`.

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL (for production)
- Redis (optional, for caching)
- Web server (Nginx/Apache)
- SSL certificates

## 🔧 Backend Configuration

### 1. Production Settings

The backend is configured with production settings in `backend/ebglobal/settings_production.py`:

- **Domain**: `www.e-b-global.online`
- **Allowed Hosts**: `www.e-b-global.online`, `e-b-global.online`
- **CORS Origins**: HTTPS domains for frontend applications
- **Security**: SSL redirect, HSTS, secure headers
- **Database**: PostgreSQL (production) / SQLite (development)

### 2. Environment Variables

Create a `.env` file in the backend directory with:

```bash
# Production Environment
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=www.e-b-global.online,e-b-global.online

# Database
DB_NAME=ebglobal_prod
DB_USER=ebglobal_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@e-b-global.online

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# AWS S3 (optional)
USE_S3=True
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=ebglobal-production
```

### 3. Deployment Commands

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Run deployment script
python deploy.py
```

### 4. Health Check Endpoints

The API includes health monitoring endpoints:

- **Health Check**: `GET /api/v1/health/`
- **API Status**: `GET /api/v1/status/`

Example response:
```json
{
  "status": "healthy",
  "service": "E-B Global API",
  "version": "1.0.0",
  "database": "connected",
  "redis": "available",
  "timestamp": "2025-10-16T02:13:38.336585"
}
```

## 🌐 Frontend Configuration

### 1. Web Application

The web app automatically detects the environment and uses the appropriate API URL:

- **Development**: `http://localhost:8000`
- **Production**: `https://www.e-b-global.online`

Configuration is in `web/src/config/api.ts`:

```typescript
const isProduction = process.env.NODE_ENV === 'production';
export const API_CONFIG = {
  BASE_URL: isProduction ? 'https://www.e-b-global.online' : 'http://localhost:8000',
  // ... other configurations
};
```

### 2. Build Commands

```bash
# Navigate to web directory
cd web

# Install dependencies
npm install

# Build for production
npm run build

# Start production server
npm start
```

### 3. Mobile Application

The mobile app uses the same API configuration pattern:

- **Development**: `http://localhost:8000`
- **Production**: `https://www.e-b-global.online`

Configuration is in `mobile/src/config/api.ts`.

## 🔐 Authentication Features

### 1. Web Application
- JWT-based authentication
- Forgot password functionality
- Automatic currency detection
- Multi-language support (English/Portuguese)

### 2. Mobile Application
- Biometric authentication (Face ID, Touch ID, Iris)
- JWT-based authentication
- Automatic currency detection
- Multi-language support

## 🌍 Internationalization

The application supports:

- **Languages**: English, Portuguese
- **Auto-detection**: Browser language detection
- **Currency**: Automatic currency detection based on user location
- **Countries**: 7 African currencies supported

## 📱 Mobile Features

### Biometric Authentication
- Face ID (iOS)
- Touch ID (iOS/Android)
- Iris recognition
- Secure credential storage

### API Integration
- Production-ready API endpoints
- Health monitoring
- Error handling
- Retry mechanisms

## 🚀 Deployment Steps

### 1. Backend Deployment

```bash
# 1. Set up production server
sudo apt update
sudo apt install python3-pip postgresql nginx

# 2. Clone repository
git clone https://github.com/ludmilpaulo/E-B-global.git
cd E-B-global/backend

# 3. Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment variables
cp .env.example .env
# Edit .env with production values

# 6. Set up database
sudo -u postgres createdb ebglobal_prod
python manage.py migrate

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Start application server
gunicorn ebglobal.wsgi_production:application --bind 0.0.0.0:8000
```

### 2. Frontend Deployment

```bash
# 1. Navigate to web directory
cd web

# 2. Install dependencies
npm install

# 3. Build for production
npm run build

# 4. Start production server
npm start
```

### 3. Nginx Configuration

```nginx
server {
    listen 80;
    server_name www.e-b-global.online e-b-global.online;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name www.e-b-global.online e-b-global.online;

    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/private.key;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔍 Monitoring & Health Checks

### API Health Monitoring

```bash
# Check API health
curl https://www.e-b-global.online/api/v1/health/

# Check API status
curl https://www.e-b-global.online/api/v1/status/
```

### Frontend Health Checks

The applications include automatic API health checking and fallback mechanisms.

## 📊 Performance Optimization

### Backend
- Database connection pooling
- Redis caching
- Static file serving via Nginx
- Gzip compression

### Frontend
- Next.js optimization
- Static generation
- Image optimization
- Code splitting

## 🔒 Security Features

### Backend
- HTTPS enforcement
- CORS configuration
- JWT authentication
- Rate limiting
- Input validation

### Frontend
- HTTPS-only communication
- Secure token storage
- XSS protection
- CSRF protection

## 📱 Mobile Deployment

### iOS
```bash
# Build for iOS
cd mobile
npx expo build:ios
```

### Android
```bash
# Build for Android
cd mobile
npx expo build:android
```

## 🚨 Troubleshooting

### Common Issues

1. **API Connection Issues**
   - Check CORS configuration
   - Verify SSL certificates
   - Test health endpoints

2. **Database Connection**
   - Verify PostgreSQL is running
   - Check connection credentials
   - Run migrations

3. **Static Files**
   - Ensure static files are collected
   - Check Nginx configuration
   - Verify file permissions

### Logs

- **Backend**: `backend/logs/django.log`
- **Frontend**: Browser console
- **Mobile**: Expo logs

## 📞 Support

For deployment support:
- Check health endpoints: `/api/v1/health/`
- Review logs in `backend/logs/`
- Test API connectivity
- Verify SSL configuration

## 🎯 Success Criteria

✅ **Backend**: API responds on `https://www.e-b-global.online/api/v1/health/`
✅ **Frontend**: Web app loads on `https://www.e-b-global.online`
✅ **Mobile**: App connects to production API
✅ **Authentication**: Login/logout works
✅ **Translations**: Language switching works
✅ **Currency**: Auto-detection works
✅ **Biometrics**: Mobile authentication works

---

**Deployment Status**: ✅ Ready for Production
**API Domain**: `https://www.e-b-global.online`
**Last Updated**: October 16, 2025
