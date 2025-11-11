import pytest

from src.data.taxons import generate_taxons_data
from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.schema_assertion import AssertionTaxons
from src.assertions.taxons.add_content_assertions import AssertionTaxonContent
from src.assertions.taxons.error_assertion import AssertionTaxonsError
from utils.logger_helpers import log_request_response

def test_TC121_Crear_taxon_con_todos_los_campos_validos(add_taxon):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data()
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionTaxons.assert_add_output_schema(response_json)
    AssertionTaxonContent.assert_taxon_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

def test_TC122_Crear_taxon_con_solo_campos_requeridos(add_taxon):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data(required_only=True)
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload, required_only=True)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionTaxons.assert_add_output_schema(response_json)
    AssertionTaxonContent.assert_taxon_response(payload, response_json, required_only=True)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

def test_TC123_Validar_error_al_crear_taxon_sin_autenticacion():
    headers = {}
    payload = generate_taxons_data()
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "JWT Token not found")
    log_request_response(url, response, headers, payload)

def test_TC124_Validar_error_al_crear_taxon_con_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    payload = generate_taxons_data()
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "Invalid JWT Token")
    log_request_response(url, response, headers, payload)

@pytest.mark.parametrize("code",[
    "a",
    "a"*255,
    "code-test",
    "code_test"
])
def test_TC_Crear_taxon_con_code_valido(add_taxon, code):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data()
    payload["code"] = code
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionTaxons.assert_add_output_schema(response_json)
    AssertionTaxonContent.assert_taxon_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

@pytest.mark.parametrize("code, message", [
    ("", "code: Please enter taxon code."),
    ("a"*256, "code: The code must not be longer than 255 characters."),
    ("Test_#12/", "code: Taxon code can only be comprised of letters, numbers, dashes and underscores.")
])
def test_TC_Validar_error_al_crear_taxon_con_code_invalido(add_taxon, code, message):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data()
    payload["code"] = code
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxonsError.assert_taxons_error_request(response_json, 422, message)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

def test_TC128_Crear_taxon_con_referencia_de_taxon_padre_valido(add_taxon):
    headers, created_taxons = add_taxon
    payload_padre = generate_taxons_data()
    url = TaxonsEndpoint.taxon()
    response_padre = SyliusRequest.post(url, headers, payload_padre)
    response_padre_json = response_padre.json()
    payload_hijo = generate_taxons_data(parent=response_padre_json)
    url = TaxonsEndpoint.taxon()
    response_hijo = SyliusRequest.post(url, headers, payload_hijo)
    response_hijo_json = response_hijo.json()
    AssertionTaxons.assert_add_input_schema(payload_hijo)
    AssertionTaxonContent.assert_taxon_payload(payload_hijo)
    AssertionStatusCode.assert_status_code_201(response_hijo)
    AssertionTaxons.assert_add_output_schema(response_hijo_json)
    AssertionTaxonContent.assert_taxon_response(payload_hijo, response_hijo_json)
    log_request_response(url, response_padre, headers, payload_padre)
    log_request_response(url, response_hijo, headers, payload_hijo)
    created_taxons.append(response_padre_json)
    created_taxons.append(response_hijo_json)

def test_TC142_Crear_taxon_sin_referencia_de_taxon_padre(add_taxon):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data(parent={})
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxons.assert_add_output_schema(response_json)
    AssertionTaxonContent.assert_taxon_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

def test_TC129_Validar_error_al_crear_taxon_con_referencia_de_taxon_padre_invalido(add_taxon):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data(parent={"@id": "PARENT_INVALIDO"})
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionStatusCode.assert_status_code_400(response)
    AssertionTaxonsError.assert_taxons_error_request(response_json, 400, "PARENT_INVALIDO")
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

def test_TC133_Crear_taxon_con_estado_activado(add_taxon):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data(enabled=True)
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxons.assert_add_output_schema(response_json)
    AssertionTaxonContent.assert_taxon_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

def test_TC134_Crear_taxon_con_estado_desactivado(add_taxon):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data(enabled=False)
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxons.assert_add_output_schema(response_json)
    AssertionTaxonContent.assert_taxon_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

@pytest.mark.parametrize("name, slug", [
    ("a","a"),
    ("a","b"*255),
    ("a","test-slug"),
    ("a","test_slug"),
    ("a"*255,"a"),
    ("a"*255,"a"*255),
    ("a"*255,"test-slug"),
    ("a"*255,"test_slug")
])
def test_TC_Crear_traduccion_de_taxon_con_name_y_slug_valido(add_taxon, name, slug):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data()
    payload["translations"]["en_US"]["name"] = name
    payload["translations"]["en_US"]["slug"] = slug
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxons.assert_add_output_schema(response_json)
    AssertionTaxonContent.assert_taxon_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

@pytest.mark.parametrize("name, slug", [
    ("",""),
    ("","b"*256),
    ("","test slug"),
    ("","Test_#12/"),
    ("a"*256,""),
    ("a"*256,"a"*256),
    ("a"*256,"test slug"),
    ("a"*256,"Test_#12/")
])
def test_TC_Validar_error_al_crear_traduccion_de_taxon_con_name_y_slug_invalido(add_taxon, name, slug):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data()
    payload["translations"]["en_US"]["name"] = name
    payload["translations"]["en_US"]["slug"] = slug
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionStatusCode.assert_status_code_422(response)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

def test_TC385_Crear_taxon_con_mas_de_una_traduccion_valida(add_taxon):
    headers, created_taxons = add_taxon
    translations = {
            "es_ES": {
            "name": "Nombre espanol",
            "slug": "nombre-es",
            "description": "Descripción en español"
        }
    }
    payload = generate_taxons_data(extra_translations=translations)
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxons.assert_add_output_schema(response_json)
    AssertionTaxonContent.assert_taxon_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

def test_TC386_Crear_taxon_con_descripcion_en_traduccion(add_taxon):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data()
    payload["translations"]["en_US"]["description"] = "Descripción en ingles"
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxons.assert_add_output_schema(response_json)
    AssertionTaxonContent.assert_taxon_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)

def test_TC387_Crear_taxon_sin_descripcion_en_traduccion(add_taxon):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data()
    payload["translations"]["en_US"].pop("description")
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionTaxonContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxons.assert_add_output_schema(response_json)
    AssertionTaxonContent.assert_taxon_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_taxons.append(response_json)