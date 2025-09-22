from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode

def test_TCXX_Obtener_taxons(view_taxon):
    headers, taxon1, taxon2 = view_taxon
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)