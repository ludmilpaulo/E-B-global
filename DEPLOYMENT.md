# E-B Global Deployment Guide

This guide covers deploying the E-B Global platform to production environments.

## 🚀 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose
- Domain name with DNS access
- SSL certificate (Let's Encrypt recommended)

### 1. Clone and Configure

```bash
git clone https://github.com/your-username/E-B-global.git
cd E-B-global

# Copy environment files
cp backend/env.example backend/.env
cp web/.env.example web/.env.local

# Edit configuration files
nano backend/.env
nano web/.env.local
```

### 2. Environment Configuration

#### Backend (.env)
```env
# Production Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=ebglobal_prod
DB_USER=ebglobal_user
DB_PASSWORD=secure-database-password
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Email (SendGrid)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# AWS S3 (Production)
USE_S3=True
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket
AWS_S3_REGION_NAME=us-east-1

# Stripe Payments
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key
```

#### Web (.env.local)
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api/v1
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
```

### 3. Deploy with Docker Compose

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

## 🏗️ Manual Server Deployment

### Prerequisites
- Ubuntu 20.04+ server
- PostgreSQL 15
- Redis 7
- Nginx
- Python 3.12
- Node.js 18

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.12 python3.12-venv python3.12-dev \
    postgresql postgresql-contrib redis-server nginx \
    build-essential libpq-dev curl git

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 2. Database Setup

```bash
# Create database and user
sudo -u postgres psql
CREATE DATABASE ebglobal_prod;
CREATE USER ebglobal_user WITH PASSWORD 'secure-password';
GRANT ALL PRIVILEGES ON DATABASE ebglobal_prod TO ebglobal_user;
\q
```

### 3. Backend Deployment

```bash
# Clone repository
git clone https://github.com/your-username/E-B-global.git
cd E-B-global/backend

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
nano .env  # Edit with production values

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test server
python manage.py runserver 0.0.0.0:8000
```

### 4. Web Frontend Deployment

```bash
cd ../web

# Install dependencies
npm ci --production

# Build application
npm run build

# Test production build
npm start
```

### 5. Nginx Configuration

Create `/etc/nginx/sites-available/ebglobal`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Web Frontend
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Static files
    location /static/ {
        alias /path/to/backend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /path/to/backend/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/ebglobal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 7. System Services

#### Backend Service (`/etc/systemd/system/ebglobal-backend.service`):
```ini
[Unit]
Description=E-B Global Backend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/path/to/backend
Environment=PATH=/path/to/backend/venv/bin
ExecStart=/path/to/backend/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 3 ebglobal.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Web Service (`/etc/systemd/system/ebglobal-web.service`):
```ini
[Unit]
Description=E-B Global Web Frontend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/path/to/web
ExecStart=/usr/bin/npm start
Restart=always

[Install]
WantedBy=multi-user.target
```

Start services:
```bash
sudo systemctl enable ebglobal-backend
sudo systemctl enable ebglobal-web
sudo systemctl start ebglobal-backend
sudo systemctl start ebglobal-web
```

## 📱 Mobile App Deployment

### 1. Expo Configuration

```bash
cd mobile

# Install EAS CLI
npm install -g @expo/eas-cli

# Login to Expo
eas login

# Configure EAS
eas build:configure
```

### 2. Build Configuration

Update `app.json`:
```json
{
  "expo": {
    "extra": {
      "eas": {
        "projectId": "your-expo-project-id"
      }
    }
  }
}
```

### 3. Build and Deploy

```bash
# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android

# Submit to app stores
eas submit --platform ios
eas submit --platform android
```

## 🔧 Production Optimizations

### Backend Optimizations

1. **Database Indexing**
```sql
-- Add indexes for common queries
CREATE INDEX CONCURRENTLY idx_bookings_client_status ON bookings_booking(client_id, status);
CREATE INDEX CONCURRENTLY idx_services_partner_active ON services_service(partner_id, is_active);
CREATE INDEX CONCURRENTLY idx_payments_booking_status ON payments_payment(booking_id, status);
```

2. **Caching Strategy**
```python
# In Django settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Cache frequently accessed data
from django.core.cache import cache

def get_service_categories():
    categories = cache.get('service_categories')
    if not categories:
        categories = ServiceCategory.objects.filter(is_active=True)
        cache.set('service_categories', categories, 3600)  # 1 hour
    return categories
```

3. **Static File Optimization**
```bash
# Compress static files
python manage.py compress

# Use CDN for static files
# Configure AWS CloudFront or Cloudflare
```

### Frontend Optimizations

1. **Next.js Optimization**
```javascript
// next.config.js
module.exports = {
  compress: true,
  poweredByHeader: false,
  images: {
    domains: ['your-s3-bucket.s3.amazonaws.com'],
    formats: ['image/webp', 'image/avif'],
  },
  experimental: {
    optimizeCss: true,
  },
}
```

2. **Bundle Analysis**
```bash
npm install --save-dev @next/bundle-analyzer
npm run analyze
```

## 📊 Monitoring and Logging

### 1. Error Tracking (Sentry)

```bash
# Install Sentry
pip install sentry-sdk[django]
```

Configure in Django settings:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### 2. Logging Configuration

```python
# settings.py
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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### 3. Performance Monitoring

```bash
# Install monitoring tools
pip install django-silk
pip install django-debug-toolbar  # Development only
```

## 🔒 Security Checklist

- [ ] SSL/TLS certificates installed and configured
- [ ] Security headers configured in Nginx
- [ ] Database credentials secured
- [ ] API keys and secrets in environment variables
- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] Input validation and sanitization
- [ ] Regular security updates
- [ ] Backup strategy implemented
- [ ] Monitoring and alerting set up

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Errors**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U ebglobal_user -d ebglobal_prod
```

2. **Static Files Not Loading**
```bash
# Check file permissions
sudo chown -R www-data:www-data /path/to/staticfiles

# Collect static files
python manage.py collectstatic --noinput
```

3. **High Memory Usage**
```bash
# Monitor processes
htop
ps aux | grep python

# Optimize Gunicorn workers
# Reduce --workers count if needed
```

4. **SSL Certificate Issues**
```bash
# Test SSL configuration
openssl s_client -connect yourdomain.com:443

# Renew certificate
sudo certbot renew --dry-run
```

## 📞 Support

For deployment issues:
- Check logs: `sudo journalctl -u ebglobal-backend -f`
- Monitor system resources: `htop`, `df -h`
- Test connectivity: `curl -I https://yourdomain.com/api/`
- Review Nginx logs: `sudo tail -f /var/log/nginx/error.log`

---

**Happy Deploying!** 🚀