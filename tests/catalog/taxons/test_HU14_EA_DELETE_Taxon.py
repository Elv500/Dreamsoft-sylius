import pytest

from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.error_assertion import AssertionTaxonsError
from utils.logger_helpers import log_request_response
from src.routes.taxon_images_endpoint import TaxonImagesEndpoint
from src.assertions.taxons.taxon_images.error_assertion import AssertionTaxonImagesError
from src.services.call_request.taxon_images_call import TaxonImagesCall


@pytest.mark.functional_positive
@pytest.mark.smoke
def test_TC149_Eliminar_taxon_existente_con_code_valido(delete_taxon):
    headers, taxon = delete_taxon
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response)
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC150_Validar_error_al_eliminar_taxon_inexistente(delete_taxon):
    headers, _ = delete_taxon
    url = TaxonsEndpoint.taxon_code("inexistente")
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionTaxonsError.assert_taxons_error_request(response.json(), 404, "Not Found")
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC151_Validar_error_al_eliminar_taxon_sin_code(delete_taxon):
    headers, _ = delete_taxon
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_405(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 405, "Method Not Allowed")
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC152_Validar_error_al_eliminar_taxon_sin_autenticacion(delete_taxon):
    headers, taxon = delete_taxon
    headers = {}
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "JWT Token not found")
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC153_Validar_error_al_eliminar_taxon_con_token_invalido(delete_taxon):
    headers, taxon = delete_taxon
    headers = {"Authorization": "Bearer invalid_token"}
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "Invalid JWT Token")
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC154_Validar_error_al_intentar_eliminar_dos_veces_el_mismo_taxon(delete_taxon):
    headers, taxon = delete_taxon
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    responseFirst = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(responseFirst)
    log_request_response(url, responseFirst, headers)
    responseSecond = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_404(responseSecond)
    AssertionTaxonsError.assert_taxons_error_request(responseSecond.json(), 404, "Not Found")
    log_request_response(url, responseSecond, headers)


@pytest.mark.functional_positive
def test_TC155_Verificar_que_un_taxon_eliminado_no_exista_mas(delete_taxon):
    headers, taxon = delete_taxon
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    responseDelete = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(responseDelete)
    log_request_response(url, responseDelete, headers)
    responseGet = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_404(responseGet)
    AssertionTaxonsError.assert_taxons_error_request(responseGet.json(), 404, "Not Found")
    log_request_response(url, responseGet, headers)


@pytest.mark.functional_positive
def test_TC156_Eliminar_taxon_con_imagen_asociada(delete_taxon_with_image):
    headers, taxon, image = delete_taxon_with_image
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response)
    log_request_response(url, response, headers)

    image_url = TaxonImagesEndpoint.taxon_image_code(taxon["code"], image["id"])
    response_get = SyliusRequest.get(image_url, headers)
    AssertionStatusCode.assert_status_code_404(response_get)
    AssertionTaxonImagesError.assert_taxon_images_error_request(response_get.json(), 404, "Not Found")
    log_request_response(url, response_get, headers)


@pytest.mark.functional_positive
def test_TC158_Verificar_imagen_de_taxon_eliminado_no_exista(delete_taxon_with_image):
    headers, taxon, image = delete_taxon_with_image
    url_delete = TaxonsEndpoint.taxon_code(taxon["code"])
    response_delete = SyliusRequest.delete(url_delete, headers)
    AssertionStatusCode.assert_status_code_204(response_delete)
    log_request_response(url_delete, response_delete, headers)

    url_image = TaxonImagesEndpoint.taxon_image_code(taxon["code"], image["id"])
    response_image = SyliusRequest.get(url_image, headers)
    AssertionStatusCode.assert_status_code_404(response_image)
    AssertionTaxonImagesError.assert_taxon_images_error_request(response_image.json(), 404, "Not Found")
    log_request_response(url_image, response_image, headers)


@pytest.mark.functional_positive
def test_TC157_Eliminar_taxon_sin_imagen_asociada(delete_taxon):
    headers, taxon = delete_taxon
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response)
    log_request_response(url, response, headers)


@pytest.mark.functional_positive
def test_TC159_Eliminar_taxon_con_taxones_hijos(delete_taxon_with_children):
    headers, padre, hijos = delete_taxon_with_children
    url_padre = TaxonsEndpoint.taxon_code(padre["code"])
    response = SyliusRequest.delete(url_padre, headers)
    AssertionStatusCode.assert_status_code_204(response)
    log_request_response(url_padre, response, headers)

    for hijo in hijos:
        url_hijo = TaxonsEndpoint.taxon_code(hijo["code"])
        response_get = SyliusRequest.get(url_hijo, headers)
        AssertionStatusCode.assert_status_code_404(response_get)
        AssertionTaxonsError.assert_taxons_error_request(response_get.json(), 404, "Not Found")
        log_request_response(url_hijo, response, headers)


@pytest.mark.functional_positive
def test_TC160_Verificar_taxones_hijos_de_padre_eliminado(delete_taxon_with_children):
    headers, padre, hijos = delete_taxon_with_children
    url_padre = TaxonsEndpoint.taxon_code(padre["code"])
    response_delete = SyliusRequest.delete(url_padre, headers)
    AssertionStatusCode.assert_status_code_204(response_delete)
    log_request_response(url_padre, response_delete, headers)

    for hijo in hijos:
        url_hijo = TaxonsEndpoint.taxon_code(hijo["code"])
        response_get = SyliusRequest.get(url_hijo, headers)
        AssertionStatusCode.assert_status_code_404(response_get)
        AssertionTaxonsError.assert_taxons_error_request(response_get.json(), 404, "Not Found")
        log_request_response(url_hijo, response_get, headers)


@pytest.mark.functional_positive
def test_TC161_Eliminar_taxon_sin_taxones_hijos_asociados(delete_taxon):
    headers, taxon = delete_taxon
    url = TaxonsEndpoint.taxon_code(taxon["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response)
    log_request_response(url, response, headers)