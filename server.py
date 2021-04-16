import os
from threading import Timer

from flask import Flask, request, render_template, make_response
from bs4 import BeautifulSoup
from selenium import webdriver
import recommendation_seeker
from Controller import RecommendationController
from create_pdf import make_pdf

app = Flask(__name__, static_folder="static")


class Router:

    recommendation_controller = RecommendationController()

    # Отображаем домашнюю страницу
    @app.route('/', methods=['GET'])
    def home_page(self):
        return render_template('index.php')

    # Создаем документ и отображаем его на странице
    @app.route('/search', methods=['POST'])
    def make_recommendation(self):
        search_req = request.form['search_req']
        mkbs = search_req.split("+")
        url = self.recommendation_controller.generate_recommendation(mkbs)

        return render_template('pdf.html', url=url)


if __name__ == '__main__':
    app.run(port=8880)
