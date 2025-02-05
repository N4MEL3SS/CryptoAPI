from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

crypto_msg_api = FastAPI()

# Модели данных
class KeyPair(BaseModel):
    public_key: str
    private_key: str

class EncryptRequest(BaseModel):
    public_key: str
    message: str

class DecryptRequest(BaseModel):
    private_key: str
    ciphertext: str


# Генерация новой криптосвязки
KEY_SIZE = 2048
@crypto_msg_api.post("/keys/create")
def create_keys() -> KeyPair:
    key = RSA.generate(KEY_SIZE)
    public_key = key.publickey().export_key().decode()
    private_key = key.export_key().decode()
    
    return KeyPair(public_key=public_key, private_key=private_key)


# Шифрование сообщения
@crypto_msg_api.post("/message/encrypt")
def encrypt_message(request: EncryptRequest) -> dict[str, str]:
    try:
        public_key = RSA.import_key(request.public_key)
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_data = cipher.encrypt(request.message.encode())
        encrypted_b64 = base64.b64encode(encrypted_data).decode()
        
        return {"ciphertext": encrypted_b64}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid public key or message: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption error: {str(e)}")


# Расшифровка сообщения
@crypto_msg_api.post("/message/decrypt")
def decrypt_message(request: DecryptRequest) -> dict[str, str]:
    try:
        private_key = RSA.import_key(request.private_key)
        cipher = PKCS1_OAEP.new(private_key)
        encrypted_data = base64.b64decode(request.ciphertext)
        decrypted_message = cipher.decrypt(encrypted_data).decode()
        
        return {"message": decrypted_message}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid private key or message: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption error: {str(e)}")
