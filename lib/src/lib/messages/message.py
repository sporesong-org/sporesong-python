import json
import lib.messages.message_body as mb
import lib.cryptography.key as cryptography
from datetime import datetime

class Message:
    def __init__(self):
        self.source : str = None
        self.destination : str = None
        self.message_body : mb.MessageBody = None

    def set_source(self, source : str):
        self.source = source
        return self

    def set_destination(self, destination : str):
        self.destination : str = destination
        return self

    def set_body(self, body : mb.MessageBody):
        self.message_body = body
        return self

    """
    Creates a str of the json representation of the Message.
    Used to get the Message's contents for sending over the
    network.
    """
    def pack(self, body_key : str) -> tuple[str, int]:
        encrypted_body : str = cryptography.encrypt(self.message_body.pack(), body_key)

        message_json : dict = {
            "source" : self.source,
            "destination" : self.destination,
            "body" : encrypted_body,
            "timestamp" : datetime.now().timestamp()
        }

        message_str : str = json.dumps(message_json)

        return message_str   
        
def unpack(message_json : str, body_key : str) -> dict:
    message_data : dict = json.loads(message_json)

    message_data["body"] = mb.unpack(
        cryptography.decrypt(
            message_data["body"], body_key
        )
    )

    return message_data

