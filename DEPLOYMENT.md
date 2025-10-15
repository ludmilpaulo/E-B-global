# E-B Global - Deployment Guide

## 🚀 Quick Start with Docker

The easiest way to run E-B Global is using Docker Compose:

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
- **Backend**: http://localhost:8000
- **Web Frontend**: http://localhost:3000
- **Database**: PostgreSQL on port 5432
- **Cache**: Redis on port 6379

## 📋 Manual Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp env.example .env

# Edit .env with your configuration
nano .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Web Frontend Setup

```bash
cd web

# Install dependencies
npm install

# Start development server
npm run dev
```

### Mobile App Setup

```bash
cd mobile

# Install dependencies
npm install

# Start Expo development server
npx expo start
```

## 🌍 Environment Configuration

### Backend (.env)
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Settings
DB_NAME=ebglobal
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Redis Settings
REDIS_URL=redis://localhost:6379/0

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@ebglobal.com

# AWS S3 Settings (for production)
USE_S3=False
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Payment Gateway Settings
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
```

### Mobile (app.json)
```json
{
  "expo": {
    "extra": {
      "apiUrl": "http://localhost:8000/api/v1"
    }
  }
}
```

## 🐳 Production Deployment

### Using Docker Compose

1. **Update docker-compose.yml for production:**
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend

  # ... other services with production configurations
```

2. **Deploy:**
```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

### Manual Production Setup

1. **Backend (Ubuntu/Debian):**
```bash
# Install system dependencies
sudo apt update
sudo apt install python3.11 python3.11-venv postgresql postgresql-contrib redis-server nginx

# Create application user
sudo useradd -m -s /bin/bash ebglobal
sudo su - ebglobal

# Clone and setup application
git clone <repository-url>
cd E-B-global/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure PostgreSQL
sudo -u postgres createdb ebglobal
sudo -u postgres createuser ebglobal
sudo -u postgres psql -c "ALTER USER ebglobal PASSWORD 'your-password';"

# Run migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput

# Setup systemd service
sudo nano /etc/systemd/system/ebglobal-backend.service
```

2. **Frontend:**
```bash
cd ../web
npm install
npm run build
npm install -g pm2
pm2 start npm --name "ebglobal-web" -- start
pm2 save
pm2 startup
```

3. **Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ebglobal/E-B-global/backend/staticfiles/;
    }

    location /media/ {
        alias /home/ebglobal/E-B-global/backend/media/;
    }
}
```

## 📱 Mobile App Deployment

### iOS (App Store)
```bash
cd mobile

# Install EAS CLI
npm install -g @expo/eas-cli

# Login to Expo
eas login

# Configure EAS
eas build:configure

# Build for iOS
eas build --platform ios

# Submit to App Store
eas submit --platform ios
```

### Android (Google Play)
```bash
cd mobile

# Build for Android
eas build --platform android

# Submit to Google Play
eas submit --platform android
```

## 🔧 Database Setup

### Initial Data
```bash
# Create superuser
python manage.py createsuperuser

# Load initial data (categories, locations, etc.)
python manage.py loaddata initial_data.json

# Create sample partners and services
python manage.py create_sample_data
```

### Backup & Restore
```bash
# Backup database
pg_dump -h localhost -U ebglobal ebglobal > backup.sql

# Restore database
psql -h localhost -U ebglobal ebglobal < backup.sql
```

## 🔐 Security Checklist

- [ ] Change default database passwords
- [ ] Use strong SECRET_KEY
- [ ] Configure HTTPS with SSL certificates
- [ ] Set up proper CORS settings
- [ ] Configure firewall rules
- [ ] Enable database SSL
- [ ] Set up backup strategy
- [ ] Configure monitoring and logging
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting

## 📊 Monitoring & Logging

### Application Monitoring
```bash
# Install monitoring tools
pip install sentry-sdk

# Configure Sentry in settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### Log Configuration
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

## 🚀 Performance Optimization

### Backend
- Enable database connection pooling
- Configure Redis caching
- Use CDN for static files
- Enable Gzip compression
- Optimize database queries

### Frontend
- Enable Next.js static generation
- Use image optimization
- Implement code splitting
- Configure caching headers
- Use service workers

### Database
- Create proper indexes
- Optimize queries
- Configure connection pooling
- Set up read replicas for scaling

## 📞 Support

For deployment issues or questions:
- Check the logs: `docker-compose logs -f`
- Review the configuration files
- Ensure all environment variables are set
- Verify database connectivity
- Check firewall and network settings

## 🔄 Updates

To update the application:
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart services
docker-compose down
docker-compose build
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate
```
