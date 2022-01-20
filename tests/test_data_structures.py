import unittest
from datetime import datetime

import database_updater
from data_structures import Recommendation, Thesis


class TestRecommendation(unittest.TestCase):

    def test_from_json(self):
        date = datetime.today()
        expected_res = Recommendation('n1', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                                      [Thesis('4', '5', '6')], 'tag1', date)
        res = Recommendation.from_json({
            '_id': 'n1' + str(['c1', 'c2']),
            'nozology_name': 'n1',
            'MKBs': ['c1', 'c2'],
            'diagnosticTheses': {'g1': [{'text': '1', 'LCR': '2', 'LRE': '3'}]},
            'treatmentTheses': [{'text': '4', 'LCR': '5', 'LRE': '6'}],
            'table_tag': 'tag1',
            'publication_date': date,
        })
        self.assertEquals(res, expected_res)

    def test_serialize(self):
        date = datetime.today()
        expected_res = {
            '_id': 'n1' + str(['c1', 'c2']),
            'nozology_name': 'n1',
            'MKBs': ['c1', 'c2'],
            'diagnosticTheses': {'g1': [{'text': '1', 'LCR': '2', 'LRE': '3'}]},
            'treatmentTheses': [{'text': '4', 'LCR': '5', 'LRE': '6'}],
            'table_tag': 'tag1',
            'publication_date': date,
        }

        res = Recommendation('n1', ['c1', 'c2'], {'g1': [Thesis('1', '2', '3')]},
                             [Thesis('4', '5', '6')], 'tag1', date).serialize()
        self.assertEquals(res, expected_res)


class TestThesis(unittest.TestCase):

    def test_from_json(self):
        expected_res = Thesis('1', '2', '3')
        res = Thesis.from_json({
            'text': '1',
            'LCR': '2',
            'LRE': '3',
        })
        self.assertEquals(res, expected_res)

    def test_serialize(self):
        expected_res = {
            'text': '1',
            'LCR': '2',
            'LRE': '3',
        }
        res = Thesis('1', '2', '3')
        self.assertTrue(res, expected_res)
