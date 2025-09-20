import pytest

from src.routes.endpoint import Endpoint
from src.routes.request import SyliusRequest
from src.assertions.status_code_assertion import AssertionStatusCode

@pytest.mark.parametrize("email, password", [
    ("api@example.com","sylius-api"),
    ("sylius@example.com","sylius")
])
def test_TC_91_Autenticacion_exitosa_con_email_y_contrasena_validos(email, password):
    payload = {"email": email, "password": password}
    url = Endpoint.login()
    response = SyliusRequest.post(url, payload=payload)
    AssertionStatusCode.assert_status_code_200(response)
    