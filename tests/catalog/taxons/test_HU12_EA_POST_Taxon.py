from src.data.taxons import generate_taxons_data
from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.schema_assertion import AssertionTaxons

def test_TC121_Crear_taxon_con_todos_los_campos_validos(add_taxon):
    headers, created_taxons = add_taxon
    payload = generate_taxons_data()
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.post(url, headers, payload)
    AssertionTaxons.assert_add_input_schema(payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionTaxons.assert_add_output_schema(response_json)
    created_taxons.append(response_json)