from connection import MongoConnection
from connection_provider import ConnectionProvider
from tests.mongo_connection_for_tests import MongoConnectionForTest


class ConnectionProviderForTests(ConnectionProvider):
    def create_connection(self) -> MongoConnection:
        return MongoConnectionForTest()
