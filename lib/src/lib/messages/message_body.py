import json

class MessageBody:
    def __init__(self):
        self.content = {}
        self.tags = {}
        self.type = None

    """
    Client-Server Note
    """
    def CSN(self, note_text : str, format : str):
        self.type = "CSN"
        self.content = {
            "text" : note_text
        }
        self.tags = {
            "timestamp" : 0,
            "format" : format
        }

        return self

    """
    Creates a str of the json representation of the MessageType.
    Used to get the MessageType's contents for sending over the
    network.
    """
    def pack(self) -> str:
        message_json : dict = {
            "type" : self.type,
            "content" : self.content,
            "tags" : self.tags
        }
        
        return json.dumps(message_json)

def unpack(body_json : str) -> dict:
    body_data : dict = json.loads(body_json)

    return body_data