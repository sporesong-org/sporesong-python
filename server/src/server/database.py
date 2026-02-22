import psycopg2

from config import Config
from typing import Tuple, List

class Database:
    def __init__(self):
        self.__connection: psycopg2.Connection = None

    def __del__(self):
        if self.__connection is not None:
            self.__connection.close()

    def connection_is_alive(self) -> bool:
        """
        Return status of connection, printing and error if it is None
        """
        if self.__connection is None:
            print("ERROR: Connection not initialized")
            return False
        else:
            return True

    def get_connection(self) -> None:
        """
        Get a connection to the database
        """
        print("STATUS: Getting database connection...")
        conn = None
        try:
            conn = psycopg2.connect(
                dbname = Config.DB_NAME,
                user = Config.DB_USER,
                password = Config.DB_PASSWORD,
                host = Config.DB_HOST,
            )
            print("STATUS: Got database connection")
        except psycopg2.DatabaseError:
            print("ERROR: Failed to connect to database")
        
        self.__connection = conn
    
    def initialize_relations(self) -> None:
        """
        Initialize relations in the database - Requires empty database
        """
        print("STATUS: Initializing database relations...")
        if not self.connection_is_alive():
            return
        
        try:
            cursor = self.__connection.cursor()
            cursor.execute("""
            CREATE TABLE client(
            id          VARCHAR    PRIMARY KEY,
            name        VARCHAR    NOT NULL,
            join_date   TIMESTAMP   NOT NULL,
            secret      VARCHAR
            );

            CREATE TABLE message (
            sequence_number BIGSERIAL   PRIMARY KEY,
            time            TIMESTAMP   NOT NULL,
            content         VARCHAR     NOT NULL,
            author          VARCHAR     NOT NULL,
            FOREIGN KEY (author) REFERENCES client (id)
            );

            CREATE TABLE tag (
            message BIGSERIAL,
            key     VARCHAR,
            value   VARCHAR,
            PRIMARY KEY (message, key, value)
            ); 
            """)
            print("STATUS: Relations initialized")
            cursor.close()
            self.__connection.commit()
        # TODO: Proper exception handling
        except Exception as e:
            print(f"ERROR: {e}")
    
    def drop_relations(self) -> None:
        """
        Clear relations in the database
        """
        print("STATUS: Dropping relations...")
        if self.__connection is None:
            print("ERROR: Connection not initialized")
            return

        try:
            cursor = self.__connection.cursor()
            cursor.execute("""
            DROP TABLE IF EXISTS tag;
            DROP TABLE IF EXISTS message;
            DROP TABLE IF EXISTS client;
            """)
            print("STATUS: Relations dropped")
            cursor.close()
            self.__connection.commit()
        # TODO: Proper exception handling
        except Exception as e:
            print(f"ERROR: {e}")
    
    def put_client(self, id: str, name: str, secret: str = None):
        """
        Put a new client in the database
        """
        print(f"STATUS: Storing user '{name}':('{id}')")
        if self.__connection is None:
            print("ERROR: Connection not initialized")
            return None

        try:
            cursor = self.__connection.cursor()
            cursor.execute(
                "INSERT INTO client VALUES (%s, %s, CURRENT_TIMESTAMP, %s);",
                (id, name, secret, )
            )
            cursor.close()
            self.__connection.commit()
        # TODO: Proper exception handling
        except Exception as e:
            print(f"ERROR: {e}")
        
    def get_client(self, id: str) -> Tuple[str, str, str, str] | None:
        print(f"STATUS: Getting user with id: '{id}'")
        if not self.connection_is_alive:
            return
        
        try:
            cursor = self.__connection.cursor()
            cursor.execute("""
            SELECT id, name, join_date, secret
            FROM client
            WHERE id = %s;
            """, (id, ))
            client = cursor.fetchone()
            cursor.close()
            self.__connection.commit()
            return client
        # TODO: Proper exception handling
        except Exception as e:
            print(f"ERROR: {e}")

        return None
    
    def get_clients(self) -> List[Tuple[str, str, str, str]] | None:
        print("STATUS: Getting users")
        if not self.connection_is_alive:
            return

        try:
            cursor = self.__connection.cursor()
            cursor.execute("SELECT * FROM client")
            clients = cursor.fetchall()
            print(f"STATUS: Fetched {len(clients)} clients")
            cursor.close()
            self.__connection.commit()
            return clients
        # TODO: Proper exception handling
        except Exception as e:
            print(f"ERROR: {e}")

    def update_client_secret(self, id: str, secret: str) -> None:
        print("STATUS: Updating client secret")
        if not self.connection_is_alive:
            return

        try:
            cursor = self.__connection.cursor()
            cursor.execute("UPDATE client SET secret = %s WHERE id = %s", (secret, id, ))
            cursor.close()
            self.__connection.commit()
        # TODO: Proper exception handling
        except Exception as e:
            print(f"ERROR: {e}")


    def update_client_name(self, id: str, name: str) -> None:
        print("STATUS: Updating client secret")
        if not self.connection_is_alive:
            return

        try:
            cursor = self.__connection.cursor()
            cursor.execute("UPDATE client SET name = %s WHERE id = %s", (name, id, ))
            cursor.close()
            self.__connection.commit()
        # TODO: Proper exception handling
        except Exception as e:
            print(f"ERROR: {e}")


    def put_message(self, content: str, author: str, tags: dict[str, str]) -> int | None:
        print("STATUS: Putting message")
        if not self.connection_is_alive:
            return None
        try:
            cursor = self.__connection.cursor()
            cursor.execute(
                "INSERT INTO message (time, content, author) VALUES (LOCALTIMESTAMP, %s, %s) RETURNING sequence_number;",
                (content, author, )
            )
            sequence_number = cursor.fetchone()[0]

            tag_rows = [
                (sequence_number, key, value) for key, value in tags.items()
            ]
            cursor.executemany(
                "INSERT INTO tag VALUES (%s, %s, %s);", 
                tag_rows
            )

            cursor.close()
            self.__connection.commit()
            return sequence_number

        # TODO Proper error handling
        except Exception as e:
            print(f"ERROR: {e}")
        return None

    def get_message(self, sequence_number: int) -> Tuple[int, int, str, str, dict[str,str]]| None:
        print(f"STATUS: Getting message with sequence_number: {sequence_number}")
        if not self.connection_is_alive:
            return None
        try:
            cursor = self.__connection.cursor()
            cursor.execute("SELECT * FROM message WHERE sequence_number = %s;", (sequence_number, ))
            message = cursor.fetchone()
            if message is None: return None
            print(message)
            cursor.execute("SELECT key, value FROM tag WHERE message = %s", (message[0], ))
            tags = cursor.fetchall()
            cursor.close()
            return (*message, dict(tags))
        # TODO Proper error handling
        except Exception as e:
            print(f"ERROR: {e}")
        return None

    def get_messages_sequence(self, sequence_number_min: int, sequence_number_max: int) -> List[Tuple[int, int, str, str, dict[str, str]]] | None:
        print(f"STATUS: Getting messages: [{sequence_number_min},{sequence_number_max}]")
        if not self.connection_is_alive:
            return
        try:
            out_messages = []

            cursor = self.__connection.cursor()
            cursor.execute(
                "SELECT * FROM message WHERE sequence_number >= %s AND sequence_number <= %s;", 
                (sequence_number_min, sequence_number_max, )
            )
            messages = cursor.fetchall()
            if messages is None: return None
            for message in messages:
                print(f"The message, {message}")
                cursor.execute("SELECT key, value FROM tag WHERE message = %s", (message[0], ))
                tags = cursor.fetchall()
                out_messages.append((*message, dict(tags)))
            
            cursor.close()
            self.__connection.commit()
            return out_messages

        # TODO Proper error handling
        except Exception as e:
            print(f"ERROR: {e}")
        return None

    def get_messages_time(self, time_min: int, time_max: int) -> List[Tuple[int, int, str, str, List[str, str]]] | None:
        print(f"STATUS: Getting messages: [{time_min},{time_max}]")
        if not self.connection_is_alive:
            return
        try:
            out_messages = []

            cursor = self.__connection.cursor()
            cursor.execute("SELECT * FROM message WHERE time >= %(time_min)s AND time <= %(time_max)s;", time_min, time_max)
            messages = cursor.fetchone()
            for message in messages:
                cursor.execute("SELECT key, value FROM tag WHERE messsage = %s", message[0])
                tags = cursor.fetch_all()
                out_messages.append(tuple(set(message + tags)))
            
            cursor.close()
            self.__connection.commit()
            return out_messages

        # TODO Proper error handling
        except Exception as e:
            print(f"ERROR: {e}")
        return None