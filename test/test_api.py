from schematics.models import Model
from schematics.types import StringType

from .conftest import client


class KeyPairSchema(Model):
    public_key = StringType(required=True)
    private_key = StringType(required=True)

class EncryptSchema(Model):
    ciphertext = StringType(required=True)

class DecryptSchema(Model):
    message = StringType(required=True)


class TestCryptoMsgAPI:
    def test_create_keys(self):
        """Тест генерации новой криптосвязки"""
        
        response = client.post("/keys/create")
        assert response.status_code == 200
        
        data = response.json()
        KeyPairSchema(data).validate()
    
    def test_encrypt_message(self, generate_keys):
        """Тест шифрования сообщения"""
        
        message = "Hello, world!"
        payload = {"public_key": generate_keys["public_key"], "message": message}
    
        response = client.post("/message/encrypt", json=payload)
        assert response.status_code == 200
    
        data = response.json()
        EncryptSchema(data).validate()
    
    def test_decrypt_message(self, generate_keys):
        """Тест расшифровки сообщения"""
        
        message = "Hello, World!"
        payload_encrypt = {"public_key": generate_keys["public_key"], "message": message}
        
        encrypted_response = client.post("/message/encrypt", json=payload_encrypt)
        encrypted_text = encrypted_response.json()["ciphertext"]
    
        payload_decrypt = {"private_key": generate_keys["private_key"], "ciphertext": encrypted_text}
        response = client.post("/message/decrypt", json=payload_decrypt)
        
        assert response.status_code == 200
    
        data = response.json()
        DecryptSchema(data).validate()
        
        assert data["message"] == message
    
    def test_invalid_key(self):
        """Тест с некорректным ключом"""
        
        payload = {"public_key": "INVALID_KEY", "message": "Test"}
        response = client.post("/message/encrypt", json=payload)
        
        assert response.status_code == 400
