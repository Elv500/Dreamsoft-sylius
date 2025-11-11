import pytest

class AssertionTaxonImagesUpdateContent:

    @staticmethod
    def assert_taxon_image_update_payload(payload):
        try:
            assert "file" not in payload, "El campo 'file' no debe incluirse en el payload PUT"
            assert "type" in payload, "Debe incluirse el campo 'type'"
            assert isinstance(payload["type"], str), "Campo 'type' debe ser string"
        except AssertionError as e:
            pytest.fail(f"[TaxonImagePutPayload] {e}")

    @staticmethod
    def assert_taxon_image_update_response(payload, response_json, expected_id, expected_owner):
        try:
            assert response_json["@context"].strip(), "Campo '@context' vacío"
            assert response_json["@id"].strip(), "Campo '@id' vacío"
            assert response_json["@type"] == "TaxonImage", "Tipo en response no es 'TaxonImage'"
            assert response_json["id"] == expected_id, f"ID esperado {expected_id}, obtenido {response_json['id']}"
            assert response_json["owner"].endswith(expected_owner), f"Owner inesperado: {response_json['owner']}"
            assert response_json["path"].startswith("http"), "Path no es una URL válida"

            if "type" in payload:
                assert response_json["type"] == payload["type"], (
                    f"Tipo en response '{response_json['type']}' != payload '{payload['type']}'"
                )
        except AssertionError as e:
            pytest.fail(f"[TaxonImagePutResponse] {e}")