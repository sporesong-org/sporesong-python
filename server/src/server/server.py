
"""
Author: Cash Hilstad, Orion Hess
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
from database import Database
import secrets

class Server:
    def __init__(self):
        """
        Initializes the client with empty data and generates
        a keypair for encryption.
        """
        self.client = nClient(self.rx, self.tx)
        self.private_key, self.public_key = cryptography.generate_keypair()
        self.registered = False
        self.db = Database()
        self.db.get_connection()
        self.db.drop_relations()
        self.db.initialize_relations()

    async def boot(self):
        msg_body = mb.MessageBody()
        msg_body = msg_body.SPRR("test", "public")
        await self.send_message(msg_body, "")



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

            content: dict = message_data["body"]["content"]

            match message_data["body"]["type"]:
                case "PSRA":
                    print("Got to psra handling")
                    self.registered = content["registered"]
                    
                case "GSB":
                    # TODO: handle status of clients
                    # For now just send register them then send them the secret
                    message_body = mb.MessageBody()
                    message_body = message_body.GSA()
                    await self.send_message(message_body, src)
                    await self.generate_secret(src)
                    
                case "GSA":
                    pass

                case "CSRR":
                    # TODO: Handle verification of clients
                    # For now every client is allowed in
                    display_name = "Default Name"
                    if "display_name" in content.keys():
                        display_name = content["display_name"]

                    self.db.put_client(src, display_name)

                    
                case "CSN":
                    client = self.db.get_client(src)
                    if client is None:
                        return

                    if client[3] == content["secret"]:
                        sequence_number = self.db.put_message(content["text"], src, message_data["body"]["tags"])
                        print(f"seq num: {sequence_number}")
                        print(content["text"])
                        for client in self.db.get_clients():
                            msg_bd = mb.MessageBody()
                            msg_bd = msg_bd.SCPI([(sequence_number, content["text"], message_data["body"]["tags"])])
                            await self.send_message(msg_bd, client[0])
                    else:
                        await self.generate_secret(src)

                case "CSQR":
                    pass

                case _:
                    pass # Don't know how to handle that one...

    # Function for handling outbound transmissions
    async def tx(self, socket: ServerConnection, message):
        await socket.send(message, text=True)

    async def generate_secret(self, src):
        secret = secrets.token_urlsafe(30)
        self.db.update_client_secret(src, secret)
        msg_body = mb.MessageBody()
        msg_body = msg_body.SCSA(secret)
        await self.send_message(msg_body, src)

        return secret
