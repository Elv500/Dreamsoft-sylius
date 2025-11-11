import pytest
from src.services.request import SyliusRequest
from src.routes.taxon_images_endpoint import TaxonImagesEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.taxon_images.schema_assertion import AssertionTaxonImages
from src.assertions.taxons.taxon_images.view_content_assertions import AssertionTaxonImagesContent
from src.assertions.taxons.taxon_images.error_assertion import AssertionTaxonImagesError
from utils.logger_helpers import log_request_response

def test_TC169_Obtener_imagen_existente_por_ID(view_taxon_images):
    headers, taxon, created_images = view_taxon_images
    image = created_images[0]
    url = TaxonImagesEndpoint.taxon_image_code(taxon["code"], image["id"])
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxonImages.assert_code_schema(response_json)
    AssertionTaxonImagesContent.assert_taxon_image_item(response_json, expected_id=image["id"], expected_owner=taxon["code"])
    log_request_response(url, response, headers)

@pytest.mark.xfail(reason="BUG: El endpoint retorna 200 en lugar de 404 al consultar imagen inexistente", run=True)
def test_TC170_Validar_error_al_obtener_imagen_inexistente_en_taxon_valido(view_taxon_images):
    headers, taxon, _ = view_taxon_images
    url = TaxonImagesEndpoint.taxon_image_code(taxon["code"], 999999)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 404, "Not Found")
    log_request_response(url, response, headers)


def test_TC171_Validar_error_al_obtener_imagen_de_un_taxon_sin_token_de_autenticacion(view_taxon_images):
    _, taxon, created_images = view_taxon_images
    image = created_images[0]
    headers = {}
    url = TaxonImagesEndpoint.taxon_image_code(taxon["code"], image["id"])
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 401, "JWT Token not found")
    log_request_response(url, response, headers)

def test_TC172_Validar_error_al_obtener_imagen_de_un_taxon_con_token_invalido(view_taxon_images):
    _, taxon, created_images = view_taxon_images
    image = created_images[0]
    headers = {"Authorization": "Bearer invalid_token"}
    url = TaxonImagesEndpoint.taxon_image_code(taxon["code"], image["id"])
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 401, "Invalid JWT Token")
    log_request_response(url, response, headers)

@pytest.mark.parametrize("invalid_id", [
    0,        
    "uno",    
    -1,
    2.5     
])
def test_TC_418_421_Validar_error_al_obtener_imagen_con_ID_invalido(view_taxon_images, invalid_id):
    headers, taxon, _ = view_taxon_images
    url = TaxonImagesEndpoint.taxon_image_code(taxon["code"], invalid_id)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_404(response)
    log_request_response(url, response, headers)