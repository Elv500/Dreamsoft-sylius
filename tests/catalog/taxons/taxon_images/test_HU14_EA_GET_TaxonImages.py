import pytest
from src.services.request import SyliusRequest
from src.routes.taxon_images_endpoint import TaxonImagesEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.taxon_images.schema_assertion import AssertionTaxonImages
from src.assertions.taxons.taxon_images.view_content_assertions import AssertionTaxonImagesContent
from src.assertions.taxons.taxon_images.error_assertion import AssertionTaxonImagesError
from utils.logger_helpers import log_request_response


@pytest.mark.functional_positive
@pytest.mark.smoke
def test_TC163_Obtener_lista_imagenes_sin_imagenes_asociadas(view_taxon_images_empty):
    headers, taxon = view_taxon_images_empty
    url = TaxonImagesEndpoint.taxon_images(taxon["code"])
    response = SyliusRequest.get(url, headers)

    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxonImages.assert_list_schema(response_json)
    AssertionTaxonImagesContent.assert_taxon_images_collection_empty(response_json)
    log_request_response(url, response, headers)


@pytest.mark.functional_positive
def test_TC162_Obtener_lista_imagenes_con_imagenes_existentes(view_taxon_images):
    headers, taxon, created_images = view_taxon_images
    url = TaxonImagesEndpoint.taxon_images(taxon["code"])
    response = SyliusRequest.get(url, headers)

    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxonImages.assert_list_schema(response_json)
    AssertionTaxonImagesContent.assert_taxon_images_collection(response_json)
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC164_Listar_imagenes_sin_autenticacion(view_taxon_images):
    _, taxon, _ = view_taxon_images
    headers = {}
    url = TaxonImagesEndpoint.taxon_images(taxon["code"])
    response = SyliusRequest.get(url, headers)

    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 401, "JWT Token not found")
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
def test_TC165_Listar_imagenes_con_token_invalido(view_taxon_images):
    _, taxon, _ = view_taxon_images
    headers = {"Authorization": "Bearer invalid_token"}
    url = TaxonImagesEndpoint.taxon_images(taxon["code"])
    response = SyliusRequest.get(url, headers)

    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 401, "Invalid JWT Token")
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
@pytest.mark.xfail(reason="BUG: El endpoint retorna 200 en lugar de 404 al listar imágenes de un taxon inexistente", run=True)
def test_TC166_Listar_imagenes_de_taxon_inexistente(view_taxon_images):
    headers, _, _ = view_taxon_images
    url = TaxonImagesEndpoint.taxon_images("taxon_inexistente")
    response = SyliusRequest.get(url, headers)

    AssertionStatusCode.assert_status_code_404(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 404, "Not Found")
    log_request_response(url, response, headers)


@pytest.mark.functional_positive
@pytest.mark.domain
@pytest.mark.parametrize("page, itemsPerPage", [
    (1, None),
    (1, 1),
    (1, 0)
])
def test_TC_Listar_imagenes_con_paginacion_valida(view_taxon_images, page, itemsPerPage):
    headers, taxon, _ = view_taxon_images
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = TaxonImagesEndpoint.taxon_images_with_params(taxon["code"], **params)
    response = SyliusRequest.get(url, headers)

    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxonImagesContent.assert_taxon_images_collection(response.json(), params=params)
    log_request_response(url, response, headers)


@pytest.mark.functional_negative
@pytest.mark.domain
@pytest.mark.parametrize("page, itemsPerPage", [
    (0, 1),
    (-1, 1),
    pytest.param(1.5, 1, marks=pytest.mark.xfail(reason="BUG-411: Al listar imagnes de un taxon acepta decimales en page", run=True)),
    ("uno", 1),
    (" ", 1),       
    (1, -1),
    pytest.param(1, 1.5, marks=pytest.mark.xfail(reason="BUG-415: Al listar imagnes de un taxon acepta decimales en itemsPerPage", run=True)),
    pytest.param(1, "uno", marks=pytest.mark.xfail(reason="BUG-416: Al listar imagnes de un taxon acepta string en itemsPerPage", run=True)),
    pytest.param(1, None, marks=pytest.mark.xfail(reason="BUG-417: Al listar imagnes de un taxon acepta itemsPerPage vacío", run=True))
])
def test_TC_Listar_imagenes_con_paginacion_invalida(view_taxon_images, page, itemsPerPage):
    headers, taxon, _ = view_taxon_images
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = TaxonImagesEndpoint.taxon_images_with_params(taxon["code"], **params)
    response = SyliusRequest.get(url, headers)

    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(url, response, headers)