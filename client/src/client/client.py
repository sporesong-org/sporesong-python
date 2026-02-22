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
    async def rx(self, socket: ServerConnection, message : str):
        print(socket.id, message)

        message_header_data : dict = msg.unpack_header(message)

        dst : str = message_header_data["destination"]
        src : str = message_header_data["source"]

        if not (src in self.public_keys_to_ids.keys()):
            # We don't have them in the map yet...
            self.public_keys_to_ids[src] = socket.id

        if dst == self.public_key or dst == "":
            # Message is meant for us
            if dst == "":
                message_data = msg.unpack_all(message, "")
            else:
                message_data = msg.unpack_all(message, self.private_key)

            body : mb.MessageBody = mb.MessageBody()

            match message_data["body"]["type"]:
                case "SPRR":
                    # This requires us building the server registry
                    server_display_name = message_data["body"]["content"]["display_name"]
                    visibility_level = message_data["body"]["content"]["visibility_level"]

                    # Current implementation always accepts requests
                    # TODO: make it possible to deny based on something
                    self.add_server_to_registry(server_display_name, src)
                    self.add_server_visibility(visibility_level, src)

                    body = body.PSRA(True)
                    await self.send_message(body, src)

                case "GSB":
                    body = body.GSA()
                    await self.send_message(body, src)

                case "CPSLR":
                    # Client is requesting a list of public servers
                    # We gotta get that list (+S, display name)

                    server_list : list[tuple[str, str]] = []

                    for key in self.server_visibility.keys():
                        if self.server_visibility[key] == "public":
                            server_list.append(
                                (key, self.server_registry[key])
                            )

                    body = body.PCSLA(server_list) # Pass in list
                    await self.send_message(body, src)
                case _:
                    pass # Don't know how to handle that one...
        else:
            # Message was meant for another
            try:
                await self.send_to_client(self.public_keys_to_ids[src], message)
            except Exception:
                print(f"Unable to forward message to ({src}). Does it have an associated socket id?")

    # Function for handling outbound transmissions
    async def tx(self, socket: ServerConnection, message):
        await socket.send(message, text=True)