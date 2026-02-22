import lib.networking.client
from server.database import Database

db = Database() 
db.get_connection()
db.drop_relations()
db.initialize_relations()

