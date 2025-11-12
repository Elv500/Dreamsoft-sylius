import pytest
from pathlib import Path

class AssertionTaxonImagesContent:

    @staticmethod
    def assert_taxon_image_payload(payload):
        try:
            files, data = payload

            assert "file" in files, "El campo 'file' es obligatorio en files"
            file_obj = files["file"]

            if isinstance(file_obj, (str, Path)):
                assert Path(file_obj).exists(), f"El archivo '{file_obj}' no existe"
            else:
                assert hasattr(file_obj, "read"), "El objeto 'file' no es legible"

            if data:
                assert isinstance(data, dict), "El campo 'data' debe ser un diccionario"
                if "type" in data:
                    assert isinstance(data["type"], str), "El campo 'type' debe ser texto"
                    assert data["type"].strip(), "El campo 'type' no puede estar vacío"

        except AssertionError as e:
            pytest.fail(f"[TaxonImagePayload] {e}")

    @staticmethod
    def assert_taxon_image_response(payload, response_json):
        try:
            files, data = payload

            assert response_json["@context"].strip(), "Campo '@context' vacío"
            assert response_json["@id"].strip(), "Campo '@id' vacío"
            assert response_json["@type"] == "TaxonImage", "Tipo incorrecto en response"
            assert response_json["id"] > 0, "ID inválido en response"
            assert "path" in response_json, "Falta campo 'path' en response"
            assert response_json["path"].strip(), "Campo 'path' vacío en response"

            if data and "type" in data:
                expected_type = data["type"]
                actual_type = response_json.get("type", None)
                assert actual_type == expected_type, (
                    f"Campo 'type' en response '{actual_type}' "
                    f"no coincide con el payload '{expected_type}'"
                )

        except AssertionError as e:
            pytest.fail(f"[TaxonImageResponse] {e}")