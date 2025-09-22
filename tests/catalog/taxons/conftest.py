import pytest

@pytest.fixture(scope="module")
def view_taxon(auth_headers):
    return