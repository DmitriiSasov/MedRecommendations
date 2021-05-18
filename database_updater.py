import requests
import json

from data_structures import Recommendation
from recommendation_seeker import RecommendationSeeker
from db import insert_recommendation_into_db
from apscheduler.schedulers.background import BackgroundScheduler
import datetime


class DatabaseUpdater:
    recommendation_response = None

    RECOMMENDATION_LIST_URL = 'https://democenter.nitrosbase.com/clinrecalg5/API.ashx?op=GetJsonClinrecs&ssid=undefined'

    recommendation_seeker = RecommendationSeeker()

    db_updating = False

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.start()

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
        self.db_updating = True
        if not self.is_recommendation_service_available():
            return False

        count = 0
        recommendations = json.loads(self.recommendation_response.text)
        for recommendation in recommendations:
            self.save_recommendation(self.recommendation_seeker.find_recommendation(recommendation['id']))
            if count == len(recommendations):
                self.db_updating = False

            count += 1

    def is_db_updating(self):
        return self.db_updating

    def first_db_filling(self):
        self.scheduler.add_job(self.db_update, 'date',
                               run_date=datetime.datetime.now() + datetime.timedelta(seconds=5))

    def scheduler_func(self):
        self.scheduler.add_job(self.db_update, 'cron', hour='23')

    def db_update(self):
        if self.is_recommendation_service_available() is False:
            self.scheduler.add_job(self.db_update_2, 'date',
                                   run_date=datetime.datetime.now() + datetime.timedelta(hours=1))
        else:
            self.updating_process()

    def db_update_2(self):
        if self.is_recommendation_service_available() is False:
            self.scheduler.add_job(self.db_update_2, 'date',
                                   run_date=datetime.datetime.now() + datetime.timedelta(hours=1))
        else:
            self.updating_process()

    def updating_process(self):
        print("Database updating...")
        self.db_updating = True
        self.update_recommendations()
        self.db_updating = False
        print("Database updated!")
