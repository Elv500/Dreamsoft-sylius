import pytest

from src.services.call_request.taxon_images_call import TaxonImagesCall
from src.routes.taxon_images_endpoint import TaxonImagesEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.data.taxon_images import generate_taxon_images_data
from src.assertions.taxons.taxon_images.add_content_assertions import AssertionTaxonImagesContent
from src.assertions.taxons.taxon_images.schema_assertion import AssertionTaxonImages
from src.assertions.taxons.taxon_images.error_assertion import AssertionTaxonImagesError
from utils.logger_helpers import log_request_response


@pytest.mark.functional_positive
@pytest.mark.smoke
def test_TC173_Agregar_imagen_a_un_taxon_existente(add_taxon_image):
    headers, created_taxon_images, taxon = add_taxon_image
    payload = generate_taxon_images_data(type="logo")
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    response_json = response.json()
    AssertionTaxonImagesContent.assert_taxon_image_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxonImages.assert_add_output_schema(response_json)
    AssertionTaxonImagesContent.assert_taxon_image_response(payload, response_json)
    log_request_response(response.url, response, headers, payload)
    created_taxon_images.append(response_json)


@pytest.mark.functional_positive
def test_TC180_Agregar_mas_de_una_imagen_a_un_taxon_existente(add_taxon_image):
    headers, created_taxon_images, taxon = add_taxon_image
    payloadOne = generate_taxon_images_data(type="logo")
    responseOne = TaxonImagesCall.create(headers, taxon["code"], payloadOne)
    responseOne_json = responseOne.json()
    AssertionStatusCode.assert_status_code_201(responseOne)
    AssertionTaxonImages.assert_add_output_schema(responseOne_json)
    log_request_response(responseOne.url, responseOne, headers, payloadOne)
    payloadTwo = generate_taxon_images_data(type="banner")
    responseTwo = TaxonImagesCall.create(headers, taxon["code"], payloadTwo)
    responseTwo_json = responseTwo.json()
    AssertionStatusCode.assert_status_code_201(responseTwo)
    AssertionTaxonImages.assert_add_output_schema(responseTwo_json)
    log_request_response(responseTwo.url, responseOne, headers, payloadTwo)
    created_taxon_images.append(responseOne_json)
    created_taxon_images.append(responseTwo_json)


@pytest.mark.functional_negative
def test_TC174_Validar_error_al_agregar_imagen_a_un_taxon_inexistente(add_taxon_image):
    headers, created_taxon_images, _ = add_taxon_image
    payload = generate_taxon_images_data(type="logo")
    url = TaxonImagesEndpoint.taxon_images("inexistente")
    response = TaxonImagesCall.create(headers, url, payload)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 404, "Not Found")
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_negative
def test_TC175_Validar_error_al_agregar_imagen_sin_autenticacion(add_taxon_image):
    headers, created_taxon_images, taxon = add_taxon_image
    headers = {}
    payload = generate_taxon_images_data(type="logo")
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 401, "JWT Token not found")
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_negative
def test_TC176_Validar_error_al_agregar_imagen_con_token_invalido(add_taxon_image):
    headers, created_taxon_images, taxon = add_taxon_image
    headers = {"Authorization": "Bearer invalid_token"}
    payload = generate_taxon_images_data(type="logo")
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonImagesError.assert_taxon_images_error(response.json(), 401, "Invalid JWT Token")
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_positive
def test_TC177_Agregar_imagen_a_un_taxon_con_solo_campo_requerido(add_taxon_image):
    headers, created_taxon_images, taxon = add_taxon_image
    payload = generate_taxon_images_data()
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    response_json = response.json()
    AssertionTaxonImagesContent.assert_taxon_image_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxonImages.assert_add_output_schema(response_json)
    AssertionTaxonImagesContent.assert_taxon_image_response(payload, response_json)
    log_request_response(response.url, response, headers, payload)
    created_taxon_images.append(response_json)

@pytest.mark.functional_positive
@pytest.mark.domain
@pytest.mark.parametrize("file", [
    "test_image_jpeg_valid.jpeg",
    "test_image_valid.png",
    "test_image_jpg_valid.jpg",
    "test_image_gif_valid.gif",
    "test_image_svg_valid.svg"
])
def test_TC_Agregar_imagen_con_extension_valida_a_un_taxon(add_taxon_image, file):
    headers, created_taxon_images, taxon = add_taxon_image
    payload = generate_taxon_images_data(file=file)
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    response_json = response.json()
    AssertionTaxonImagesContent.assert_taxon_image_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxonImages.assert_add_output_schema(response_json)
    AssertionTaxonImagesContent.assert_taxon_image_response(payload, response_json)
    log_request_response(response.url, response, headers, payload)
    created_taxon_images.append(response_json)


