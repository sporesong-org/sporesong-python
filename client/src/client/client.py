"""
Author: Cash Hilstad
Created: 2026-02-22
Edited: 2026-02-22
Purpose: Basic proxy implementation for hosting networking
    and allowing server-client communication. 
"""

from lib.networking.client import Client as nClient
import lib.messages.message as msg
import lib.messages.message_body as mb
import lib.cryptography.key as cryptography
from websockets.asyncio.server import ServerConnection
import asyncio

class Client:
    def __init__(self):
        """
        Initializes the client with empty data and generates
        a keypair for encryption.
        """
        self.client = nClient(self.rx, self.tx)
        self.private_key, self.public_key = cryptography.generate_keypair()

    async def send_to_proxy(self, packed_message : str):
        """
        Given a packed Message, send it out through the connection's queue.
        """
        await self.client.watch_tx.put(packed_message)

    async def send_message(self, body : mb.MessageBody, target_key : str):
        """
        Constructs a proper Message with correct metadata targeting
        target key and containing body content. Calls send_to_proxy
        when done.
        """
        message : msg.Message = msg.Message()
        message = message.set_source(self.public_key).set_destination(target_key).set_body(body)

        message_packed = message.pack(target_key)

        await self.send_to_proxy(message_packed)

    async def entry_point(self):
        while True:
            user_input = await asyncio.to_thread(input, "> ")
            body = mb.MessageBody()
            body = body.GSB("online")
            await self.send_message(body, "")

    # Function for handling incoming transmissions
    async def rx(self, message : str):
        message_header_data : dict = msg.unpack_header(message)

        dst : str = message_header_data["destination"]
        src : str = message_header_data["source"]

        if dst == self.public_key:
            # Message is meant for us
            message_data = msg.unpack_all(message, self.private_key)

            print(message_data)

            body : mb.MessageBody = mb.MessageBody()

            match message_data["body"]["type"]:
                case _:
                    pass # Don't know how to handle that one...

    # Function for handling outbound transmissions
    async def tx(self, socket: ServerConnection, message):
        await socket.send(message, text=True)