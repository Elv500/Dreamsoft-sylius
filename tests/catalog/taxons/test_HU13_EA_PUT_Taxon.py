import pytest

from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.schema_assertion import AssertionTaxons
from src.assertions.taxons.update_content_assertions import AssertionTaxonUpdateContent
from src.assertions.taxons.error_assertion import AssertionTaxonsError
from src.data.taxons import generate_taxons_data
from utils.logger_helpers import log_request_response

def test_TC135_Actualizar_taxon_existente_con_datos_validos(update_taxon):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    responseBefore = SyliusRequest.get(url, headers)
    log_request_response(url, responseBefore, headers)
    payload = generate_taxons_data(locale="es_ES")
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionTaxonUpdateContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxons.assert_update_output_schema(response_json)
    AssertionTaxonUpdateContent.assert_taxon_response(payload, response_json, taxon_hijo["code"])
    log_request_response(url, response, headers, payload)

def test_TC136_Validar_error_al_actualizar_taxon_inexistente(update_taxon):
    headers, _, _ = update_taxon
    code = "inexistente"
    url = TaxonsEndpoint.taxon_code(code)
    payload = generate_taxons_data(locale="es_ES")
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionTaxonsError.assert_taxons_error_request(response.json(), 404, "Not Found")
    log_request_response(url, response, headers, payload)

def test_TC137_Validar_error_al_actualizar_taxon_sin_code(update_taxon):
    headers, _, _ = update_taxon
    url = TaxonsEndpoint.taxon()
    payload = generate_taxons_data(locale="es_ES")
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionStatusCode.assert_status_code_405(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 405, "Method Not Allowed")
    log_request_response(url, response, headers, payload)

def test_TC138_Validar_error_al_actualizar_taxon_sin_autenticacion(update_taxon):
    headers_auth, taxon_padre, taxon_hijo = update_taxon
    headers = {}
    payload = generate_taxons_data(locale="es_ES")
    payload.pop("code")
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    response = SyliusRequest.put(url, headers, payload)
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionTaxonUpdateContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "JWT Token not found")
    log_request_response(url, response, headers, payload)

def test_TC139_Validar_error_al_actualizar_taxon_con_token_invalido(update_taxon):
    headers_auth, taxon_padre, taxon_hijo = update_taxon
    headers = {"Authorization": "Bearer invalid_token"}
    payload = generate_taxons_data(locale="es_ES")
    payload.pop("code")
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    response = SyliusRequest.put(url, headers, payload)
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionTaxonUpdateContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "Invalid JWT Token")
    log_request_response(url, response, headers, payload)

def test_TC140_Actualizar_taxon_con_referencia_de_taxon_padre_valido(update_taxon):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    payload = generate_taxons_data(parent=taxon_padre, locale="es_ES")
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionTaxonUpdateContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxons.assert_update_output_schema(response_json)
    AssertionTaxonUpdateContent.assert_taxon_response(payload, response_json, taxon_hijo["code"])
    log_request_response(url, response, headers, payload)

def test_TC145_Actualizar_taxon_sin_referencia_de_taxon_padre(update_taxon):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_padre["code"])
    payload = generate_taxons_data(locale="es_ES")
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionTaxonUpdateContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxons.assert_update_output_schema(response_json)
    AssertionTaxonUpdateContent.assert_taxon_response(payload, response_json, taxon_padre["code"])
    log_request_response(url, response, headers, payload)

def test_TC141_Validar_error_al_actualizar_taxon_con_referencia_de_taxon_padre_invalido(update_taxon):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    payload = generate_taxons_data(parent={"@id": "parent_invalido"}, locale="es_ES")
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionStatusCode.assert_status_code_400(response)
    AssertionTaxonsError.assert_taxons_error_request(response_json, 400, "Invalid IRI")
    log_request_response(url, response, headers, payload)

@pytest.mark.parametrize("position", [
    (0),
    (1)
])
def test_TC_Actualizar_taxon_con_posicion_valida(update_taxon, position):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    payload = generate_taxons_data(locale="es_ES", position=position)
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionTaxonUpdateContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxons.assert_update_output_schema(response_json)
    log_request_response(url, response, headers, payload)

@pytest.mark.parametrize("position", [
    (1.5),
    pytest.param(-1, marks=pytest.mark.xfail(reason="BUG: Permite actualizar taxon con posición negativa", run=True))
])
def test_TC_Validar_error_al_actualizar_taxon_con_posicion_invalida(update_taxon, position):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    payload = generate_taxons_data(locale="es_ES", position=position)
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    AssertionStatusCode.assert_status_code_400(response)
    AssertionTaxonsError.assert_taxons_error_request(response_json, status=400, detail="The type of the \"position\" attribute must be \"int\", \"double\" given.")
    log_request_response(url, response, headers, payload)

def test_TC148_Actualizar_taxon_con_estado_activado(update_taxon):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    payload = generate_taxons_data(locale="es_ES", enabled=True)
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionTaxonUpdateContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxons.assert_update_output_schema(response_json)
    AssertionTaxonUpdateContent.assert_taxon_response(payload, response_json, taxon_hijo["code"])
    log_request_response(url, response, headers, payload)

@pytest.mark.xfail(reason="BUG: No permite actualizar una traduccion existente")
def test_TC146_Actualizar_traduccion_existente_de_un_taxon(update_taxon):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    payload = generate_taxons_data(locale="en_US")
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionTaxonUpdateContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxons.assert_update_output_schema(response_json)
    AssertionTaxonUpdateContent.assert_taxon_response(payload, response_json, taxon_hijo["code"])
    log_request_response(url, response, headers, payload)

def test_TC147_Actualizar_agregando_traduccion_nueva_a_taxon(update_taxon):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    payload = generate_taxons_data(locale="es_ES")
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionTaxonUpdateContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxons.assert_update_output_schema(response_json)
    AssertionTaxonUpdateContent.assert_taxon_response(payload, response_json, taxon_hijo["code"])
    log_request_response(url, response, headers, payload)

@pytest.mark.parametrize("name, slug", [
    ("a","a"),
    ("b","b"*255),
    ("c","test-slug"),
    ("d","test_slug"),
    ("e"*255,"c"),
    ("f"*255,"d"*255),
    ("g"*255,"test-slug"),
    ("h"*255,"test_slug")
])
def test_TC_Actualizar_traduccion_de_taxon_con_name_y_slug_valido(update_taxon, name, slug):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    payload = generate_taxons_data(locale="es_ES")
    payload.pop("code")
    payload["translations"]["es_ES"]["name"] = name
    payload["translations"]["es_ES"]["slug"] = slug
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionTaxonUpdateContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxons.assert_update_output_schema(response_json)
    AssertionTaxonUpdateContent.assert_taxon_response(payload, response_json, taxon_hijo["code"])
    log_request_response(url, response, headers, payload)

@pytest.mark.parametrize("name, slug", [
    ("",""),
    ("","a"*256),
    ("","test slug"),
    ("","Test_#12/"),
    ("b"*256,""),
    ("c"*256,"f"*256),
    ("d"*256,"test slug"),
    ("e"*256,"Test_#12/")
])
def test_TC_Validar_error_al_actualizar_traduccion_de_taxon_con_name_y_slug_invalido(update_taxon, name, slug):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    payload = generate_taxons_data(locale="es_ES")
    payload.pop("code")
    payload["translations"]["es_ES"]["name"] = name
    payload["translations"]["es_ES"]["slug"] = slug
    response = SyliusRequest.put(url, headers, payload)
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionStatusCode.assert_status_code_422(response)
    log_request_response(url, response, headers, payload)