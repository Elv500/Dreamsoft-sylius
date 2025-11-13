import pytest

from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.schema_assertion import AssertionTaxons
from src.assertions.taxons.view_content_assertions import AssertionTaxonsContent
from src.assertions.taxons.error_assertion import AssertionTaxonsError
from utils.logger_helpers import log_request_response


@pytest.mark.functional_positive
@pytest.mark.smoke
def test_TC106_Obtener_lista_de_taxones(view_taxon):
    headers, _, _ = view_taxon
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxons.assert_list_schema(response_json)
    AssertionTaxonsContent.assert_taxons_collection(response_json)
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC107_Listar_taxones_sin_autenticacion():
    headers = {}
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "JWT Token not found")
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC108_Listar_taxones_con_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "Invalid JWT Token")
    log_request_response(url, response, headers)


@pytest.mark.domain
@pytest.mark.functional_positive
@pytest.mark.parametrize("page, itemsPerPage", [
    (1, None),
    (1, 1),
    (1, 0)
])
def test_TC_Obtener_lista_de_taxones_con_paginacion_valida(view_taxon, page, itemsPerPage):
    headers, _, _ = view_taxon
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = TaxonsEndpoint.taxons_with_params(**params)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxonsContent.assert_taxons_collection(response.json(), params=params)
    log_request_response(url, response, headers)


@pytest.mark.domain
@pytest.mark.functional_negative
@pytest.mark.parametrize("page, itemsPerPage", [
    (0, 1),
    (-1, 1),
    pytest.param(1.5, 1, marks=pytest.mark.xfail(reason="BUG-360: Al listar taxons con parámetro page acepta decimales y rompe la URL", run=True)),
    ("uno", 1),
    (" ", 1),
    (1, -1),
    pytest.param(1, 1.5, marks=pytest.mark.xfail(reason="BUG-364: Al listar taxons con parámetro itemsPerPage puede ser decimal rompiendo la URL", run=True)),
    pytest.param(1, "uno", marks=pytest.mark.xfail(reason="BUG-365: Al listar taxons con parámetro itemsPerPage puede ser string rompiendo la URL", run=True)),
    pytest.param(1, None, marks=pytest.mark.xfail(reason="BUG-366: Al listar taxons con parámetro itemsPerPage puede ser vacío rompiendo la URL", run=True))
])
def test_TC_Obtener_lista_de_taxones_con_paginacion_invalida(view_taxon, page, itemsPerPage):
    headers, _, _ = view_taxon
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = TaxonsEndpoint.taxons_with_params(**params)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(url, response, headers)