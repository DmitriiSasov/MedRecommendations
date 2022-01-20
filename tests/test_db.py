import unittest
from datetime import datetime, timedelta

import db
from data_structures import Recommendation, Thesis
from .connection_provider_for_tests import ConnectionProviderForTests
from .mongo_connection_for_tests import MongoConnectionForTest


class TestDb(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.db = db.DB(ConnectionProviderForTests())

    def setUp(self) -> None:
        super().setUp()
        with MongoConnectionForTest() as connection:
            connection.get_collection().delete_many({})

    def test_is_rec_not_exist__contains_note_in_db(self):
        test_date = datetime.today()
        recommendations = [Recommendation('n1', ['c1', 'c2'], {'g1': ['t1']}, ['t2'], 'tag1', test_date).__dict__,
                           Recommendation('n2', ['c1', 'c2'], {'g1': ['t1']}, ['t2'], 'tag1',
                                          datetime(2020, 12, 21, 5, 3, 2, 5)).__dict__]

        with MongoConnectionForTest() as connection:
            connection.get_collection().insert_many(recommendations)
        self.assertFalse(self.db.is_rec_not_exist('n1', test_date))

    def test_is_rec_not_exist__doesnt_contains_note_in_db(self):
        test_date = datetime.today()
        recommendations = [Recommendation('n1', ['c1', 'c2'], {'g1': ['t1']}, ['t2'], 'tag1',
                                          datetime(2020, 12, 21, 5, 3, 2, 5)).__dict__,
                           Recommendation('n2', ['c1', 'c2'], {'g1': ['t1']}, ['t2'], 'tag1',
                                          datetime(2020, 12, 21, 5, 3, 2, 5)).__dict__]

        with MongoConnectionForTest() as connection:
            res = connection.get_collection().insert_many(recommendations)
        self.assertTrue(self.db.is_rec_not_exist('n1', test_date))

    def test_is_rec_not_exist__empty_db(self):
        self.assertTrue(self.db.is_rec_not_exist('n1', datetime.today()))

    def test_insert_recommendation_into_db__to_empty_db(self):
        rec = Recommendation('n1', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]}, [Thesis('1', '2', '3')], 'tag1',
                             datetime(2020, 12, 21, 5, 3, 2, 5))
        self.db.insert_recommendation_into_db(rec)
        with MongoConnectionForTest() as connection:
            is_found_my_rec = connection.get_collection().count_documents({'nozology_name': 'n1'}) == 1
            count_docs = connection.get_collection().count_documents({})
        self.assertTrue(is_found_my_rec)
        self.assertEqual(count_docs, 1)

    def test_insert_recommendation_into_db__to_db_with_elements(self):
        rec = Recommendation('n1', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]}, [Thesis('1', '2', '3')], 'tag1',
                             datetime(2020, 12, 21, 5, 3, 2, 5))
        with MongoConnectionForTest() as connection:
            connection.get_collection().insert_one(Recommendation('n2', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                                                  [Thesis('1', '2', '3')], 'tag1',
                                                                  datetime(2020, 12, 21, 5, 3, 2, 5)).serialize())
        self.db.insert_recommendation_into_db(rec)
        with MongoConnectionForTest() as connection:
            is_found_my_rec = connection.get_collection().count_documents({'nozology_name': 'n1'}) == 1
            count_docs = connection.get_collection().count_documents({})
        self.assertTrue(is_found_my_rec)
        self.assertEqual(count_docs, 2)

    def test_get_recommendation_from_db__from_not_empty_db(self):
        with MongoConnectionForTest() as connection:
            connection.get_collection().insert_one(Recommendation('n2', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                                                  [Thesis('1', '2', '3')], 'tag1',
                                                                  datetime(2020, 12, 21, 5, 3, 2, 5)).serialize())
        res = self.db.get_recommendation_from_db('n2')
        self.assertEquals(Recommendation('n2', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]}, [Thesis('1', '2', '3')],
                                         'tag1', datetime(2020, 12, 21, 5, 3, 2)), res)

    def test_get_recommendation_from_db__from_not_empty_db_last_recomendation(self):
        test_date = datetime(2021, 12, 21, 5, 3, 2, 0)
        with MongoConnectionForTest() as connection:
            connection.get_collection().insert_many([Recommendation('n2', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                                                    [Thesis('1', '2', '3')], 'tag1',
                                                                    datetime(2020, 12, 21, 5, 3, 2, 5)).serialize(),
                                                     Recommendation('n2', ['c1', 'c2'],
                                                                    {'g1': [Thesis('1', '1', '1')]},
                                                                    [Thesis('1', '1', '1')], 'tag2',
                                                                    test_date).serialize()
                                                     ])
        res = self.db.get_recommendation_from_db('n2')
        self.assertEquals(Recommendation('n2', ['c1', 'c2'], {'g1': [Thesis('1', '1', '1')]}, [Thesis('1', '1', '1')],
                                         'tag2', test_date), res)

    def test_get_recommendation_from_db__from_empty_db(self):
        res = self.db.get_recommendation_from_db('n2')
        self.assertFalse(res)

    def test_get_recommendation_from_db__from_not_empty_db_without_res(self):
        with MongoConnectionForTest() as connection:
            connection.get_collection().insert_one(Recommendation('n2', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                                                  [Thesis('1', '2', '3')], 'tag1',
                                                                  datetime(2020, 12, 21, 5, 3, 2, 5)).serialize())
        res = self.db.get_recommendation_from_db('n1')
        self.assertFalse(res)

    def test_insert_recommendations_if_not_exist__to_not_empty_db_without_repeats(self):
        existed_recommendations = [Recommendation('n1', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                                  [Thesis('4', '5', '6')], 'tag1',
                                                  datetime.today()).serialize(),
                                   Recommendation('n2', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                                  [Thesis('4', '5', '6')], 'tag1',
                                                  datetime(2020, 12, 21, 5, 3, 2, 5)).serialize()]
        new_recommendations = [Recommendation('n3', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                              [Thesis('4', '5', '6')], 'tag1',
                                              datetime.today()),
                               Recommendation('n4', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                              [Thesis('4', '5', '6')], 'tag1',
                                              datetime(2020, 12, 21, 5, 3, 2, 5))]
        with MongoConnectionForTest() as connection:
            connection.get_collection().insert_many(existed_recommendations)
        self.db.insert_recommendations_if_not_exist(new_recommendations)
        with MongoConnectionForTest() as connection:
            is_found_my_rec_1 = connection.get_collection().count_documents({'nozology_name': 'n3'}) == 1
            is_found_my_rec_2 = connection.get_collection().count_documents({'nozology_name': 'n4'}) == 1
            is_all_docs_inserted = connection.get_collection().count_documents({}) == 4
        self.assertTrue(is_found_my_rec_1)
        self.assertTrue(is_found_my_rec_2)
        self.assertTrue(is_all_docs_inserted)

    def test_insert_recommendations_if_not_exist__to_not_empty_db_with_repeats(self):
        existed_recommendations = [Recommendation('n1', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                                  [Thesis('4', '5', '6')], 'tag1',
                                                  datetime.today()).serialize(),
                                   Recommendation('n2', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                                  [Thesis('4', '5', '6')], 'tag1',
                                                  datetime(2020, 12, 21, 5, 3, 2, 5)).serialize()]
        new_recommendations = [Recommendation('n3', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                              [Thesis('4', '5', '6')], 'tag1',
                                              datetime.today()),
                               Recommendation('n2', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                              [Thesis('4', '5', '6')], 'tag1',
                                              datetime(2020, 12, 21, 5, 3, 2, 5))]
        with MongoConnectionForTest() as connection:
            connection.get_collection().insert_many(existed_recommendations)
        self.db.insert_recommendations_if_not_exist(new_recommendations)
        with MongoConnectionForTest() as connection:
            is_found_my_rec_1 = connection.get_collection().count_documents({'nozology_name': 'n3'}) == 1
            is_found_my_rec_2 = connection.get_collection().count_documents({'nozology_name': 'n2'}) == 1
            is_all_docs_inserted = connection.get_collection().count_documents({}) == 3
        self.assertTrue(is_found_my_rec_1)
        self.assertTrue(is_found_my_rec_2)
        self.assertTrue(is_all_docs_inserted)

    def test_insert_recommendations_if_not_exist__to_empty_db(self):
        new_recommendations = [Recommendation('n1', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                              [Thesis('4', '5', '6')], 'tag1',
                                              datetime.today()),
                               Recommendation('n2', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                              [Thesis('4', '5', '6')], 'tag1',
                                              datetime(2020, 12, 21, 5, 3, 2, 5))]
        self.db.insert_recommendations_if_not_exist(new_recommendations)
        with MongoConnectionForTest() as connection:
            is_found_my_rec_1 = connection.get_collection().count_documents({'nozology_name': 'n1'}) == 1
            is_found_my_rec_2 = connection.get_collection().count_documents({'nozology_name': 'n2'}) == 1
            is_all_docs_inserted = connection.get_collection().count_documents({}) == 2
        self.assertTrue(is_found_my_rec_1)
        self.assertTrue(is_found_my_rec_2)
        self.assertTrue(is_all_docs_inserted)
