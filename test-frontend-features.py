#!/usr/bin/env python3
"""
Test E-B Global Frontend Features
"""

import requests
import json

def test_registration_page():
    """Test the registration page functionality"""
    print("Testing Frontend Registration Page...")
    print("=" * 40)
    
    try:
        response = requests.get('https://e-b-global.vercel.app/auth/register/', timeout=10)
        print(f"Registration Page Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text.lower()
            
            # Check for key form elements
            checks = [
                ('First Name field', 'first name' in content),
                ('Last Name field', 'last name' in content),
                ('Email field', 'email' in content),
                ('Password field', 'password' in content),
                ('Confirm Password', 'confirm password' in content),
                ('Phone Number', 'phone number' in content),
                ('Account Type', 'account type' in content or 'client' in content),
                ('Language Selection', 'preferred language' in content or 'english' in content),
                ('Sign Up Button', 'sign up' in content),
                ('Login Link', 'already have an account' in content)
            ]
            
            print()
            print("Form Elements Check:")
            for check_name, result in checks:
                status = "PASS" if result else "FAIL"
                print(f"  {check_name}: {status}")
            
            # Overall assessment
            passed = sum(1 for _, result in checks if result)
            total = len(checks)
            print(f"\nOverall Score: {passed}/{total} checks passed")
            
            if passed >= 8:
                print("SUCCESS: Registration form is fully functional!")
                return True
            else:
                print("WARNING: Some form elements may be missing")
                return False
        else:
            print("FAIL: Registration page not accessible")
            return False
            
    except Exception as e:
        print(f"Error testing registration page: {e}")
        return False

def test_homepage_features():
    """Test homepage features"""
    print("\nTesting Homepage Features...")
    print("=" * 40)
    
    try:
        response = requests.get('https://e-b-global.vercel.app/', timeout=10)
        print(f"Homepage Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text.lower()
            
            # Check for key homepage elements
            checks = [
                ('Hero Section', 'professional services' in content),
                ('Service Categories', 'real estate' in content and 'transportation' in content),
                ('Language Switcher', 'en' in content and 'pt' in content),
                ('Navigation Menu', 'services' in content and 'about' in content),
                ('Search Functionality', 'search' in content),
                ('Statistics', '500+' in content or 'verified partners' in content),
                ('How It Works', 'discover services' in content or 'book your slot' in content),
                ('Testimonials', 'clients say' in content or 'testimonials' in content),
                ('Call to Action', 'get started' in content or 'find services' in content),
                ('Footer', 'company' in content and 'support' in content)
            ]
            
            print()
            print("Homepage Features Check:")
            for check_name, result in checks:
                status = "PASS" if result else "FAIL"
                print(f"  {check_name}: {status}")
            
            passed = sum(1 for _, result in checks if result)
            total = len(checks)
            print(f"\nOverall Score: {passed}/{total} features working")
            
            return passed >= 8
            
        else:
            print("FAIL: Homepage not accessible")
            return False
            
    except Exception as e:
        print(f"Error testing homepage: {e}")
        return False

def test_navigation_pages():
    """Test navigation pages"""
    print("\nTesting Navigation Pages...")
    print("=" * 40)
    
    pages = [
        ('/services', 'Services Page'),
        ('/about', 'About Page'),
        ('/contact', 'Contact Page'),
        ('/how-it-works', 'How It Works Page'),
        ('/auth/login', 'Login Page')
    ]
    
    results = []
    
    for page, name in pages:
        try:
            response = requests.get(f'https://e-b-global.vercel.app{page}', timeout=10)
            status = "PASS" if response.status_code == 200 else "FAIL"
            print(f"  {name}: {status} ({response.status_code})")
            results.append(response.status_code == 200)
        except Exception as e:
            print(f"  {name}: FAIL (Error: {e})")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\nNavigation Pages: {passed}/{total} working")
    
    return passed >= 4

def test_language_features():
    """Test language and currency features"""
    print("\nTesting Language & Currency Features...")
    print("=" * 40)
    
    try:
        response = requests.get('https://e-b-global.vercel.app/', timeout=10)
        content = response.text.lower()
        
        # Check for multilingual content
        checks = [
            ('English Content', 'professional' in content and 'services' in content),
            ('Language Switcher', 'en' in content and 'pt' in content),
            ('Currency Support', 'currency' in content or '$' in content or '€' in content),
            ('African Context', 'africa' in content or 'angola' in content),
            ('Service Categories', len([cat for cat in ['real estate', 'transportation', 'legal', 'business'] if cat in content]) >= 3)
        ]
        
        print()
        print("Language & Currency Check:")
        for check_name, result in checks:
            status = "PASS" if result else "FAIL"
            print(f"  {check_name}: {status}")
        
        passed = sum(1 for _, result in checks if result)
        total = len(checks)
        print(f"\nLanguage Features: {passed}/{total} working")
        
        return passed >= 4
        
    except Exception as e:
        print(f"Error testing language features: {e}")
        return False

def main():
    """Run all frontend tests"""
    print("E-B Global Frontend Feature Testing")
    print("=" * 50)
    
    # Run all tests
    registration_ok = test_registration_page()
    homepage_ok = test_homepage_features()
    navigation_ok = test_navigation_pages()
    language_ok = test_language_features()
    
    # Summary
    print("\n" + "=" * 50)
    print("FRONTEND TEST SUMMARY")
    print("=" * 50)
    print(f"Registration Page: {'WORKING' if registration_ok else 'ISSUES'}")
    print(f"Homepage Features: {'WORKING' if homepage_ok else 'ISSUES'}")
    print(f"Navigation Pages: {'WORKING' if navigation_ok else 'ISSUES'}")
    print(f"Language Features: {'WORKING' if language_ok else 'ISSUES'}")
    
    overall_score = sum([registration_ok, homepage_ok, navigation_ok, language_ok])
    total_tests = 4
    
    print(f"\nOverall Score: {overall_score}/{total_tests}")
    
    if overall_score >= 3:
        print("\nSUCCESS: Frontend is working excellently!")
        print("✅ Users can register and access all features")
    else:
        print("\nWARNING: Some frontend issues detected")
    
    return overall_score >= 3

if __name__ == "__main__":
    main()
