import json

class MessageBody:
    def __init__(self):
        self.content = {}
        self.tags = {}
        self.type = None
    

    """
    Server-Proxy Registration Request (SPRR)
    """
    def SPRR(self, ):
        self.type = "SPRR"
        self.content = {

        }
        self.tags = {

        }

        return self
    
    """
    Proxy-Server Registration Acknowledgement (PSRA)
    """
    def PSRA(self, ):
        self.type = "PSRA"
        self.content = {

        }
        self.tags = {

        }

        return self
    
    """
    General Status Broadcast (GSB)
    """
    def GSB(self, ):
        self.type = "GSB"
        self.content = {

        }
        self.tags = {

        }

        return self
    
    """
    General Status Acknowledgement (GSA)
    """
    def GSA(self, ):
        self.type = "GSA"
        self.content = {

        }
        self.tags = {

        }

        return self
    
    """
    Client-Proxy Server List Request (CPSLR)
    """
    def CPSLR(self, ):
        self.type = "CPSLR"
        self.content = {

        }
        self.tags = {

        }

        return self
    
    """
    Proxy-Client Server List Acknowledgement (PCSLA)
    """
    def PCSLA(self, ):
        self.type = "PCSLA"
        self.content = {

        }
        self.tags = {

        }

        return self
    
    """
    Client-Server Registration Request (CSRR)
    """
    def CSRR(self, ):
        self.type = "CSRR"
        self.content = {

        }
        self.tags = {

        }

        return self
    
    """
    Server-Client Registration Acknowledgement (SCRA)
    """
    def SCRA(self, ):
        self.type = "SCRA"
        self.content = {

        }
        self.tags = {

        }

        return self

    """
    Client-Server Note (CSN)
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
    Client-Server Query Request (CSQR)
    """
    def CSQR(self, ):
        self.type = "CSQR"
        self.content = {

        }
        self.tags = {

        }

        return self
    
    
    """
    Server-Client Post-It (SCPI)
    """
    def SCPI(self, ):
        self.type = "SCPI"
        self.content = {

        }
        self.tags = {

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