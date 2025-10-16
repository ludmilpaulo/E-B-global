#!/usr/bin/env python3
"""
E-B Global Simple Integration Test
"""

import requests
import sys

def test_endpoint(url, timeout=10):
    """Test a single endpoint"""
    try:
        response = requests.get(url, timeout=timeout)
        return {
            "status_code": response.status_code,
            "success": response.status_code < 400,
            "content_length": len(response.text)
        }
    except Exception as e:
        return {"error": str(e), "success": False}

def main():
    print("E-B Global Integration Test")
    print("=" * 40)
    
    # Test endpoints
    endpoints = [
        ("Local Backend Health", "http://localhost:8000/api/v1/health/"),
        ("Production Backend Health", "https://www.e-b-global.online/api/v1/health/"),
        ("Production Frontend", "https://e-b-global.vercel.app/"),
    ]
    
    results = {}
    
    for name, url in endpoints:
        print(f"Testing {name}...")
        result = test_endpoint(url)
        results[name] = result
        
        if result.get("success"):
            print(f"  PASS - Status: {result.get('status_code')}")
        else:
            print(f"  FAIL - Status: {result.get('status_code', 'ERROR')}")
            if "error" in result:
                print(f"  Error: {result['error']}")
    
    print("\nSummary:")
    print("=" * 40)
    
    local_backend = results.get("Local Backend Health", {}).get("success", False)
    prod_backend = results.get("Production Backend Health", {}).get("success", False)
    frontend = results.get("Production Frontend", {}).get("success", False)
    
    print(f"Local Backend: {'WORKING' if local_backend else 'ERROR'}")
    print(f"Production Backend: {'WORKING' if prod_backend else 'NEEDS DEPLOYMENT'}")
    print(f"Production Frontend: {'WORKING' if frontend else 'ERROR'}")
    
    if frontend:
        print("\nSUCCESS: Frontend is accessible!")
        if not prod_backend:
            print("NOTE: Production backend needs deployment with correct settings.")
    else:
        print("\nERROR: Critical issues found!")
        sys.exit(1)

if __name__ == "__main__":
    main()
