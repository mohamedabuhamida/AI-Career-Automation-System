import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Load key from environment
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY environment variable is required")

# Node.js side used base64 to store the 32-byte key
key_bytes = base64.b64decode(ENCRYPTION_KEY)

if len(key_bytes) != 32:
    raise ValueError("ENCRYPTION_KEY must be 32 bytes when decoded from base64")

IV_LENGTH = 16
AUTH_TAG_LENGTH = 16

def decrypt(encrypted_data_b64: str) -> str:
    """
    Matches the TypeScript decrypt function.
    Layout: [IV (16 bytes)] + [AuthTag (16 bytes)] + [Ciphertext (N bytes)]
    """
    # 1. Decode from base64
    data = base64.b64decode(encrypted_data_b64)
    
    # 2. Extract components
    iv = data[:IV_LENGTH]
    auth_tag = data[IV_LENGTH:IV_LENGTH + AUTH_TAG_LENGTH]
    ciphertext = data[IV_LENGTH + AUTH_TAG_LENGTH:]
    
    # 3. Setup Decipher
    # We use modes.GCM(iv, auth_tag) to match Node's decipher.setAuthTag(authTag)
    cipher = Cipher(
        algorithms.AES(key_bytes),
        modes.GCM(iv, auth_tag),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    
    # 4. Decrypt
    decrypted_bytes = decryptor.update(ciphertext) + decryptor.finalize()
    
    return decrypted_bytes.decode('utf-8')

def encrypt(text: str) -> str:
    """
    Matches the TypeScript encrypt function.
    Layout: [IV (16 bytes)] + [AuthTag (16 bytes)] + [Ciphertext (N bytes)]
    """
    iv = os.urandom(IV_LENGTH)
    
    cipher = Cipher(
        algorithms.AES(key_bytes),
        modes.GCM(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    
    ciphertext = encryptor.update(text.encode('utf-8')) + encryptor.finalize()
    auth_tag = encryptor.tag
    
    # Combine: iv + tag + ciphertext
    result = iv + auth_tag + ciphertext
    
    return base64.b64encode(result).decode('utf-8')