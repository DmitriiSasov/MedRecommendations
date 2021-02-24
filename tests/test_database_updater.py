import unittest

import database_updater

class TestParser(unittest.TestCase):

    updater = None

    def setUp(self):
        self.updater = database_updater.DatabaseUpdater()

    def test_is_recommendation_server_available_server_is_available(self):
        self.assertTrue(self.updater.is_recommendation_service_available())

    def test_update_recommendations(self):
        self.updater.update_recommendations()

