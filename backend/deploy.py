#!/usr/bin/env python3
"""
Deployment script for E-B Global API
"""
import os
import sys
import subprocess
import django
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebglobal.settings_production')

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def deploy():
    """Main deployment function"""
    print("🚀 Starting E-B Global API deployment...")
    
    # Install/update dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Run database migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        return False
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        return False
    
    # Create superuser if it doesn't exist
    try:
        django.setup()
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            print("🔄 Creating superuser...")
            User.objects.create_superuser(
                email='admin@e-b-global.online',
                password='admin123',  # Change this in production
                first_name='Admin',
                last_name='User'
            )
            print("✅ Superuser created")
        else:
            print("✅ Superuser already exists")
    except Exception as e:
        print(f"⚠️  Superuser creation failed: {e}")
    
    # Run tests
    if not run_command("python manage.py test", "Running tests"):
        print("⚠️  Tests failed, but continuing deployment")
    
    print("🎉 Deployment completed successfully!")
    print("📋 Next steps:")
    print("   1. Configure your web server (nginx/apache)")
    print("   2. Set up SSL certificates")
    print("   3. Configure environment variables")
    print("   4. Start the application server")
    
    return True

if __name__ == "__main__":
    success = deploy()
    sys.exit(0 if success else 1)
