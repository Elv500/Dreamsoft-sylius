import requests
from src.routes.taxon_images_endpoint import TaxonImagesEndpoint
from src.services.request import SyliusRequest

class TaxonImagesCall:

    @classmethod
    def view(cls, headers, taxon_code, image_code):
        response = SyliusRequest.get(TaxonImagesEndpoint.taxon_image_code(taxon_code, image_code), headers)
        return response.json()

    @classmethod
    def create(cls, headers, taxon_code, payload):
        url = TaxonImagesEndpoint.taxon_images(taxon_code)
        files, data = payload
        headers = headers.copy()
        response = requests.post(url, headers=headers, files=files, data=data)
        files["file"].close()
        return response

    @classmethod
    def update(cls, headers, taxon_code, image_code, payload):
        response = SyliusRequest.put(TaxonImagesEndpoint.taxon_image_code(taxon_code, image_code), headers, payload)
        return response.json()
    
    @classmethod
    def delete(cls, headers, taxon_code, image_code):
        response = SyliusRequest.delete(TaxonImagesEndpoint.taxon_image_code(taxon_code, image_code), headers)
        return response