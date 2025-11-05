class TaxonsPayload:

    @staticmethod
    def build_payload_taxon(data):
        
        payload_taxon = {
            "code": data["code"],
            "translations": {
                "en_US": {
                    "name": data["translations"]["en_US"]["name"],
                    "slug": data["translations"]["en_US"]["slug"],
                    "description": data["translations"]["en_US"]["description"]
                }
            },
            "enabled": data["enabled"]
        }

        if "parent" in data:
            payload_taxon["parent"] = data["parent"]

        if "position" in data:
            payload_taxon["position"] = data["position"]

        return payload_taxon