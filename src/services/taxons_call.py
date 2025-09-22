from src.routes.taxons_endpoint import TaxonsEndpoint
from src.core.request import SyliusRequest

class TaxonsCall:

    @classmethod
    def view(cls, headers, code):
        response = SyliusRequest.get(TaxonsEndpoint.taxon_code(code), headers)
        return response.json()
    
    @classmethod
    def create(cls, headers, payload):
        response = SyliusRequest.post(TaxonsEndpoint.taxons(), headers, payload)
        return response.json()
    
    @classmethod
    def update(cls, headers, payload, code):
        response = SyliusRequest.put(TaxonsEndpoint.taxon_code(code), headers, payload)
        return response.json()
    
    @classmethod
    def delete(cls, headers, code):
        response = SyliusRequest().delete(TaxonsEndpoint.taxon_code(code), headers)
        return response