import requests
from src.config.conftest import auth_headers
import pytest

def test_prueba(auth_headers):

    url = "https://demo.sylius.com/api/v2/admin/taxons"

    headers = auth_headers
    response = requests.get(url, headers=headers)
    assert response.status_code == 200