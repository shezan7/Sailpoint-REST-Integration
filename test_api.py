"""
Test script for IAM REST API
Run this script after starting the Flask app to test the API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(response, endpoint):
    """Helper function to print response"""
    print(f"\n{'='*60}")
    print(f"Endpoint: {endpoint}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print(f"{'='*60}")

def test_api():
    """Test all API endpoints"""
    
    print("\n" + "="*60)
    print("IAM REST API - Integration Test")
    print("="*60)
    
    # ==================== USER TESTS ====================
    print("\n\n### TESTING USER ENDPOINTS ###\n")
    
    # 1. Get all users (should be empty initially)
    print("\n1. Get all users (initially empty)")
    response = requests.get(f"{BASE_URL}/api/users")
    print_response(response, "GET /api/users")
    
    # 2. Create User 1
    print("\n2. Create User 1")
    user1_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "is_enabled": True
    }
    response = requests.post(f"{BASE_URL}/api/users", json=user1_data)
    print_response(response, "POST /api/users")
    user1_id = response.json()['id']
    print(f"Created User ID: {user1_id}")
    
    # 3. Create User 2
    print("\n3. Create User 2")
    user2_data = {
        "username": "alice_smith",
        "email": "alice@example.com",
        "is_enabled": True
    }
    response = requests.post(f"{BASE_URL}/api/users", json=user2_data)
    print_response(response, "POST /api/users")
    user2_id = response.json()['id']
    print(f"Created User ID: {user2_id}")
    
    # 4. Create User 3
    print("\n4. Create User 3")
    user3_data = {
        "username": "bob_wilson",
        "email": "bob@example.com",
        "is_enabled": True
    }
    response = requests.post(f"{BASE_URL}/api/users", json=user3_data)
    print_response(response, "POST /api/users")
    user3_id = response.json()['id']
    print(f"Created User ID: {user3_id}")
    
    # 5. Get all users
    print("\n5. Get all users")
    response = requests.get(f"{BASE_URL}/api/users")
    print_response(response, "GET /api/users")
    
    # 6. Get single user
    print(f"\n6. Get single user (ID: {user1_id})")
    response = requests.get(f"{BASE_URL}/api/users/{user1_id}")
    print_response(response, f"GET /api/users/{user1_id}")
    
    # 7. Update user
    print(f"\n7. Update user (ID: {user1_id})")
    update_data = {
        "email": "john.doe@example.com"
    }
    response = requests.put(f"{BASE_URL}/api/users/{user1_id}", json=update_data)
    print_response(response, f"PUT /api/users/{user1_id}")
    
    # 8. Disable user
    print(f"\n8. Disable user (ID: {user2_id})")
    response = requests.patch(f"{BASE_URL}/api/users/{user2_id}/disable")
    print_response(response, f"PATCH /api/users/{user2_id}/disable")
    
    # 9. Enable user
    print(f"\n9. Enable user (ID: {user2_id})")
    response = requests.patch(f"{BASE_URL}/api/users/{user2_id}/enable")
    print_response(response, f"PATCH /api/users/{user2_id}/enable")
    
    # ==================== GROUP TESTS ====================
    print("\n\n### TESTING GROUP ENDPOINTS ###\n")
    
    # 1. Create Group 1
    print("\n1. Create Group 1")
    group1_data = {
        "name": "Administrators",
        "description": "Admin Group"
    }
    response = requests.post(f"{BASE_URL}/api/groups", json=group1_data)
    print_response(response, "POST /api/groups")
    group1_id = response.json()['id']
    print(f"Created Group ID: {group1_id}")
    
    # 2. Create Group 2
    print("\n2. Create Group 2")
    group2_data = {
        "name": "Developers",
        "description": "Development Team"
    }
    response = requests.post(f"{BASE_URL}/api/groups", json=group2_data)
    print_response(response, "POST /api/groups")
    group2_id = response.json()['id']
    print(f"Created Group ID: {group2_id}")
    
    # 3. Create Group 3
    print("\n3. Create Group 3")
    group3_data = {
        "name": "QA Engineers",
        "description": "Quality Assurance Team"
    }
    response = requests.post(f"{BASE_URL}/api/groups", json=group3_data)
    print_response(response, "POST /api/groups")
    group3_id = response.json()['id']
    print(f"Created Group ID: {group3_id}")
    
    # 4. Get all groups
    print("\n4. Get all groups")
    response = requests.get(f"{BASE_URL}/api/groups")
    print_response(response, "GET /api/groups")
    
    # 5. Get single group
    print(f"\n5. Get single group (ID: {group1_id})")
    response = requests.get(f"{BASE_URL}/api/groups/{group1_id}")
    print_response(response, f"GET /api/groups/{group1_id}")
    
    # 6. Update group
    print(f"\n6. Update group (ID: {group2_id})")
    update_data = {
        "description": "Senior Development Team"
    }
    response = requests.put(f"{BASE_URL}/api/groups/{group2_id}", json=update_data)
    print_response(response, f"PUT /api/groups/{group2_id}")
    
    # ==================== USER-GROUP RELATIONSHIP TESTS ====================
    print("\n\n### TESTING USER-GROUP RELATIONSHIP ENDPOINTS ###\n")
    
    # 1. Assign group to user
    print(f"\n1. Assign group {group1_id} to user {user1_id}")
    response = requests.post(f"{BASE_URL}/api/users/{user1_id}/groups/{group1_id}")
    print_response(response, f"POST /api/users/{user1_id}/groups/{group1_id}")
    
    # 2. Assign another group to same user
    print(f"\n2. Assign group {group2_id} to user {user1_id}")
    response = requests.post(f"{BASE_URL}/api/users/{user1_id}/groups/{group2_id}")
    print_response(response, f"POST /api/users/{user1_id}/groups/{group2_id}")
    
    # 3. Assign group to user 2
    print(f"\n3. Assign group {group2_id} to user {user2_id}")
    response = requests.post(f"{BASE_URL}/api/users/{user2_id}/groups/{group2_id}")
    print_response(response, f"POST /api/users/{user2_id}/groups/{group2_id}")
    
    # 4. Assign group to user 3
    print(f"\n4. Assign group {group3_id} to user {user3_id}")
    response = requests.post(f"{BASE_URL}/api/users/{user3_id}/groups/{group3_id}")
    print_response(response, f"POST /api/users/{user3_id}/groups/{group3_id}")
    
    # 5. Get user groups
    print(f"\n5. Get groups for user {user1_id}")
    response = requests.get(f"{BASE_URL}/api/users/{user1_id}/groups")
    print_response(response, f"GET /api/users/{user1_id}/groups")
    
    # 6. Get group members
    print(f"\n6. Get members of group {group2_id}")
    response = requests.get(f"{BASE_URL}/api/groups/{group2_id}/members")
    print_response(response, f"GET /api/groups/{group2_id}/members")
    
    # 7. Remove group from user
    print(f"\n7. Remove group {group1_id} from user {user1_id}")
    response = requests.delete(f"{BASE_URL}/api/users/{user1_id}/groups/{group1_id}")
    print_response(response, f"DELETE /api/users/{user1_id}/groups/{group1_id}")
    
    # 8. Verify removal - Get user groups again
    print(f"\n8. Verify removal - Get groups for user {user1_id}")
    response = requests.get(f"{BASE_URL}/api/users/{user1_id}/groups")
    print_response(response, f"GET /api/users/{user1_id}/groups")
    
    # ==================== ERROR HANDLING TESTS ====================
    print("\n\n### TESTING ERROR HANDLING ###\n")
    
    # 1. Get non-existent user
    print("\n1. Get non-existent user (ID: 999)")
    response = requests.get(f"{BASE_URL}/api/users/999")
    print_response(response, "GET /api/users/999")
    
    # 2. Create duplicate username
    print("\n2. Try to create user with duplicate username")
    duplicate_data = {
        "username": "john_doe",
        "email": "different@example.com"
    }
    response = requests.post(f"{BASE_URL}/api/users", json=duplicate_data)
    print_response(response, "POST /api/users (duplicate username)")
    
    # 3. Create duplicate group name
    print("\n3. Try to create group with duplicate name")
    duplicate_group = {
        "name": "Administrators",
        "description": "Another Admin Group"
    }
    response = requests.post(f"{BASE_URL}/api/groups", json=duplicate_group)
    print_response(response, "POST /api/groups (duplicate name)")
    
    # ==================== DELETE TESTS ====================
    print("\n\n### TESTING DELETE OPERATIONS ###\n")
    
    # 1. Delete user
    print(f"\n1. Delete user (ID: {user3_id})")
    response = requests.delete(f"{BASE_URL}/api/users/{user3_id}")
    print_response(response, f"DELETE /api/users/{user3_id}")
    
    # 2. Delete group
    print(f"\n2. Delete group (ID: {group3_id})")
    response = requests.delete(f"{BASE_URL}/api/groups/{group3_id}")
    print_response(response, f"DELETE /api/groups/{group3_id}")
    
    # 3. Final state - Get all users
    print("\n3. Final state - Get all users")
    response = requests.get(f"{BASE_URL}/api/users")
    print_response(response, "GET /api/users")
    
    # 4. Final state - Get all groups
    print("\n4. Final state - Get all groups")
    response = requests.get(f"{BASE_URL}/api/groups")
    print_response(response, "GET /api/groups")
    
    print("\n\n" + "="*60)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to the Flask application.")
        print("Make sure the Flask app is running at http://localhost:5000")
        print("\nTo start the application, run:")
        print("  python app_python1.py")
    except Exception as e:
        print(f"\nERROR: {str(e)}")
