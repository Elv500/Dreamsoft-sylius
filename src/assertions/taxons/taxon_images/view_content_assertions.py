import pytest

IMAGE_PREFIX = "/api/v2/admin/taxons/"
IMAGE_ITEM_PREFIX = "/api/v2/admin/taxons/"

class AssertionTaxonImagesContent:

    @staticmethod
    def assert_taxon_images_collection(response_json, params=None):
        try:
            members = response_json.get("hydra:member", [])
            assert isinstance(members, list), "'hydra:member' no es lista"
            ids = [it["id"] for it in members]
            assert len(ids) == len(set(ids)), "Hay IDs duplicados en taxon images"

            for it in members:
                AssertionTaxonImagesContent.assert_taxon_image_item(it)
            if params:
                AssertionTaxonImagesContent._assert_pagination(response_json, params)

        except AssertionError as e:
            pytest.fail(f"[TaxonImagesCollection] {e}")

    @staticmethod
    def assert_taxon_images_collection_empty(response_json):
        try:
            assert response_json.get("hydra:totalItems", 0) == 0, "Se esperaban 0 imágenes"
            assert response_json.get("hydra:member", []) == [], "hydra:member debería estar vacío"
        except AssertionError as e:
            pytest.fail(f"[TaxonImagesEmpty] {e}")

    @staticmethod
    def assert_taxon_image_item(item, expected_id=None, expected_owner=None):
        try:
            assert item["@id"].startswith(IMAGE_PREFIX), f"@id inesperado: {item['@id']}"
            assert item["@type"] == "TaxonImage", f"@type inesperado: {item['@type']}"
            assert item["id"] > 0, "id debe ser > 0"
            assert isinstance(item["type"], str), "type debe ser cadena"
            assert item["path"].startswith("http"), "path debe ser una URL válida"
            assert item["owner"].startswith(IMAGE_PREFIX), f"owner URI inesperada: {item['owner']}"

            if expected_id is not None:
                assert item["id"] == expected_id, f"id esperado {expected_id}, encontrado {item['id']}"
            if expected_owner is not None:
                assert expected_owner in item["owner"], f"owner esperado '{expected_owner}', encontrado '{item['owner']}'"
        except AssertionError as e:
            pytest.fail(f"[TaxonImageItem] {e}")

    @staticmethod
    def _assert_pagination(response_json, params):
        try:
            items = params.get("itemsPerPage")
            page = params.get("page", 1)
            if items is None:
                return

            if "hydra:member" in response_json and items == 0:
                assert len(response_json["hydra:member"]) == 0, \
                    "itemsPerPage=0 debería devolver 0 items"

            expected_base = "images?itemsPerPage=" + str(items)
            if items != 0:
                expected_base += f"&page={page}"

            view = response_json.get("hydra:view", {})
            assert "@id" in view, "hydra:view.@id ausente"
            assert expected_base in view["@id"], \
                f"hydra:view.@id no coincide con base esperada: {view.get('@id')}"

        except AssertionError as e:
            pytest.fail(f"[TaxonImagesPagination] {e}")
