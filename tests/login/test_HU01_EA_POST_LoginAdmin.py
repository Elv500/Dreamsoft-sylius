import pytest

from src.routes.endpoint import Endpoint
from src.routes.request import SyliusRequest
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.login.schema_assertion import AssertionLogin
from utils.logger_helpers import log_request_response

@pytest.mark.parametrize("email, password", [
    ("api@example.com","sylius-api")
])
def test_TC_91_Autenticacion_exitosa_con_email_y_contrasena_validos(email, password):
    payload = {"email": email, "password": password}
    url = Endpoint.login()
    response = SyliusRequest.post(url, payload=payload)
    log_request_response(url, response, payload=payload)
    AssertionLogin.assert_input_schema(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionLogin.assert_output_schema(response.json())