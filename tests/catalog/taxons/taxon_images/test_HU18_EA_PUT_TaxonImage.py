import pytest

from src.services.call_request.taxon_images_call import TaxonImagesCall
from src.routes.taxon_images_endpoint import TaxonImagesEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.taxon_images.schema_assertion import AssertionTaxonImages
from src.assertions.taxons.taxon_images.error_assertion import AssertionTaxonImagesError
from src.assertions.taxons.taxon_images.update_content_assertions import AssertionTaxonImagesUpdateContent
from utils.logger_helpers import log_request_response


@pytest.mark.functional_positive
@pytest.mark.smoke
def test_TC181_Actualizar_imagen_asociado_de_un_taxon_existente(update_taxon_image):
    headers, taxon, image = update_taxon_image
    payload = {"type": "banner"}
    AssertionTaxonImagesUpdateContent.assert_taxon_image_update_payload(payload)
    response = TaxonImagesCall.update(headers, taxon["code"], image["id"], payload)
    response_json = response.json()
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxonImages.assert_update_output_schema(response_json)
    AssertionTaxonImagesUpdateContent.assert_taxon_image_update_response(payload, response_json, image["id"], taxon["code"])
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_negative
def test_TC182_Validar_error_al_actualizar_imagen_inexistente_de_un_taxon_existente(update_taxon_image):
    headers, taxon, _ = update_taxon_image
    payload = {"type": "banner"}
    response = TaxonImagesCall.update(headers, taxon["code"], 999999, payload)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionTaxonImagesError.assert_taxon_images_error_request(response.json(), 404, "Not Found")
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_negative
def test_TC183_Validar_error_al_actualizar_imagen_de_un_taxon_sin_token_de_autenticacion(update_taxon_image):
    _, taxon, image = update_taxon_image
    headers = {}
    payload = {"type": "banner"}
    response = TaxonImagesCall.update(headers, taxon["code"], image["id"], payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 401, "JWT Token not found")
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_negative
def test_TC184_Validar_error_al_actualizar_imagen_de_un_taxon_con_token_invalido(update_taxon_image):
    _, taxon, image = update_taxon_image
    headers = {"Authorization": "Bearer invalid_token"}
    payload = {"type": "banner"}
    response = TaxonImagesCall.update(headers, taxon["code"], image["id"], payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 401, "Invalid JWT Token")
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_positive
@pytest.mark.domain
@pytest.mark.parametrize("file", [
    pytest.param("test_image_jpeg_valid.jpeg", marks=pytest.mark.xfail(reason="BUG: Permite subir archivo valido en PUT", run=True)),
    pytest.param("test_image_valid.png", marks=pytest.mark.xfail(reason="BUG: Permite subir archivo valido en PUT", run=True)),
    pytest.param("test_image_jpg_valid.jpg", marks=pytest.mark.xfail(reason="BUG: Permite subir archivo valido en PUT", run=True)),
    pytest.param("test_image_gif_valid.gif", marks=pytest.mark.xfail(reason="BUG: Permite subir archivo valido en PUT", run=True)),
    pytest.param("test_image_svg_valid.svg", marks=pytest.mark.xfail(reason="BUG: Permite subir archivo valido en PUT", run=True)),
])
def test_TC_187_511_Validar_error_al_intentar_actualizar_archivo(update_taxon_image, file):
    headers, taxon, image = update_taxon_image
    payload = {"file": file, "type": "logo"}
    response = TaxonImagesCall.update(headers, taxon["code"], image["id"], payload)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_negative
@pytest.mark.domain
@pytest.mark.parametrize("file", [
    pytest.param("test_image_csv_invalid.csv", marks=pytest.mark.xfail(reason="BUG: Permite subir archivo invalido en PUT", run=True)),
    pytest.param("test_image_xlsx_invalid.xlsx", marks=pytest.mark.xfail(reason="BUG: Permite subir archivo invalido en PUT", run=True)),
    pytest.param("test_image_docx_invalid.docx", marks=pytest.mark.xfail(reason="BUG: Permite subir archivo invalido en PUT", run=True)),
    pytest.param("test_image_pdf_invalid.pdf", marks=pytest.mark.xfail(reason="BUG: Permite subir archivo invalido en PUT", run=True)),
])
def test_TC_188_514_Validar_error_al_actualizar_con_extension_invalida(update_taxon_image, file):
    headers, taxon, image = update_taxon_image
    payload = {"file": file, "type": "logo"}
    response = TaxonImagesCall.update(headers, taxon["code"], image["id"], payload)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_positive
@pytest.mark.domain
@pytest.mark.parametrize("type_value", [
    "",
    "a" * 255
])
def test_TC_518_519_Actualizar_imagen_con_tipo_valido(update_taxon_image, type_value):
    headers, taxon, image = update_taxon_image
    payload = {"type": type_value}
    AssertionTaxonImagesUpdateContent.assert_taxon_image_update_payload(payload)
    response = TaxonImagesCall.update(headers, taxon["code"], image["id"], payload)
    response_json = response.json()
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxonImages.assert_update_output_schema(response_json)
    AssertionTaxonImagesUpdateContent.assert_taxon_image_update_response(payload, response_json, image["id"], taxon["code"])
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_negative
def test_TC520_Validar_error_al_actualizar_imagen_con_tipo_de_256_caracteres(update_taxon_image):
    headers, taxon, image = update_taxon_image
    payload = {"type": "a" * 256}
    response = TaxonImagesCall.update(headers, taxon["code"], image["id"], payload)
    AssertionStatusCode.assert_status_code_500(response)
    AssertionTaxonImagesError.assert_taxon_images_error_request(response.json(), 500, "Internal Server Error")
    log_request_response(response.url, response, headers, payload)