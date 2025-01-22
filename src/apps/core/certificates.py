# core/certificates.py
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

CERTS_DIR = "certs/"

def create_certificates():
    if not os.path.exists(CERTS_DIR):
        os.makedirs(CERTS_DIR)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    # Save private key
    with open(os.path.join(CERTS_DIR, 'private_key.pem'), 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    public_key = private_key.public_key()
    # Save public key
    with open(os.path.join(CERTS_DIR, 'public_key.pem'), 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))

def sign_data(data: bytes) -> bytes:
    with open(os.path.join(CERTS_DIR, 'private_key.pem'), 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature

def verify_signature(data: bytes, signature: bytes) -> bool:
    with open(os.path.join(CERTS_DIR, 'public_key.pem'), 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False