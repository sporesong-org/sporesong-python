import json

class MessageBody:
    def __init__(self):
        self.content = {}
        self.tags = {}
        self.type = None
    

    """
    Server-Proxy Registration Request (SPRR)

    The display name field informs the proxy of the
    server's friendly name. The visibility level field
    states the desired privacy that the server wants
    from the proxy.
    """
    def SPRR(self, display_name : str, visibility_level : str):
        self.type = "SPRR"
        self.content = {
            "display_name" : display_name,
            "visibility_level" : visibility_level
        }
        self.tags = {}

        return self
    
    """
    Proxy-Server Registration Acknowledgement (PSRA)
    
    The registered field informs the server that the
    proxy has the server in the registry.
    """
    def PSRA(self, registered : bool):
        self.type = "PSRA"
        self.content = {
            "registered" : registered
        }
        self.tags = {}

        return self
    
    """
    General Status Broadcast (GSB)

    The status field informs the recipient of the sender's
    status. This is used to maintain a constant connection
    between hosts.
    """
    def GSB(self, status : str):
        self.type = "GSB"
        self.content = {
            "status" : status
        }
        self.tags = {}

        return self
    
    """
    General Status Acknowledgement (GSA)

    Used as a general response for most GSB
    messages. In some cases, a SCSA message
    is sent instead.
    """
    def GSA(self, ):
        self.type = "GSA"
        self.content = {}
        self.tags = {}

        return self
    
    """
    Server-Client Status Acknowledgement (SCSA)

    Used by servers to acknowledge client's
    online status and establish a shared secret
    between them.
    """
    def SCSA(self, secret : str):
        self.type = "SCSA"
        self.content = {
            "secret" : secret
        }
        self.tags = {}

        return self
    
    """
    Client-Proxy Server List Request (CPSLR)

    Used by clients to request a public server
    list from the proxy.
    """
    def CPSLR(self, ):
        self.type = "CPSLR"
        self.content = {}
        self.tags = {}

        return self
    
    """
    Proxy-Client Server List Acknowledgement (PCSLA)

    The server list field contains a list of servers
    by (+S, display name) from the proxy for the client.
    """
    def PCSLA(self, server_list : list[tuple[str, str]]):
        self.type = "PCSLA"
        self.content = {
            "server_list" : server_list
        }
        self.tags = {}

        return self
    
    """
    Client-Server Registration Request (CSRR)

    Used by clients to request addition to a server's
    list of members. Up to the server for how to
    respond.
    """
    def CSRR(self, ):
        self.type = "CSRR"
        self.content = {}
        self.tags = {}

        return self
    
    """
    Server-Client Registration Acknowledgement (SCRA)

    The registered field informs the client of their
    current registration status. It does not imply
    anything more than the current status.
    """
    def SCRA(self, registered : bool):
        self.type = "SCRA"
        self.content = {
            "registered" : registered
        }
        self.tags = {}

        return self

    """
    Client-Server Note (CSN)

    A note is sent by a client to post a message on
    a server. The note text field is the main content
    of the note, and the format field specifies the format
    of the note's data.
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

    A CSQR is used by a client to request previous
    notes posted on the server that fall in a given
    range. The range type field describes what kind
    of data should be considered, and range begin
    and end specify where the range should span,
    inclusive.
    """
    def CSQR(self, range_begin : str, range_end : str, range_type : str):
        self.type = "CSQR"
        self.content = {
            "range_begin" : range_begin,
            "range_end" : range_end,
            "range_type" : range_type
        }
        self.tags = {}

        return self
    
    
    """
    Server-Client Post-It (SCPI)

    Used to send a list of notes to a client. The
    notes field is a list of notes with the format
    (id, text, tags).
    """
    def SCPI(self, notes : list[tuple[int, str, dict]]):
        self.type = "SCPI"
        self.content = {
            "notes" : notes
        }
        self.tags = {}

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