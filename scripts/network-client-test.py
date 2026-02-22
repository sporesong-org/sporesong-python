import asyncio
from lib.networking import client
from websockets.asyncio.client import ClientConnection

import lib.messages.message as msg
import lib.messages.message_body as mb
from lib.cryptography import key

def print_stuff(message):
    print(message)

async def tx(socket: ClientConnection, message):
    await socket.send(message)

c = client.Client(print_stuff, tx)

async def main():
    private_key, public_key = key.generate_keypair()
    message = msg.Message()
    body = mb.MessageBody()
    body = body.GSB("online")
    packed = message.set_source(public_key).set_destination("").set_body(body).pack("")
    await c.watch_tx.put(packed)
    await c.connect("ws://localhost:4321")



if __name__ == "__main__":
    asyncio.run(main())
