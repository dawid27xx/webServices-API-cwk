import requests
import json

BASE_URL = "https://sc22ds.pythonanywhere.com/api"

# Valid login credentials
VALID_USERNAME = "dstep"
VALID_PASSWORD = "password"

# Test data
VALID_REGISTRATION = {"username": "newuser", "email": "newuser@example.com", "password": "SecurePass123"}
INVALID_REGISTRATION = [
    {"email": "newuser@example.com", "password": "SecurePass123"},  # Missing username
    {"username": "newuser", "password": "SecurePass123"},  # Missing email
    {"username": "newuser", "email": "invalid-email", "password": "SecurePass123"},  # Invalid email
    {"username": "dstep", "email": "existing@example.com", "password": "password"},  # Duplicate username
    {"username": "admin' --", "email": "admin@example.com", "password": "pass"}  # SQL injection attempt
]

VALID_RATING = {"professor_id": "DS1", "module_code": "PC1", "year": 2024, "semester": 2, "rating": 5}
INVALID_RATING = [
    {"professor_id": "DS1", "module_code": "PC1", "year": 2024, "semester": 2, "rating": 6},  # Out of range
    {"professor_id": "DS1", "module_code": "PC1", "year": 2024, "semester": 2, "rating": 0},  # Out of range
    {"professor_id": "XX1", "module_code": "PC1", "year": 2024, "semester": 2, "rating": 5},  # Invalid professor
    {"professor_id": "DS1", "module_code": "XYZ", "year": 2024, "semester": 2, "rating": 5},  # Invalid module
    {"professor_id": "DS1", "module_code": "PC1", "year": "twenty", "semester": 2, "rating": 5},  # Invalid year
    {"professor_id": "DS1", "module_code": "PC1", "year": 2024, "semester": "spring", "rating": 5},  # Invalid semester
]


def test_registration():
    print("Testing Registration...")
    for data in INVALID_REGISTRATION:
        response = requests.post(f"{BASE_URL}/register/", json=data)
        print(f"Input: {data} | Status: {response.status_code} | Response: {response.json()}")
    
    response = requests.post(f"{BASE_URL}/register/", json=VALID_REGISTRATION)
    print(f"Valid Registration | Status: {response.status_code} | Response: {response.json()}")


def test_login():
    print("Testing Login...")
    valid_data = {"username": VALID_USERNAME, "password": VALID_PASSWORD}
    response = requests.post(f"{BASE_URL}/login/", json=valid_data)
    print(f"Valid Login | Status: {response.status_code} | Response: {response.json()}")
    
    invalid_data = {"username": "fakeuser", "password": "password"}
    response = requests.post(f"{BASE_URL}/login/", json=invalid_data)
    print(f"Invalid Login | Status: {response.status_code} | Response: {response.json()}")


def test_list_instances():
    print("Testing List Instances...")
    response = requests.get(f"{BASE_URL}/list/")
    print(f"Status: {response.status_code} | Response: {response.json()}")


def test_view_ratings():
    print("Testing View Ratings...")
    response = requests.get(f"{BASE_URL}/view/")
    print(f"Status: {response.status_code} | Response: {response.json()}")


def test_average_rating():
    print("Testing Average Rating...")
    response = requests.get(f"{BASE_URL}/average/DS1/PC1/")
    print(f"Valid Query | Status: {response.status_code} | Response: {response.json()}")
    
    response = requests.get(f"{BASE_URL}/average/XX1/PC1/")
    print(f"Invalid Professor | Status: {response.status_code} | Response: {response.json()}")


def test_submit_rating():
    print("Testing Submit Rating...")
    for data in INVALID_RATING:
        response = requests.post(f"{BASE_URL}/rate/", json=data)
        print(f"Input: {data} | Status: {response.status_code} | Response: {response.json()}")
    
    response = requests.post(f"{BASE_URL}/rate/", json=VALID_RATING)
    print(f"Valid Rating | Status: {response.status_code} | Response: {response.json()}")


def run_tests():
    test_registration()
    test_login()
    test_list_instances()
    test_view_ratings()
    test_average_rating()
    test_submit_rating()


if __name__ == "__main__":
    run_tests()