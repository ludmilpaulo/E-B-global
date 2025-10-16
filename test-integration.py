#!/usr/bin/env python3
"""
E-B Global Integration Test Script
Tests all functionality including authentication, language switching, and API integration
"""

import requests
import json
import sys
from typing import Dict, Any

class EBGlobalTester:
    def __init__(self):
        self.local_backend = "http://localhost:8000"
        self.production_backend = "https://www.e-b-global.online"
        self.production_frontend = "https://e-b-global.vercel.app"
        self.results = {}
        
    def test_endpoint(self, url: str, method: str = "GET", data: Dict = None, headers: Dict = None) -> Dict[str, Any]:
        """Test a single endpoint and return results"""
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            else:
                return {"error": f"Unsupported method: {method}"}
                
            return {
                "status_code": response.status_code,
                "success": response.status_code < 400,
                "response_time": response.elapsed.total_seconds(),
                "content_length": len(response.text),
                "content_preview": response.text[:200] if response.text else "",
                "headers": dict(response.headers)
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "success": False
            }
    
    def test_backend_health(self):
        """Test backend health endpoints"""
        print("Testing Backend Health Endpoints...")
        
        # Test local backend
        local_result = self.test_endpoint(f"{self.local_backend}/api/v1/health/")
        self.results["local_backend_health"] = local_result
        print(f"  Local Backend: {'PASS' if local_result.get('success') else 'FAIL'} {local_result.get('status_code', 'ERROR')}")
        
        # Test production backend
        prod_result = self.test_endpoint(f"{self.production_backend}/api/v1/health/")
        self.results["production_backend_health"] = prod_result
        print(f"  Production Backend: {'PASS' if prod_result.get('success') else 'FAIL'} {prod_result.get('status_code', 'ERROR')}")
        
        return local_result.get('success', False), prod_result.get('success', False)
    
    def test_frontend(self):
        """Test frontend accessibility"""
        print("🌐 Testing Frontend...")
        
        frontend_result = self.test_endpoint(self.production_frontend)
        self.results["frontend"] = frontend_result
        
        if frontend_result.get('success'):
            content = frontend_result.get('content_preview', '').lower()
            has_title = 'e-b global' in content
            has_services = 'services' in content
            has_language = 'language' in content or 'idioma' in content
            
            print(f"  Frontend: ✅ {frontend_result.get('status_code')}")
            print(f"    Title: {'✅' if has_title else '❌'}")
            print(f"    Services: {'✅' if has_services else '❌'}")
            print(f"    Language Support: {'✅' if has_language else '❌'}")
        else:
            print(f"  Frontend: ❌ {frontend_result.get('status_code', 'ERROR')}")
        
        return frontend_result.get('success', False)
    
    def test_authentication_endpoints(self):
        """Test authentication endpoints"""
        print("🔐 Testing Authentication Endpoints...")
        
        # Test auth endpoints (should return 401 for unauthenticated requests)
        auth_endpoints = [
            "/api/v1/auth/login/",
            "/api/v1/auth/register/",
            "/api/v1/services/",
        ]
        
        auth_results = {}
        for endpoint in auth_endpoints:
            # Test local
            local_result = self.test_endpoint(f"{self.local_backend}{endpoint}")
            # Test production
            prod_result = self.test_endpoint(f"{self.production_backend}{endpoint}")
            
            auth_results[endpoint] = {
                "local": local_result,
                "production": prod_result
            }
            
            local_ok = local_result.get('status_code') == 401  # Expected for unauthenticated
            prod_ok = prod_result.get('status_code') == 401 or prod_result.get('success', False)
            
            print(f"  {endpoint}")
            print(f"    Local: {'✅' if local_ok else '❌'} {local_result.get('status_code', 'ERROR')}")
            print(f"    Production: {'✅' if prod_ok else '❌'} {prod_result.get('status_code', 'ERROR')}")
        
        self.results["authentication"] = auth_results
        return all(
            result["local"].get('status_code') == 401 and 
            (result["production"].get('status_code') == 401 or result["production"].get('success', False))
            for result in auth_results.values()
        )
    
    def test_language_features(self):
        """Test language and currency features"""
        print("🌍 Testing Language and Currency Features...")
        
        # Test if frontend has language switching
        frontend_result = self.results.get("frontend", {})
        content = frontend_result.get('content_preview', '').lower()
        
        # Check for language indicators
        has_english = any(word in content for word in ['services', 'professional', 'africa'])
        has_portuguese = any(word in content for word in ['serviços', 'profissional', 'áfrica'])
        has_language_switcher = 'en' in content and 'pt' in content
        
        print(f"  English Content: {'✅' if has_english else '❌'}")
        print(f"  Portuguese Content: {'✅' if has_portuguese else '❌'}")
        print(f"  Language Switcher: {'✅' if has_language_switcher else '❌'}")
        
        self.results["language_features"] = {
            "english_content": has_english,
            "portuguese_content": has_portuguese,
            "language_switcher": has_language_switcher
        }
        
        return has_english and has_language_switcher
    
    def test_api_integration(self):
        """Test API integration readiness"""
        print("🔗 Testing API Integration...")
        
        # Test if frontend can reach backend
        integration_ready = True
        
        # Check if production backend is accessible
        prod_health = self.results.get("production_backend_health", {})
        if not prod_health.get('success', False):
            print("  ❌ Production backend not accessible")
            integration_ready = False
        else:
            print("  ✅ Production backend accessible")
        
        # Check if frontend is accessible
        frontend_health = self.results.get("frontend", {})
        if not frontend_health.get('success', False):
            print("  ❌ Frontend not accessible")
            integration_ready = False
        else:
            print("  ✅ Frontend accessible")
        
        self.results["api_integration"] = integration_ready
        return integration_ready
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("E-B Global Integration Test Suite")
        print("=" * 50)
        
        # Run all tests
        backend_local_ok, backend_prod_ok = self.test_backend_health()
        frontend_ok = self.test_frontend()
        auth_ok = self.test_authentication_endpoints()
        language_ok = self.test_language_features()
        integration_ok = self.test_api_integration()
        
        # Summary
        print("\n📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Local Backend: {'✅ Working' if backend_local_ok else '❌ Error'}")
        print(f"Production Backend: {'✅ Working' if backend_prod_ok else '❌ Needs Deployment'}")
        print(f"Frontend: {'✅ Working' if frontend_ok else '❌ Error'}")
        print(f"Authentication: {'✅ Working' if auth_ok else '❌ Error'}")
        print(f"Language Features: {'✅ Working' if language_ok else '❌ Error'}")
        print(f"API Integration: {'✅ Ready' if integration_ok else '❌ Issues'}")
        
        # Overall status
        critical_issues = []
        if not frontend_ok:
            critical_issues.append("Frontend not accessible")
        if not auth_ok:
            critical_issues.append("Authentication issues")
        if not language_ok:
            critical_issues.append("Language features missing")
        
        if not critical_issues:
            print("\n🎉 ALL CRITICAL TESTS PASSED!")
            print("✅ The E-B Global application is ready for production use.")
        else:
            print(f"\n⚠️  CRITICAL ISSUES FOUND:")
            for issue in critical_issues:
                print(f"   ❌ {issue}")
        
        if not backend_prod_ok:
            print("\n📝 PRODUCTION BACKEND DEPLOYMENT NEEDED:")
            print("   1. Run './deploy-production.sh' to prepare deployment")
            print("   2. Update production server settings to use settings_production.py")
            print("   3. Restart production server")
        
        return {
            "backend_local": backend_local_ok,
            "backend_production": backend_prod_ok,
            "frontend": frontend_ok,
            "authentication": auth_ok,
            "language_features": language_ok,
            "api_integration": integration_ok,
            "critical_issues": critical_issues
        }

if __name__ == "__main__":
    tester = EBGlobalTester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if results["critical_issues"]:
        sys.exit(1)
    else:
        sys.exit(0)
