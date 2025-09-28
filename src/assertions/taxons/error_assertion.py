import pytest

class AssertionTaxonsError:

    @staticmethod
    def assert_taxons_error(response_json, code, message):
        try:
            assert "code" in response_json, '"code" no está en la respuesta'
            assert "message" in response_json, '"message" no está en la respuesta'
            assert response_json["code"] == code, "Codigo de error no coincide"
            assert response_json["message"] == message, "Mensaje de error no coincide"
        except AssertionError as e:
            pytest.fail(f"[TaxonsError Errors] {e}")