import lib.networking.client
from server.database import Database


def main() -> None:
    db = Database() 
    db.get_connection()
    db.drop_relations()
    db.initialize_relations()
    id = "I'm an ID String!"
    name = "I'm a name!"
    db.put_client(id, name)
    #print("Get single client")
    #print(db.get_client(id))
    #print()
    #print("Get all clients")
    #print(db.get_clients())

    tags = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
        "key4": "value4",
    }
    sn = db.put_message("Message content", id, tags)
    print(db.get_message(sn))
    print(db.get_messages_sequence(0, 3))