from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.schema_assertion import AssertionTaxons
from src.assertions.taxons.view_content_assertions import AssertionTaxonsContent


def test_TC111_Obtener_taxon_por_code_existente(view_taxon):
    headers, taxon1, _ = view_taxon
    code = taxon1["code"]
    url = TaxonsEndpoint.taxon_code(code)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxons.assert_code_schema(response_json)
    AssertionTaxonsContent.assert_taxon_item(response_json, expected_code=code)

