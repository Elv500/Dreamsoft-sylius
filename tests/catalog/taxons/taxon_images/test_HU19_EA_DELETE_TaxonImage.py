import pytest

from src.services.request import SyliusRequest
from src.routes.taxon_images_endpoint import TaxonImagesEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.taxon_images.error_assertion import AssertionTaxonImagesError
from src.services.call_request.taxon_images_call import TaxonImagesCall
from src.services.call_request.taxons_call import TaxonsCall
from utils.logger_helpers import log_request_response


@pytest.mark.functional_positive
@pytest.mark.smoke
def test_TC191_Eliminar_imagen_existente_asociado_a_un_taxon_valido(delete_taxon_image):
    headers, taxon, image = delete_taxon_image
    url = TaxonImagesEndpoint.taxon_image_code(taxon["code"], image["id"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response)
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC192_Validar_error_al_eliminar_imagen_inexistente_en_un_taxon(delete_taxon_image):
    headers, taxon, _ = delete_taxon_image
    url = TaxonImagesEndpoint.taxon_image_code(taxon["code"], 999999)
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionTaxonImagesError.assert_taxon_images_error_request(response.json(), 404, "Not Found")
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC196_Validar_error_al_eliminar_imagen_sin_code(delete_taxon_image):
    headers, taxon, _ = delete_taxon_image
    url = TaxonImagesEndpoint.taxon_images(taxon["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_405(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 405, "Method Not Allowed")
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC193_Validar_error_al_eliminar_imagen_sin_token(delete_taxon_image):
    _, taxon, image = delete_taxon_image
    headers = {}
    url = TaxonImagesEndpoint.taxon_image_code(taxon["code"], image["id"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 401, "JWT Token not found")
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC194_Validar_error_al_eliminar_imagen_con_token_invalido(delete_taxon_image):
    _, taxon, image = delete_taxon_image
    headers = {"Authorization": "Bearer invalid_token"}
    url = TaxonImagesEndpoint.taxon_image_code(taxon["code"], image["id"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 401, "Invalid JWT Token")
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC195_Validar_error_al_eliminar_dos_veces_misma_imagen(delete_taxon_image):
    headers, taxon, image = delete_taxon_image
    url = TaxonImagesEndpoint.taxon_image_code(taxon["code"], image["id"])
    responseFirst = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(responseFirst)
    log_request_response(url, responseFirst, headers)

    responseSecond = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_404(responseSecond)
    AssertionTaxonImagesError.assert_taxon_images_error_request(responseSecond.json(), 404, "Not Found")
    log_request_response(url, responseSecond, headers)


@pytest.mark.functional_positive
def test_TC197_Verificar_que_una_imagen_eliminada_no_exista(delete_taxon_image):
    headers, taxon, image = delete_taxon_image
    url_delete = TaxonImagesEndpoint.taxon_image_code(taxon["code"], image["id"])
    responseDelete = SyliusRequest.delete(url_delete, headers)
    AssertionStatusCode.assert_status_code_204(responseDelete)
    log_request_response(url_delete, responseDelete, headers)

    url_get = TaxonImagesEndpoint.taxon_image_code(taxon["code"], image["id"])
    responseGet = SyliusRequest.get(url_get, headers)
    AssertionStatusCode.assert_status_code_404(responseGet)
    AssertionTaxonImagesError.assert_taxon_images_error_request(responseGet.json(), 404, "Not Found")
    log_request_response(url_get, responseGet, headers)