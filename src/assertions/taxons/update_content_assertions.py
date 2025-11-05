import pytest

class AssertionTaxonUpdateContent:

    @staticmethod
    def assert_taxon_payload(payload):
        try:
            assert "code" not in payload, "El campo 'code' no debe incluirse en el payload PUT"

            if "translations" in payload:
                translations = payload["translations"]
                assert isinstance(translations, dict), "'translations' debe ser un objeto"

                for locale, cont_tr in translations.items():
                    assert cont_tr["name"].strip(), f"Campo 'name' vacío en {locale}"
                    assert cont_tr["slug"].strip(), f"Campo 'slug' vacío en {locale}"
                    if "description" in cont_tr:
                        assert cont_tr["description"].strip(), f"Description vacío en {locale}"

            if "parent" in payload:
                parent = payload["parent"]
                if parent is not None:
                    assert isinstance(parent, str) and parent.strip(), "Campo 'parent' vacío o inválido"

            if "position" in payload:
                position = payload["position"]
                assert isinstance(position, int) and position >= 0, "Position debe ser entero >= 0"

            if "enabled" in payload:
                assert isinstance(payload["enabled"], bool), "Campo 'enabled' debe ser booleano"

        except AssertionError as e:
            pytest.fail(f"[TaxonPutPayload] {e}")

    @staticmethod
    def assert_taxon_response(payload, response_json, expected_code):
        try:
            assert response_json["@context"].strip(), "Campo '@context' vacío"
            assert response_json["@id"].strip(), "Campo '@id' vacío"
            assert response_json["@type"] == "Taxon", "Tipo en response no es 'Taxon'"
            assert response_json["id"] > 0, "ID inválido en response"

            assert response_json["code"] == expected_code, \
                f"Code en response '{response_json['code']}' != esperado '{expected_code}'"

            # Validar campos actualizados (solo los que estaban en payload)
            if "enabled" in payload:
                assert response_json["enabled"] == payload["enabled"], \
                    "Campo 'enabled' no coincide con payload"

            if "parent" in payload:
                if payload["parent"] is None:
                    assert response_json["parent"] is None, "Parent debería ser None en response"
                else:
                    assert response_json["parent"] == payload["parent"], \
                        f"Parent en response '{response_json['parent']}' != payload '{payload['parent']}'"

            if "position" in payload:
                assert response_json["position"] == payload["position"], \
                    f"Position en response '{response_json['position']}' != payload '{payload['position']}'"

            if "translations" in payload:
                translations = response_json["translations"]
                for locale, expected_tr in payload["translations"].items():
                    assert locale in translations, f"Falta traducción '{locale}' en response"
                    tr = translations[locale]

                    for field in ["@id", "@type", "id", "name", "slug"]:
                        assert field in tr, f"Falta campo '{field}' en traducción {locale}"
                        assert str(tr[field]).strip(), f"Campo '{field}' vacío en traducción {locale}"

                    assert tr["@type"] == "TaxonTranslation", f"Tipo inválido en traducción {locale}"

                    for field in ["name", "slug"]:
                        assert tr[field] == expected_tr[field], \
                            f"En {locale}, '{field}' en response '{tr[field]}' != payload '{expected_tr[field]}'"

                    if "description" in expected_tr:
                        assert tr["description"] == expected_tr["description"], \
                            f"En {locale}, descripción distinta: '{tr['description']}' != '{expected_tr['description']}'"

        except AssertionError as e:
            pytest.fail(f"[TaxonPutResponse] {e}")