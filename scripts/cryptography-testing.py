from lib.cryptography import key

private_key, public_key = key.generate_keypair()

in_text = b"Hello world, I'm readable!"
print(in_text)

cypher_text = key.encrypt(in_text, public_key)
print(cypher_text)

out_text = key.decrypt(cypher_text, private_key)
print(out_text)