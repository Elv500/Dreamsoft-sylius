from src.data.taxon_images import generate_taxon_images_data

class TaxonImagesEndpoint:

    @staticmethod
    def build_taxon_image_payload(file=None, type=None):
        files, data = generate_taxon_images_data(file, type)
        return files, data