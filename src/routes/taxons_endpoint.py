from src.routes.endpoint import Endpoint
from src.config.config import BASE_URL

class TaxonsEndpoint:

    @classmethod
    def taxon(cls):
        return f"{BASE_URL}{Endpoint.BASE_TAXONS.value}"
    
    @staticmethod
    def build_taxon_code(base, code):
        return f"{BASE_URL}{base.format(code=code)}"
    
    @classmethod
    def taxon_code(cls, code):
        return f"{BASE_URL}{Endpoint.BASE_TAXONS_CODE.value.format(code=code)}"