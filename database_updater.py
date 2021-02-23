import requests
import json


class DatabaseUpdater:

    recommendation_response = None

    RECOMMENDATION_URL = 'https://democenter.nitrosbase.com/clinrecalg5/API.ashx?op=GetJsonClinrecs&ssid=undefined'

    def setup(self):
        self.recommendation_response = requests.get(self.RECOMMENDATION_URL)

    # Проверяем, что к серверу с рекомендациями можно подключиться
    def is_recommendation_service_available(self):
        if self.recommendation_response is None or self.recommendation_response.status_code != 200 or \
                not self.recommendation_response.text.__contains__('{"id":'):
            return False
        return True




