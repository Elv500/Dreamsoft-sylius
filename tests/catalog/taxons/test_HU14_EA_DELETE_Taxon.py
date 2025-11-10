import pytest

from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.schema_assertion import AssertionTaxons
from src.assertions.taxons.update_content_assertions import AssertionTaxonUpdateContent
from src.assertions.taxons.error_assertion import AssertionTaxonsError
from src.data.taxons import generate_taxons_data
from utils.logger_helpers import log_request_response

def test_TC149_Eliminar_taxon_existente_con_code_valido(delete_taxon):
    headers, taxon = delete_taxon
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response)

def test_TC150_Validar_error_al_eliminar_taxon_inexistente(delete_taxon):
    headers, _ = delete_taxon
    url = TaxonsEndpoint.taxon_code("inexistente")
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionTaxonsError.assert_taxons_error_request(response.json(), 404, "Not Found")

def test_TC152_Validar_error_al_eliminar_taxon_sin_code(delete_taxon):
    headers, _ = delete_taxon
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_405(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 405, "Method Not Allowed")

def test_TC152_Validar_error_al_eliminar_taxon_sin_autenticacion(delete_taxon):
    headers, taxon = delete_taxon
    headers = {}
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "JWT Token not found")

def test_TC153_Validar_error_al_eliminar_taxon_con_token_invalido(delete_taxon):
    headers, taxon = delete_taxon
    headers = {"Authorization": "Bearer invalid_token"}
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "Invalid JWT Token")

def test_TC154_Validar_error_al_intentar_eliminar_dos_veces_el_mismo_taxon(delete_taxon):
    headers, taxon = delete_taxon
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    responseFirst = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(responseFirst)
    responseSecond = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_404(responseSecond)
    AssertionTaxonsError.assert_taxons_error_request(responseSecond.json(), 404, "Not Found")

def test_TC155_Verificar_que_un_taxon_eliminado_no_exista_mas(delete_taxon):
    headers, taxon = delete_taxon
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    responseDelete = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(responseDelete)
    responseGet = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_404(responseGet)
    AssertionTaxonsError.assert_taxons_error_request(responseGet.json(), 404, "Not Found")