from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.schema_assertion import AssertionTaxons
from src.assertions.taxons.view_content_assertions import AssertionTaxonsContent


def test_TC106_Obtener_lista_de_taxones(view_taxon):
    headers, _, _ = view_taxon
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxons.assert_list_schema(response_json)
    AssertionTaxonsContent.assert_taxons_collection(response_json) #Revisar esquema y ya agregar individual