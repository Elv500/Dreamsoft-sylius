from src.assertions.schemas_assertions import AssertionSchemas

class AssertionTaxonImages:
     MODULE = "taxons/taxon_images"

     @staticmethod
     def assert_list_schema(response):
          return AssertionSchemas().validate_json_schema(response, "images_list_schema.json", AssertionTaxonImages.MODULE)
    
     @staticmethod
     def assert_code_schema(response):
          return AssertionSchemas().validate_json_schema(response, "image_code_schema.json", AssertionTaxonImages.MODULE)
     
     @staticmethod
     def assert_add_output_schema(response):
          return AssertionSchemas().validate_json_schema(response, "image_add_output.json", AssertionTaxonImages.MODULE)
     
     @staticmethod
     def assert_update_output_schema(response):
          return AssertionSchemas().validate_json_schema(response, "image_update_output_schema.json", AssertionTaxonImages.MODULE)