from flask import Flask, request, render_template
from Controller import RecommendationController
from apscheduler.schedulers.background import BackgroundScheduler
from database_updater import DatabaseUpdater
import time
import datetime

app = Flask(__name__, static_folder="static")
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

db_updater = DatabaseUpdater()


def db_update():
    current_hour = time.strftime("%H", time.localtime(time.time()))
    is_service_available = db_updater.update_recommendations()

    if current_hour == "23":
        if is_service_available is False:
            scheduler.add_job(db_update_2, 'date', run_date=datetime.datetime.now()+datetime.timedelta(hours=1))
        else:
            db_updater.update_recommendations()


def db_update_2():
    is_service_available = db_updater.update_recommendations()

    if is_service_available is False:
        scheduler.add_job(db_update_2, 'date', run_date=datetime.datetime.now() + datetime.timedelta(hours=1))
    else:
        db_updater.update_recommendations()


scheduler.add_job(db_update, 'interval', hours=1)


class Router:

    recommendation_controller = RecommendationController()

    # Отображаем домашнюю страницу
    @staticmethod
    @app.route('/', methods=['GET'])
    def home_page():
        return render_template('index.html')

    # Создаем документ и отображаем его на странице
    @staticmethod
    @app.route('/search', methods=['POST'])
    def make_recommendation():
        search_req = request.form['search_req']
        mkbs = search_req.split("+")
        url = Router.recommendation_controller.generate_recommendation(mkbs)

        if url is False:
            return render_template('error.html')

        return render_template('pdf.html', url=url)


if __name__ == '__main__':
    app.run(port=8880)
