import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Generate a random salt for key derivation
salt = secrets.token_bytes(16)

# Derive AES key from a passphrase using PBKDF2
passphrase = b"your_secure_passphrase"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  # 256-bit key for AES-256
    salt=salt,
    iterations=100000,  # Adjust as needed for desired computational cost
    backend=default_backend()
)
aes_key = kdf.derive(passphrase)

# Data to be encrypted
x = 18
data = bytes(str(x), 'utf-8')

# Pad the data to match the AES block size using PKCS7 padding
padder = padding.PKCS7(algorithms.AES.block_size).padder()
padded_data = padder.update(data) + padder.finalize()

# Generate a random IV for CBC mode
iv = secrets.token_bytes(16)

# Encrypt the data using AES in CBC mode
cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded_data) + encryptor.finalize()

print("Salt:", salt.hex())
print("Initialization Vector (IV):", iv.hex())
print("Encrypted data:", ciphertext.hex())
