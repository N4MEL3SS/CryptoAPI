import pytest
from fastapi.testclient import TestClient

from server import crypto_msg_api


client = TestClient(crypto_msg_api)

@pytest.fixture
def generate_keys():
    """Фикстура для генерации связки ключей"""
    
    return client.post("/keys/create").json()
