import pytest

from tienda import create_app


@pytest.fixture
def client():
    return create_app({"TESTING": True}).test_client()
