"""
Test script to validate the WhisperWorkPro backend setup
Run this after starting your server to ensure everything works correctly.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:10000"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def print_result(test_name, status_code, expected_code=200):
    """Print test result with status"""
    status = "✅ PASS" if status_code == expected_code else "❌ FAIL"
    print(f"{status} {test_name}: {status_code}")

def test_health():
    """Test health endpoint"""
    print_section("HEALTH CHECK TESTS")
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print_result("Root endpoint", response.status_code)
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ FAIL Root endpoint: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_result("Health endpoint", response.status_code)
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Timestamp: {data.get('timestamp')}")
    except Exception as e:
        print(f"❌ FAIL Health endpoint: {e}")

def test_create_client():
    """Test creating a client"""
    print_section("CLIENT CREATION TESTS")
    
    client_data = {
        "name": "João Silva",
        "phone_number": "+351912345678",
        "email": "joao@example.com",
        "address": "Rua das Flores, 123, Porto",
        "notes": "Test client created by API test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/clients/", json=client_data)
        print_result("Create client", response.status_code, 201)
        
        if response.status_code == 201:
            client = response.json()
            print(f"   Created client ID: {client['id']}")
            print(f"   Name: {client['name']}")
            print(f"   Phone: {client['phone_number']}")
            return client["id"]
        else:
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ FAIL Create client: {e}")
        return None

def test_duplicate_client():
    """Test creating duplicate client (should fail)"""
    client_data = {
        "name": "João Silva Duplicate",
        "phone_number": "+351912345678",  # Same phone as above
        "email": "joao2@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/clients/", json=client_data)
        print_result("Create duplicate client (should fail)", response.status_code, 400)
        
        if response.status_code == 400:
            print(f"   Expected error: {response.json()['detail']}")
            
    except Exception as e:
        print(f"❌ FAIL Duplicate client test: {e}")

def test_get_clients():
    """Test getting all clients"""
    try:
        response = requests.get(f"{BASE_URL}/clients/")
        print_result("Get all clients", response.status_code)
        
        if response.status_code == 200:
            clients = response.json()
            print(f"   Found {len(clients)} clients")
            return clients
            
    except Exception as e:
        print(f"❌ FAIL Get clients: {e}")
        return []

def test_update_client(client_id):
    """Test updating a client"""
    if not client_id:
        print("❌ SKIP Update client: No client ID provided")
        return
    
    update_data = {
        "notes": f"Updated at {datetime.now().isoformat()}"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/clients/{client_id}", json=update_data)
        print_result("Update client", response.status_code)
        
        if response.status_code == 200:
            client = response.json()
            print(f"   Updated notes: {client['notes'][:50]}...")
            
    except Exception as e:
        print(f"❌ FAIL Update client: {e}")

def test_search_clients():
    """Test searching clients"""
    print_section("SEARCH TESTS")
    
    search_queries = ["João", "351", "example.com"]
    
    for query in search_queries:
        try:
            response = requests.get(f"{BASE_URL}/clients/search/?q={query}")
            print_result(f"Search '{query}'", response.status_code)
            
            if response.status_code == 200:
                results = response.json()
                print(f"   Found {len(results)} results")
                
        except Exception as e:
            print(f"❌ FAIL Search '{query}': {e}")

def test_client_history(client_id):
    """Test getting client history"""
    if not client_id:
        print("❌ SKIP Client history: No client ID provided")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/clients/{client_id}/history")
        print_result("Get client history", response.status_code)
        
        if response.status_code == 200:
            history = response.json()
            print(f"   Found {len(history)} history entries")
            for entry in history[:3]:  # Show first 3 entries
                print(f"   - {entry['action']}: {entry['details']}")
                
    except Exception as e:
        print(f"❌ FAIL Client history: {e}")

def test_resend_features(client_id):
    """Test resend invoice and job summary"""
    print_section("RESEND FEATURE TESTS")
    
    if not client_id:
        print("❌ SKIP Resend tests: No client ID provided")
        return
    
    # Test resend invoice
    try:
        response = requests.post(f"{BASE_URL}/clients/{client_id}/resend-invoice")
        print_result("Resend invoice", response.status_code)
        
        if response.status_code == 200:
            print(f"   Message: {response.json()['message']}")
            
    except Exception as e:
        print(f"❌ FAIL Resend invoice: {e}")
    
    # Test resend job summary
    try:
        response = requests.post(f"{BASE_URL}/clients/{client_id}/resend-job-summary")
        print_result("Resend job summary", response.status_code)
        
        if response.status_code == 200:
            print(f"   Message: {response.json()['message']}")
            
    except Exception as e:
        print(f"❌ FAIL Resend job summary: {e}")

def test_archive_client(client_id):
    """Test archiving a client"""
    print_section("ARCHIVE TEST")
    
    if not client_id:
        print("❌ SKIP Archive client: No client ID provided")
        return
    
    try:
        response = requests.delete(f"{BASE_URL}/clients/{client_id}")
        print_result("Archive client", response.status_code)
        
        if response.status_code == 200:
            print(f"   Message: {response.json()['message']}")
            
    except Exception as e:
        print(f"❌ FAIL Archive client: {e}")

def main():
    """Run all tests"""
    print("🧪 WhisperWorkPro API Test Suite")
    print(f"Testing server at: {BASE_URL}")
    print(f"Started at: {datetime.now().isoformat()}")
    
    try:
        # Basic health checks
        test_health()
        
        # Client management tests
        print_section("CLIENT MANAGEMENT TESTS")
        client_id = test_create_client()
        test_duplicate_client()
        test_get_clients()
        test_update_client(client_id)
        
        # Advanced feature tests
        test_search_clients()
        test_client_history(client_id)
        test_resend_features(client_id)
        
        # Cleanup
        test_archive_client(client_id)
        
        print_section("TEST SUMMARY")
        print("✅ All tests completed successfully!")
        print("\nYour WhisperWorkPro API is ready for production! 🚀")
        print(f"API Documentation: {BASE_URL}/docs")
        
    except requests.exceptions.ConnectionError:
        print_section("CONNECTION ERROR")
        print("❌ Cannot connect to the API server")
        print(f"   Make sure the server is running at: {BASE_URL}")
        print("   Start the server with: uvicorn main:app --host 0.0.0.0 --port 10000 --reload")
        
    except Exception as e:
        print_section("UNEXPECTED ERROR")
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()