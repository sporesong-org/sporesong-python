"""
Author: Cash Hilstad
Created: 2026-02-22
Edited: 2026-02-22
Purpose: Basic proxy implementation for hosting networking
    and allowing server-client communication. 
"""

from lib.networking.server import Server
import lib.messages.message as msg
import lib.messages.message_body as mb
import lib.cryptography.key as cryptography
from websockets.asyncio.server import ServerConnection
import asyncio

class Proxy:
    def __init__(self):
        """
        Initializes the proxy with empty data and generates
        a keypair for encryption.
        """
        self.host = Server(self.rx, self.tx)
        self.public_keys_to_ids : dict = {}
        self.server_registry = {}
        self.server_visibility = {}
        self.private_key, self.public_key = cryptography.generate_keypair()

    def add_server_to_registry(self, display_name : str, server_key : str):
        """
        Adds a server to the proxy's server registry. Stored as a
        hash of the server key pointing to the display name.
        """
        self.server_registry[server_key] = display_name

    def add_server_visibility(self, visibility : str, server_key : str):
        """
        Adds a server's desired visibility level to the proxy's server
        list. It is up to the proxy and server to agree upon what different
        visibilites entail.
        """
        self.server_visibility[server_key] = visibility

    async def send_to_client(self, client_id, message : str):
        """
        Given a socket client id and a packed Message, send it out 
        through the connection's queue.
        """
        await self.host.id_to_connection[client_id].put(message)

    async def send_message(self, body : mb.MessageBody, target_key : str):
        """
        Constructs a proper Message with correct metadata targeting
        target key and containing body content. Calls send_to_client
        when done.
        """
        message : msg.Message = msg.Message()
        message = message.set_source(self.public_key).set_destination(target_key).set_body(body)

        message_packed = message.pack(target_key)

        try:
            client_id = self.public_keys_to_ids[target_key]
        except Exception:
            # TODO : Make this catch better
            print(f"{target_key} not in public key - socket id dictionary.")

        await self.send_to_client(client_id, message_packed)

    # Function for handling incoming transmissions
    async def rx(self, socket: ServerConnection, message : str):
        """
        For every recieved message, do this stuff. Broadly, the
        proxy maintains a list of socket connections and who they
        belong to, and responds to messages depending on their
        content.
        """
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