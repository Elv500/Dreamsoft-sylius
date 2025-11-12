import pytest
from src.data.taxons import generate_taxons_data
from src.resources.payloads.taxons_payload import TaxonsPayload
from src.services.call_request.taxons_call import TaxonsCall

from src.data.taxon_images import generate_taxon_images_data
from src.services.call_request.taxon_images_call import TaxonImagesCall

@pytest.fixture(scope="module")
def view_taxon(auth_headers):
    payload_taxon1 = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    payload_taxon2 = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    taxon1 = TaxonsCall.create(auth_headers, payload_taxon1)
    taxon2 = TaxonsCall.create(auth_headers, payload_taxon2)
    
    yield auth_headers, taxon1, taxon2

    TaxonsCall.delete(auth_headers, taxon1["code"])
    TaxonsCall.delete(auth_headers, taxon2["code"])

@pytest.fixture(scope="function")
def add_taxon(auth_headers):
    created_taxons = []
    yield auth_headers, created_taxons

    for taxon in created_taxons:
        if 'code' in taxon:
            TaxonsCall.delete(auth_headers, taxon['code'])
        else:
            print(f"Taxon no tiene 'code': {taxon}")

@pytest.fixture(scope="class")
def update_taxon(auth_headers):
    payload_padre = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    taxon_padre = TaxonsCall.create(auth_headers, payload_padre)
    payload_hijo = TaxonsPayload.build_payload_taxon(generate_taxons_data(parent=taxon_padre))
    taxon_hijo = TaxonsCall.create(auth_headers, payload_hijo)
    
    yield auth_headers, taxon_padre, taxon_hijo

    TaxonsCall.delete(auth_headers, taxon_padre["code"])
    TaxonsCall.delete(auth_headers, taxon_hijo["code"])

@pytest.fixture(scope="function")
def delete_taxon(auth_headers):
    payload = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    taxon = TaxonsCall.create(auth_headers, payload)
    
    yield auth_headers, taxon

    TaxonsCall.delete(auth_headers, taxon["code"])

@pytest.fixture(scope="function")
def delete_taxon_with_children(auth_headers):
    payload_padre = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    taxon_padre = TaxonsCall.create(auth_headers, payload_padre)

    payload_hijo1 = TaxonsPayload.build_payload_taxon(generate_taxons_data(parent=taxon_padre))
    payload_hijo2 = TaxonsPayload.build_payload_taxon(generate_taxons_data(parent=taxon_padre))
    taxon_hijo1 = TaxonsCall.create(auth_headers, payload_hijo1)
    taxon_hijo2 = TaxonsCall.create(auth_headers, payload_hijo2)

    yield auth_headers, taxon_padre, [taxon_hijo1, taxon_hijo2]

    for hijo in [taxon_hijo1, taxon_hijo2]:
        try:
            TaxonsCall.delete(auth_headers, hijo["code"])
        except Exception as e:
            print(f"No se pudo eliminar hijo {hijo.get('code')}: {e}")

    try:
        TaxonsCall.delete(auth_headers, taxon_padre["code"])
    except Exception as e:
        print(f"No se pudo eliminar padre {taxon_padre.get('code')}: {e}")


@pytest.fixture(scope="function")
def delete_taxon_with_image(auth_headers):
    payload_taxon = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    taxon = TaxonsCall.create(auth_headers, payload_taxon)

    payload_image = generate_taxon_images_data(type="logo")
    response = TaxonImagesCall.create(auth_headers, taxon["code"], payload_image)
    response_json = response.json()

    yield auth_headers, taxon, response_json

    if "id" in response_json:
        TaxonImagesCall.delete(auth_headers, taxon["code"], response_json["id"])
    TaxonsCall.delete(auth_headers, taxon["code"])

@pytest.fixture(scope="function")
def view_taxon_with_image(auth_headers):
    payload_taxon = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    taxon = TaxonsCall.create(auth_headers, payload_taxon)

    payload_image = generate_taxon_images_data(type="logo")
    response = TaxonImagesCall.create(auth_headers, taxon["code"], payload_image)
    image_json = response.json()

    yield auth_headers, taxon, image_json

    try:
        if "id" in image_json:
            TaxonImagesCall.delete(auth_headers, taxon["code"], image_json["id"])
    except Exception:
        pass
    try:
        TaxonsCall.delete(auth_headers, taxon["code"])
    except Exception:
        pass


@pytest.fixture(scope="function")
def view_taxon_with_children(auth_headers):
    parent_payload = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    parent = TaxonsCall.create(auth_headers, parent_payload)

    if "@id" not in parent:
        parent["@id"] = f"/api/v2/admin/taxons/{parent['code']}"

    child_payload = TaxonsPayload.build_payload_taxon(generate_taxons_data(parent=parent))
    child = TaxonsCall.create(auth_headers, child_payload)

    yield auth_headers, parent, child

    try:
        TaxonsCall.delete(auth_headers, child["code"])
    except Exception:
        pass
    try:
        TaxonsCall.delete(auth_headers, parent["code"])
    except Exception:
        pass