@pytest.mark.functional_negative
@pytest.mark.domain
@pytest.mark.parametrize("file", [
    pytest.param("test_image_csv_invalid.csv", marks=pytest.mark.xfail(reason="BUG-179: Permite subir imagen a un taxon con extension csv invalida", run=True)),
    pytest.param("test_image_xlsx_invalid.xlsx", marks=pytest.mark.xfail(reason="BUG-501: Permite subir imagen a un taxon con extension xlsx invalida", run=True)),
    pytest.param("test_image_docx_invalid.docx", marks=pytest.mark.xfail(reason="BUG-502: Permite subir imagen a un taxon con extension docx invalida", run=True)),
    pytest.param("test_image_pdf_invalid.pdf", marks=pytest.mark.xfail(reason="BUG-503: Permite subir imagen a un taxon con extension pdf invalida", run=True))
])
def test_TC_Agregar_imagen_con_extension_invalida_a_un_taxon(add_taxon_image, file):
    headers, created_taxon_images, taxon = add_taxon_image
    payload = generate_taxon_images_data(file=file)
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_positive
def test_TC504_Agregar_imagen_a_un_taxon_con_un_peso_minimo_de_1KB(add_taxon_image):
    headers, created_taxon_images, taxon = add_taxon_image
    payload = generate_taxon_images_data(file="test_image_1KB.png")
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    response_json = response.json()
    AssertionTaxonImagesContent.assert_taxon_image_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxonImages.assert_add_output_schema(response_json)
    AssertionTaxonImagesContent.assert_taxon_image_response(payload, response_json)
    log_request_response(response.url, response, headers, payload)
    created_taxon_images.append(response_json)


@pytest.mark.functional_positive
def test_TC505_Agregar_imagen_a_un_taxon_con_un_peso_maximo_de_2MB(add_taxon_image):
    headers, created_taxon_images, taxon = add_taxon_image
    payload = generate_taxon_images_data(file="test_image_2MB.jpg")
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    response_json = response.json()
    AssertionTaxonImagesContent.assert_taxon_image_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxonImages.assert_add_output_schema(response_json)
    AssertionTaxonImagesContent.assert_taxon_image_response(payload, response_json)
    log_request_response(response.url, response, headers, payload)
    created_taxon_images.append(response_json)


@pytest.mark.functional_negative
def test_TC506_Validar_error_al_agregar_imagen_a_un_taxon_con_un_peso_mayor_de_2MB(add_taxon_image):
    headers, created_taxon_images, taxon = add_taxon_image
    payload = generate_taxon_images_data(file="test_image_mayor2MB.jpg")
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    response_json = response.json()
    AssertionTaxonImagesContent.assert_taxon_image_payload(payload)
    AssertionStatusCode.assert_status_code_500(response)
    AssertionTaxonImagesError.assert_taxon_images_error_request(response.json(), 500, "Internal Server Error")
    log_request_response(response.url, response, headers, payload)


@pytest.mark.functional_positive
def test_TC185_Agregar_imagen_a_un_taxon_con_campo_tipo_con_cero_caracteres(add_taxon_image):
    headers, created_taxon_images, taxon = add_taxon_image
    payload = generate_taxon_images_data(type="")
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    response_json = response.json()
    AssertionTaxonImagesContent.assert_taxon_image_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxonImages.assert_add_output_schema(response_json)
    AssertionTaxonImagesContent.assert_taxon_image_response(payload, response_json)
    log_request_response(response.url, response, headers, payload)
    created_taxon_images.append(response_json)


@pytest.mark.functional_positive
def test_TC507_Agregar_imagen_a_un_taxon_con_campo_tipo_con_255_caracteres(add_taxon_image):
    headers, created_taxon_images, taxon = add_taxon_image
    payload = generate_taxon_images_data(type="a" * 255)
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    response_json = response.json()
    AssertionTaxonImagesContent.assert_taxon_image_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxonImages.assert_add_output_schema(response_json)
    AssertionTaxonImagesContent.assert_taxon_image_response(payload, response_json)
    log_request_response(response.url, response, headers, payload)
    created_taxon_images.append(response_json)


@pytest.mark.functional_negative
def test_TC186_Validar_error_al_agregar_imagen_a_un_taxon_con_campo_tipo_con_256_caracteres(add_taxon_image):
    headers, created_taxon_images, taxon = add_taxon_image
    payload = generate_taxon_images_data(type="a" * 256)
    response = TaxonImagesCall.create(headers, taxon["code"], payload)
    AssertionStatusCode.assert_status_code_500(response)
    AssertionTaxonImagesError.assert_taxon_images_error_request(response.json(), 500, "Internal Server Error")
    log_request_response(response.url, response, headers, payload)