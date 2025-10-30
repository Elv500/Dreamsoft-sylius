from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.schema_assertion import AssertionTaxons
from src.assertions.taxons.update_content_assertions import AssertionTaxonUpdateContent
from src.assertions.taxons.error_assertion import AssertionTaxonsError
from src.data.taxons import generate_taxons_data

def test_TC135_Actualizar_taxon_existente_con_datos_validos(update_taxon):
    headers, taxon_padre, taxon_hijo = update_taxon
    url = TaxonsEndpoint.taxon_code(taxon_hijo["code"])
    responseBefore = SyliusRequest.get(url, headers)
    #loger before
    payload = generate_taxons_data(locale="es_ES")
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    AssertionTaxons.assert_update_input_schema(payload)
    AssertionTaxonUpdateContent.assert_taxon_payload(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxons.assert_update_output_schema(response_json)
    AssertionTaxonUpdateContent.assert_taxon_response(payload, response_json, taxon_hijo["code"])