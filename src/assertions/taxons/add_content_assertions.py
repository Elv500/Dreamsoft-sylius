# src/assertions/taxons_content_assertion.py
import pytest

class AssertionTaxonContent:

    @staticmethod
    def assert_taxon_payload(payload, required_only=False):
        try:
            assert payload["code"].strip(), "Campo 'code' vacío"

            translations = payload["translations"]
            assert "en_US" in translations, "Falta traducción en_US"

            for code_tr, cont_tr in translations.items():
                assert cont_tr["name"].strip(), f"Campo 'name' vacío en {code_tr}"
                assert cont_tr["slug"].strip(), f"Campo 'slug' vacío en {code_tr}"
                if "description" in cont_tr:
                    assert cont_tr["description"].strip(), f"Description vacío en {code_tr}"

            if not required_only:
                if "parent" in payload and payload["parent"] is not None:
                    assert payload["parent"].strip(), "Campo 'parent' vacío"

        except AssertionError as e:
            pytest.fail(f"[TaxonPayload] {e}")

    @staticmethod
    def assert_taxon_response(payload, response_json, required_only=False):
        try:
            assert response_json["@context"].strip(), "Campo '@context' vacío"
            assert response_json["@id"].strip(), "Campo '@id' vacío"
            assert response_json["@type"] == "Taxon", "Tipo en response no es 'Taxon'"
            assert response_json["id"] > 0, "ID inválido en response"

            assert response_json["code"] == payload["code"], \
                f"Code en response '{response_json['code']}' != payload '{payload['code']}'"
            
            assert response_json["children"] == [], "Taxon padre deberia estar vacío"
            assert response_json["images"] == [], "Taxon recien creado no puede tener imagenes"

            if required_only:
                assert response_json["parent"] is None, "Parent debería ser None en modo requerido"
                assert response_json["position"] >= 0, f"Position debería iniciar en 0 {response_json["position"]}"
            else:
                assert response_json["enabled"] == payload["enabled"], \
                    "Campo 'enabled' no coincide con el payload"
                
                if "parent" in payload and payload["parent"] is not None:
                    assert response_json["parent"] == payload["parent"], \
                        f"Parent en response '{response_json['parent']}' != payload '{payload['parent']}'"
                else:
                    assert response_json["parent"] is None, "Parent inesperado en response"

            translations = response_json["translations"]
            assert "en_US" in translations, "Falta traducción en_US en response"

            for locale, tr in translations.items():
                for field in ["@id", "@type", "id", "name", "slug"]:
                    assert field in tr, f"Falta campo '{field}' en traducción {locale}"
                    assert str(tr[field]).strip(), f"Campo '{field}' vacío en traducción {locale}"

                assert tr["@type"] == "TaxonTranslation", f"Tipo inválido en traducción {locale}"

                if locale in payload.get("translations", {}):
                    expected = payload["translations"][locale]
                    for field in ["name", "slug"]:
                        assert tr[field] == expected[field], \
                            f"En {locale}, '{field}' en response '{tr[field]}' != payload '{expected[field]}'"

                    if "description" in expected:
                        assert tr["description"] == expected["description"], \
                            f"En {locale}, description distinta: '{tr['description']}' != '{expected['description']}'"
                        
        except AssertionError as e:
            pytest.fail(f"[TaxonResponse] {e}")