from faker import Faker
import json
import re
fake = Faker()

def generate_taxons_data(required_only=False, parent=None, enabled=True):
    
    name = fake.words(nb=2, unique=True)
    name = " ".join(name).capitalize()
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip("-")

    taxons_data = {
        "code": slug,
        "translations": {
            "en_US": {
                "name": name,
                "slug": slug,
                "description": fake.paragraph()
            }
        }
    }

    if not required_only:
        taxons_data["enabled"] = enabled
        if parent:
            taxons_data["parent"] = parent["@id"]

    return taxons_data