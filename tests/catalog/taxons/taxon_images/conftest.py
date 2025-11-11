import pytest

from src.data.taxon_images import generate_taxon_images_data
from src.services.call_request.taxon_images_call import TaxonImagesCall
from src.data.taxons import generate_taxons_data
from src.resources.payloads.taxons_payload import TaxonsPayload
from src.services.call_request.taxons_call import TaxonsCall

@pytest.fixture(scope="module")
def view_taxon_images(auth_headers):
    payload_taxon = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    taxon = TaxonsCall.create(auth_headers, payload_taxon)

    created_images = []
    for img_type in ["logo", "banner"]:
        payload = generate_taxon_images_data(type=img_type)
        response = TaxonImagesCall.create(auth_headers, taxon["code"], payload)
        response_json = response.json()
        created_images.append(response_json)

    yield auth_headers, taxon, created_images

    for image in created_images:
        if "id" in image:
            TaxonImagesCall.delete(auth_headers, taxon["code"], image["id"])
        else:
            print(f"TaxonImage sin 'id': {image}")
    TaxonsCall.delete(auth_headers, taxon["code"])

@pytest.fixture(scope="module")
def view_taxon_images_empty(auth_headers):
    payload_taxon = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    taxon = TaxonsCall.create(auth_headers, payload_taxon)

    yield auth_headers, taxon

    TaxonsCall.delete(auth_headers, taxon["code"])

@pytest.fixture(scope="function")
def add_taxon_image(auth_headers):
    payload = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    taxon = TaxonsCall.create(auth_headers, payload)
    created_taxon_images = []

    yield auth_headers, created_taxon_images, taxon

    for taxon_image in created_taxon_images:
        if 'id' in taxon_image:
            TaxonImagesCall.delete(auth_headers, taxon["code"], taxon_image["id"])
        else:
            print(f"TaxonImage no tiene 'id': {taxon_image}")

    TaxonsCall.delete(auth_headers, taxon["code"])

@pytest.fixture(scope="function")
def update_taxon_image(auth_headers):
    payload_taxon = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    taxon = TaxonsCall.create(auth_headers, payload_taxon)
    payload_image = generate_taxon_images_data(type="logo")
    response = TaxonImagesCall.create(auth_headers, taxon["code"], payload_image)
    response_json = response.json()
    
    yield auth_headers, taxon, response_json
    
    if "id" in response_json:
        TaxonImagesCall.delete(auth_headers, taxon["code"], response_json["id"])
    
    TaxonsCall.delete(auth_headers, taxon["code"])