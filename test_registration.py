import requests
import json

# Test registration
url = 'http://127.0.0.1:8000/api/auth/users/'
data = {
    'username': 'testuser',
    'password': 'testpassword123'
}

response = requests.post(url, json=data)
print(f'Status: {response.status_code}')
print(f'Response: {response.text}')