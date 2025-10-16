"""
Health check views for API monitoring
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for API monitoring
    Returns basic system status
    """
    try:
        # Check database connectivity
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        
        # Check Redis connectivity (if available)
        redis_status = "unavailable"
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.ping()
            redis_status = "available"
        except:
            pass
        
        health_data = {
            "status": "healthy",
            "service": "E-B Global API",
            "version": "1.0.0",
            "database": "connected",
            "redis": redis_status,
            "timestamp": str(__import__('datetime').datetime.now())
        }
        
        return JsonResponse(health_data, status=200)
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JsonResponse({
            "status": "unhealthy",
            "service": "E-B Global API",
            "error": str(e),
            "timestamp": str(__import__('datetime').datetime.now())
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def api_status(request):
    """
    API status endpoint with more detailed information
    """
    try:
        from django.conf import settings
        
        status_data = {
            "status": "operational",
            "service": "E-B Global API",
            "version": "1.0.0",
            "environment": "production" if not settings.DEBUG else "development",
            "debug_mode": settings.DEBUG,
            "allowed_hosts": settings.ALLOWED_HOSTS,
            "cors_origins": getattr(settings, 'CORS_ALLOWED_ORIGINS', []),
            "database_engine": settings.DATABASES['default']['ENGINE'],
            "timestamp": str(__import__('datetime').datetime.now())
        }
        
        return JsonResponse(status_data, status=200)
        
    except Exception as e:
        logger.error(f"API status check failed: {str(e)}")
        return JsonResponse({
            "status": "error",
            "service": "E-B Global API",
            "error": str(e),
            "timestamp": str(__import__('datetime').datetime.now())
        }, status=500)
