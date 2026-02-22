"""
Authors: Orion Hess, Cash Hilstad
Created: 2026-02-21
Edited: 2026-02-21
Purpose: Manage encryption keys
"""
from cryptography.hazmat.primitives.hpke import Suite, KEM, KDF, AEAD
from cryptography.hazmat.primitives.asymmetric import x25519
import base64

suite = Suite(KEM.X25519, KDF.HKDF_SHA256, AEAD.AES_128_GCM)


def generate_keypair() -> tuple[str, str]:
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes_raw()
    public_bytes = public_key.public_bytes_raw()

    str_keys = (
        base64.b64encode(private_bytes).decode("utf-8"),
        base64.b64encode(public_bytes).decode("utf-8"),
    )

    return str_keys


def encrypt(data: str, public_key: str) -> str:
    data_bytes = data.encode("utf-8")
    public_bytes = base64.b64decode(public_key)

    public_key_typed = x25519.X25519PublicKey.from_public_bytes(public_bytes)

    cypher_bytes = suite.encrypt(data_bytes, public_key_typed)
    cypher_text = base64.b64encode(cypher_bytes).decode("utf-8")

    return cypher_text

def decrypt(data: str, private_key: str) -> str:
    data_bytes = base64.b64decode(data)
    private_bytes = base64.b64decode(private_key)

    private_key_typed = x25519.X25519PrivateKey.from_private_bytes(private_bytes)

    plain_bytes = suite.decrypt(data_bytes, private_key_typed)
    plain_text = plain_bytes.decode("utf-8")
    
    return plain_text
