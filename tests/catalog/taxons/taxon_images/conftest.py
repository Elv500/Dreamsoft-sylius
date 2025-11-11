import pytest
from src.services.call_request.taxon_images_call import TaxonImagesCall

from src.data.taxons import generate_taxons_data
from src.resources.payloads.taxons_payload import TaxonsPayload
from src.services.call_request.taxons_call import TaxonsCall

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