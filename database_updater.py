import requests
import json

from data_structures import Recommendation
from recommendation_seeker import RecommendationSeeker
from db import insert_recommendation_into_db


class DatabaseUpdater:
    recommendation_response = None

    RECOMMENDATION_LIST_URL = 'https://democenter.nitrosbase.com/clinrecalg5/API.ashx?op=GetJsonClinrecs&ssid=undefined'

    recommendation_seeker = RecommendationSeeker()

    def __init__(self):
        self.recommendation_response = requests.get(self.RECOMMENDATION_LIST_URL)

    def is_recommendation_service_available(self):
        if self.recommendation_response.status_code != 200 or not self.recommendation_response.text.__contains__(
                '{"id":'):
            return False
        return True

    def save_recommendation(self, recommendation: Recommendation):
        insert_recommendation_into_db(recommendation)

    def update_recommendations(self):
        if not self.is_recommendation_service_available():
            return False

        recommendations = json.loads(self.recommendation_response.text)
        for recommendation in recommendations:
            self.save_recommendation(self.recommendation_seeker.find_recommendation(recommendation['id']))
