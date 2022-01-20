from pymongo import MongoClient
import re


class MongoConnection:
    """Класс для подключения к базе данных клинических рекомендаций medrec и к коллекции recommendations"""
    CONFIG_REGEX = ':\s+([^\n]+[^\s]+)'

    def __init__(self):
        with open("db_config.txt", "r") as file:
            values = []
            for line in file:
                if line.__contains__(':'):
                    result = re.search(self.CONFIG_REGEX, line)
                    values.append(result.group(1))
        self.MONGO_CONNECTION = values[0]
        self.client = MongoClient(self.MONGO_CONNECTION)
        self.db = self.client['medrec']

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрываем соединение с бд и все коллекции
        """
        self.client.close()

    def get_collection(self):
        """
        Получить коллекцию recommendations
        """
        return self.db.get_collection('recommendations')

    def __enter__(self):
        return self

    def close(self):
        self.client.close()
