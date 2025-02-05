const baseUrl = 'http://localhost:8000';

// Генерация ключевой пары
async function createKeys() {
  try {
    const response = await fetch(`${baseUrl}/keys/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const keys = await response.json();
    console.log('Generated Keys:', keys);
    return keys;
  } catch (error) {
    console.error('Error creating keys:', error);
  }
}

// Шифрование сообщения
async function encryptMessage(publicKey, message) {
  try {
    const response = await fetch(`${baseUrl}/message/encrypt`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ public_key: publicKey, message: message })
    });
    const result = await response.json();
    console.log('Encrypted Message:', result);
    return result.ciphertext;
  } catch (error) {
    console.error('Error encrypting message:', error);
  }
}

// Расшифровка сообщения
async function decryptMessage(privateKey, ciphertext) {
  try {
    const response = await fetch(`${baseUrl}/message/decrypt`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ private_key: privateKey, ciphertext: ciphertext })
    });
    const result = await response.json();
    console.log('Decrypted Message:', result);
    return result.message;
  } catch (error) {
    console.error('Error decrypting message:', error);
  }
}

// Демонстрация работы
(async function demo() {
  const keys = await createKeys();

  const message = "Hello, World!";
  const encrypted = await encryptMessage(keys.public_key, message);
  
  if (encrypted) {
    const decrypted = await decryptMessage(keys.private_key, encrypted);
    console.log('Original Message:', message);
    console.log('Decrypted Message:', decrypted);
  }
})();
