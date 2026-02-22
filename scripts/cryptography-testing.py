from lib.cryptography import key
import lib.messages.message as msg
import lib.messages.message_body as mb

private_key, public_key = key.generate_keypair()

in_text = "Hello world, I'm readable!"
print(in_text)

cypher_text = key.encrypt(in_text, public_key)
print(cypher_text)

out_text = key.decrypt(cypher_text, private_key)
print(out_text)

message = msg.Message()
body = mb.MessageBody()
body = body.CSN("Hello, World!", "utf-8")
packed = message.set_source("SRC").set_destination("DST").set_body(body).pack(public_key)
print(packed)
unpacked = msg.unpack(packed, private_key)
print(unpacked)

