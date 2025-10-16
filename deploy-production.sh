#!/bin/bash

# E-B Global Production Deployment Script
# This script helps deploy the backend to production with correct settings

echo "🚀 E-B Global Production Deployment Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "backend/ebglobal/settings_production.py" ]; then
    echo "❌ Error: settings_production.py not found. Please run from project root."
    exit 1
fi

echo "✅ Production settings file found"

# Create environment file for production
echo "📝 Creating production environment file..."
cat > backend/.env.production << EOF
# Production Environment Variables for E-B Global
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=www.e-b-global.online,e-b-global.online,localhost,127.0.0.1

# Database Configuration
DB_NAME=ebglobal_prod
DB_USER=ebglobal_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@e-b-global.online

# AWS S3 Configuration (Optional)
USE_S3=False
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
EOF

echo "✅ Production environment file created: backend/.env.production"

# Instructions for production deployment
echo ""
echo "📋 PRODUCTION DEPLOYMENT INSTRUCTIONS:"
echo "====================================="
echo ""
echo "1. Copy the production settings to your server:"
echo "   scp backend/.env.production user@your-server:/path/to/E-B-global/backend/.env"
echo ""
echo "2. Update your server's Django settings to use production:"
echo "   export DJANGO_SETTINGS_MODULE=ebglobal.settings_production"
echo ""
echo "3. Install production dependencies:"
echo "   pip install -r backend/requirements.txt"
echo ""
echo "4. Run database migrations:"
echo "   python backend/manage.py migrate --settings=ebglobal.settings_production"
echo ""
echo "5. Collect static files:"
echo "   python backend/manage.py collectstatic --noinput --settings=ebglobal.settings_production"
echo ""
echo "6. Restart your web server (uWSGI/Gunicorn):"
echo "   sudo systemctl restart your-django-service"
echo ""
echo "7. Test the deployment:"
echo "   curl https://www.e-b-global.online/api/v1/health/"
echo ""
echo "⚠️  IMPORTANT: Update the SECRET_KEY and other sensitive values in .env.production"
echo "⚠️  IMPORTANT: Ensure your web server is configured to use ebglobal.settings_production"
echo ""
echo "🎯 The production backend should then accept requests from www.e-b-global.online"

# Create a simple health check script
echo ""
echo "📝 Creating health check script..."
cat > health-check.sh << 'EOF'
#!/bin/bash
echo "🔍 Testing E-B Global API Health..."
echo "=================================="

# Test local backend
echo "Testing local backend (http://localhost:8000)..."
LOCAL_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/health/)
echo "Local backend status: $LOCAL_STATUS"

# Test production backend
echo "Testing production backend (https://www.e-b-global.online)..."
PROD_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://www.e-b-global.online/api/v1/health/)
echo "Production backend status: $PROD_STATUS"

# Test production frontend
echo "Testing production frontend (https://e-b-global.vercel.app)..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://e-b-global.vercel.app/)
echo "Production frontend status: $FRONTEND_STATUS"

echo ""
echo "📊 Summary:"
echo "Local Backend: $([ $LOCAL_STATUS -eq 200 ] && echo "✅ Working" || echo "❌ Error")"
echo "Production Backend: $([ $PROD_STATUS -eq 200 ] && echo "✅ Working" || echo "❌ Needs Deployment")"
echo "Production Frontend: $([ $FRONTEND_STATUS -eq 200 ] && echo "✅ Working" || echo "❌ Error")"
EOF

chmod +x health-check.sh
echo "✅ Health check script created: health-check.sh"

echo ""
echo "🎉 Deployment preparation complete!"
echo "Run './health-check.sh' to test all endpoints after deployment."
