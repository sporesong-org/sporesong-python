"""
Author: Orion Hess
Created: 2026-02-21
Edited: 2026-02-21
Purpose: Manage encryption keys
"""
from cryptography.hazmat.primitives.hpke import Suite, KEM, KDF, AEAD
from cryptography.hazmat.primitives.asymmetric import x25519

suite = Suite(KEM.X25519, KDF.HKDF_SHA256, AEAD.AES_128_GCM)


def generate_keypair() -> tuple[bytes, bytes]:
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()

    return private_key.private_bytes_raw(), public_key.public_bytes_raw()


def encrypt(data: bytes, public_key: bytes) -> bytes:
    public_key_typed = x25519.X25519PublicKey.from_public_bytes(public_key)
    cypher_text = suite.encrypt(data, public_key_typed)
    return cypher_text


def decrypt(data: bytes, private_key: bytes) -> bytes:
    private_key_typed = x25519.X25519PrivateKey.from_private_bytes(private_key)
    plain_text = suite.decrypt(data, private_key_typed)
    return plain_text
