from connection import MongoConnection


class ConnectionProvider:
    def create_connection(self) -> MongoConnection:
        return MongoConnection()
