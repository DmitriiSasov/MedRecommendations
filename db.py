# -*- coding: utf-8 -*-
from datetime import datetime

import pymongo

from connection_provider import ConnectionProvider
from data_structures import Recommendation


class DB:

    def __init__(self, connection_provider: ConnectionProvider) -> None:
        self.connection_provider = connection_provider

    def is_rec_not_exist(self, nozology_name, date):
        with self.connection_provider.create_connection() as connection:
            rec = connection.get_collection().count_documents({'nozology_name': nozology_name,
                                                               'publication_date': date})
        return rec == 0

    def insert_recommendation_into_db(self, recommendation):
        with self.connection_provider.create_connection() as connection:
            if self.is_rec_not_exist(recommendation.nozology_name, recommendation.publication_date):
                connection.get_collection().insert_one(recommendation.serialize())

    def get_recommendation_from_db(self, nozology_name):
        recommendation = None
        with self.connection_provider.create_connection() as connection:
            res = connection.get_collection().find({'nozology_name': nozology_name})\
                .sort('publication_date', pymongo.DESCENDING).limit(1)
            res = list(res)
            if len(res) > 0:
                recommendation = Recommendation.from_json(res[0])
        if recommendation is None:
            return False
        return recommendation

    def insert_recommendations_if_not_exist(self, recommendations):
        """
        Добавляем в базу данных только те рекомендации, которых в базе нету
        :param recommendations: list, рекомендации, которые нужно добавить
        """
        recommendations_for_adding = []
        for recommendation in recommendations:
            if self.is_rec_not_exist(recommendation.nozology_name, recommendation.publication_date):
                recommendations_for_adding.append(recommendation.serialize())
        with self.connection_provider.create_connection() as connection:
            connection.get_collection().insert_many(recommendations_for_adding)
