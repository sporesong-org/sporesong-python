from lib.networking.server import Server
import lib.messages.message as msg
import lib.messages.message_body as mb
import lib.cryptography.key as cryptography
from websockets.asyncio.server import ServerConnection
import asyncio

class Proxy:
    def __init__(self):
        self.host = Server(self.rx, self.tx)
        self.public_keys_to_ids : dict = {}
        self.private_key, self.public_key = cryptography.generate_keypair()

    async def send_to_client(self, client_id, message : str):
        await self.host.id_to_connection[client_id].put(message)

    async def send_message(self, body : mb.MessageBody, target_key : str):
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
        print(socket.id, message)

        message_header_data : dict = msg.unpack_header(message)

        if not (message_header_data["source"] in self.public_keys_to_ids.keys()):
            # We don't have them in the map yet...
            self.public_keys_to_ids[message_header_data["source"]] = socket.id

        dest : str = message_header_data["destination"]

        if dest == self.public_key or dest == "":
            # Message is meant for us
            if dest == "":
                message_data = msg.unpack_all(message, "")
            else:
                message_data = msg.unpack_all(message, self.private_key)

            body : mb.MessageBody = mb.MessageBody()

            match message_data["body"]["type"]:
                case "SPRR":
                    pass
                case "GSB":
                    body = body.GSA()
                    await self.send_message(body, message_header_data["source"])
                case "CPSLR":
                    pass
                case _:
                    pass # Don't know how to handle that one...
        else:
            # Message was meant for another
            # TODO: Transmit to target based on map
            pass

    # Function for handling outbound transmissions
    async def tx(self, socket: ServerConnection, message):
        await socket.send(message, text=True)