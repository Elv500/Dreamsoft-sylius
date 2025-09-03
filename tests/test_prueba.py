import requests
import json

def test_prueba():
    url = "https://demo.sylius.com/api/v2/admin/administrators/token"

    payload = json.dumps({
    "email": "api@example.com",
    "password": "sylius-api"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    assert response.status_code == 200