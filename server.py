from flask import Flask, request, render_template, redirect, url_for, make_response
from Controller import RecommendationController
from database_updater import DatabaseUpdater

app = Flask(__name__, static_folder="static")

db_updater = DatabaseUpdater()


class Router:
    recommendation_controller = RecommendationController()

    MKB_ERROR_MESSAGE = 'Возможно, один или несколько кодов '\
                        'МКБ-10 введены неверно.<br>Пожалуйста, '\
                        'проверьте правильность написания кодов и '\
                        'попробуйте еще раз.'
    DB_UPDATING_ERROR_MESSAGE = 'В данный момент происходит обновление базы данных.'

    # Отображаем домашнюю страницу
    @staticmethod
    @app.route('/', methods=['GET'])
    def home_page():
        return render_template('index.html', error_message=False)

    # Создаем документ и отображаем его на странице
    @staticmethod
    @app.route('/search', methods=['POST'])
    def make_recommendation():
        if db_updater.is_db_updating():
            return render_template('index.html', error_message=Router.DB_UPDATING_ERROR_MESSAGE)

        search_req = request.form['search_req']
        mkbs = search_req.split("+")
        url = Router.recommendation_controller.generate_recommendation(mkbs)

        if url is False:
            return render_template('index.html', error_message=Router.MKB_ERROR_MESSAGE)

        return render_template('pdf.html', url=url)


if __name__ == '__main__':
    db_updater.first_db_filling()
    db_updater.scheduler_func()
    app.run(port=8880)
