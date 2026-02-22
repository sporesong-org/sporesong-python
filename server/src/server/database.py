import psycopg2

from server.config import Config

class Database:
    def __init__(self):
        self.__connection = None

    #def __del__(self):
    #    if self.__connection is not None:
    #        self.__connection.close()

    def get_connection(self) -> None:
        print("STATUS: Getting database connection...")
        conn = None
        try:
            conn = psycopg2.connect(
                dbname = Config.DB_NAME,
                user = Config.DB_USER,
                password = Config.DB_PASSWORD,
                host = Config.DB_HOST,
            )
        except psycopg2.DatabaseError:
            print("ERROR: Failed to connect to database")
        
        self.__connection = conn
    
    def initialize_relations(self) -> None:
        print("STATUS: Initializing database relations...")
        if self.__connection is None:
            print("ERROR: Connection not initialized")
            return
        
        try:
            cursor = self.__connection.cursor()
            cursor.execute("""
            CREATE TABLE user (
            id          CHAR(32)    PRIMARY KEY,
            name        CHAR(30)    NOT NULL,
            join_date   DATE        NOT NULL,
            secret      CHAR(30)    NOT NULL,
            );

            CREATE TABLE message (
            sequence_number BIGSERIAL   PRIMARY KEY,
            time            TIMESTAMP   NOT NULL,
            content         VARCHAR     NOT NULL,
            author          CHAR(32)    NOT NULL,
            FOREIGN KEY (author) REFERENCES user (id),
            );

            CREATE TABLE tag (
            message BIGSERIAL,
            key     VARCHAR,
            value   VARCHAR,
            PRIMARY KEY (message, key, value),
            ); 
            """)
        except Exception as e:
            print(f"ERROR: {e}")
    
    def drop_relations(self) -> None:
        print("STATUS: Dropping relations")
        if self.__connection is None:
            print("ERROR: Connection not initialized")
        
        try:
            cursor = self.__connection.cursor()
            cursor.execute("""
            DROP TABLE tag IF EXISTS;
            DROP TABLE message IF EXISTS;
            DROP TABLE user IF EXISTS;
            """)
        except Exception as e:
            print(f"ERROR: {e}")