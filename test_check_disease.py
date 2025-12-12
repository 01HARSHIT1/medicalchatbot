#!/usr/bin/env python3
"""
Test script for the Check Disease endpoint
=========================================

This script tests if the /check_disease endpoint is working correctly.
"""

import requests
import json

def test_check_disease_endpoint():
    """Test the check_disease endpoint"""
    print("🧪 Testing Check Disease Endpoint...")
    print("=" * 50)
    
    # Test data
    test_data = {
        "disease_name": "Acne"
    }
    
    try:
        print(f"🚀 Sending POST request to /check_disease...")
        print(f"   Disease: {test_data['disease_name']}")
        
        response = requests.post(
            "http://localhost:5000/check_disease",
            json=test_data,
            timeout=10
        )
        
        print(f"✅ Response received!")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Disease: {data.get('disease_name')}")
            print(f"   Symptom Count: {data.get('symptom_count')}")
            print(f"   All Symptoms: {data.get('all_symptoms')}")
            return True
        else:
            print(f"   ❌ Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error: Backend not running on port 5000")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def test_predict_endpoint():
    """Test the predict endpoint"""
    print(f"\n🧪 Testing Predict Endpoint...")
    print("=" * 50)
    
    # Test data
    test_data = {
        "symptoms": ["chills", "vomiting", "high_fever"]
    }
    
    try:
        print(f"🚀 Sending POST request to /predict...")
        print(f"   Symptoms: {test_data['symptoms']}")
        
        response = requests.post(
            "http://localhost:5000/predict",
            json=test_data,
            timeout=10
        )
        
        print(f"✅ Response received!")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Predicted Disease: {data.get('predicted_disease')}")
            print(f"   Description: {data.get('description')[:50]}...")
            return True
        else:
            print(f"   ❌ Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error: Backend not running on port 5000")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print(f"🚀 Starting Backend Tests...")
    
    # Test predict endpoint first
    predict_ok = test_predict_endpoint()
    
    if predict_ok:
        # Test check_disease endpoint
        check_ok = test_check_disease_endpoint()
        
        if check_ok:
            print(f"\n🎉 Both endpoints are working correctly!")
            print(f"   The Check Disease button should now appear!")
        else:
            print(f"\n❌ Check Disease endpoint failed!")
    else:
        print(f"\n❌ Predict endpoint failed!")
        print(f"   Cannot test Check Disease without working prediction!")
    
    print(f"\n" + "=" * 50)
    print(f"Test complete!")
