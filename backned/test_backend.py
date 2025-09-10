#!/usr/bin/env python3
"""
Test script for the Valuefy AI Portfolio Assistant backend
"""

import requests
import json
import time

def test_backend():
    """Test the backend API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Valuefy AI Portfolio Assistant Backend")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print(f"✅ Root endpoint working: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {str(e)}")
    
    # Test 3: MongoDB query
    print("\n3. Testing MongoDB query...")
    try:
        test_question = "Find clients with high risk appetite"
        payload = {"question": test_question}
        response = requests.post(f"{base_url}/ask", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ MongoDB query successful:")
            print(f"   Question: {test_question}")
            print(f"   Answer: {result.get('answer', 'No answer')}")
            print(f"   Processing time: {result.get('processing_time', 'Unknown')}")
        else:
            print(f"❌ MongoDB query failed: {response.status_code}")
            print(f"   Error: {response.text}")
            # Try to get more detailed error info
            try:
                error_data = response.json()
                if 'detail' in error_data:
                    print(f"   Detail: {error_data['detail']}")
            except:
                pass
    except Exception as e:
        print(f"❌ MongoDB query error: {str(e)}")
    
    # Test 4: SQL query
    print("\n4. Testing SQL query...")
    try:
        test_question = "Show me recent transactions"
        payload = {"question": test_question}
        response = requests.post(f"{base_url}/ask", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SQL query successful:")
            print(f"   Question: {test_question}")
            print(f"   Answer: {result.get('answer', 'No answer')}")
            print(f"   Processing time: {result.get('processing_time', 'Unknown')}")
        else:
            print(f"❌ SQL query failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ SQL query error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🏁 Testing completed!")

if __name__ == "__main__":
    test_backend() 