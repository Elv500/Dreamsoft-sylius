from enum import Enum
from src.config.config import BASE_URL


class Endpoint(Enum):

    LOGIN = "/api/v2/admin/administrators/token"

    BASE_INVENTORY = "/api/v2/admin/inventory-sources"
    BASE_INVENTORY_CODE = "/api/v2/admin/inventory-sources/{code}"

    @classmethod
    def login(cls):
        return f"{BASE_URL}{cls.LOGIN.value}"