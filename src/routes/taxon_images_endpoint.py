from src.routes.endpoint import Endpoint
from src.config.config import BASE_URL

class TaxonImagesEndpoint:

    @classmethod
    def taxon_images(cls, code):
        return f"{BASE_URL}{Endpoint.BASE_TAXONS_IMAGES.value.format(code=code)}"

    @classmethod
    def taxon_image_code(cls, taxon_code, image_code):
        return f"{BASE_URL}{Endpoint.BASE_TAXONS_IMAGES_CODE.value.format(code=taxon_code, imageCode=image_code)}"
    
    @classmethod
    def taxon_images_with_params(cls, code: str, **params) -> str:
        base_url = f"{BASE_URL}{Endpoint.BASE_TAXONS_IMAGES.value.format(code=code)}"
        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url