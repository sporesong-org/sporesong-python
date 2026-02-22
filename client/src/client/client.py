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
        self.secret : str = ""
        self.server_list : list[tuple[str, str]] = []
        self.fetched_servers = False
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

    async def CPSLR(self):
        body = mb.MessageBody()
        body = body.CPSLR()
        await self.send_message(body, "")

    async def CSRR(self, server_key : str):
        body = mb.MessageBody()
        body = body.CSRR("c1i3n7")
        await self.send_message(body, server_key)

    async def entry_point(self):
        await self.CPSLR()

        while not self.fetched_servers:
            await asyncio.sleep(0.1)

        print("Choose a server (type server name):")
        for server_tuple in self.server_list:
            print(server_tuple[1])

        user_in = input()
        for server_tuple in self.server_list:
            if server_tuple[1] == user_in:
                server_key = server_tuple[0]
                server_name = server_tuple[1]

        await self.CSRR(server_key)

        while True:
            user_input = await asyncio.to_thread(input, f"user@{server_name}: ")
            body = mb.MessageBody()
            body = body.CSN(user_input, "text")
            body.content["secret"] = self.secret
            await self.send_message(body, server_key)

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

            content : dict = message_data["body"]["content"]

            match message_data["body"]["type"]:
                case "SCSA":
                    self.secret = content["secret"]
                case "PCSLA":
                    self.server_list = content["server_list"]
                    self.fetched_servers = True
                case "SCRA":
                    pass
                case "SCPI":
                    notes : list[tuple[int, str, dict]] = content["notes"]
                    for note in notes:
                        print(f"Message #{note[0]}: {note[1]}")
                case _:
                    pass # Don't know how to handle that one...

    # Function for handling outbound transmissions
    async def tx(self, socket: ServerConnection, message):
        await socket.send(message, text=True)