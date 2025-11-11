from src.routes.endpoint import Endpoint
from src.config.config import BASE_URL

class TaxonImagesEndpoint:

    @classmethod
    def taxon_images(cls, code):
        return f"{BASE_URL}{Endpoint.BASE_TAXONS_IMAGES.value.format(code=code)}"

    @classmethod
    def taxon_image_code(cls, taxon_code, image_code):
        return f"{BASE_URL}{Endpoint.BASE_TAXONS_IMAGES_CODE.value.format(code=taxon_code, imageCode=image_code)}"