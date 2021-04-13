import os
from threading import Timer

from flask import Flask, request, render_template, make_response
from bs4 import BeautifulSoup
from selenium import webdriver
from db import get_recommendation_from_db
from create_pdf import make_pdf

app = Flask(__name__, static_folder="static")

URL = 'http://cr.rosminzdrav.ru/#!/rubricator/adults'


# Проверяем, что к серверу рубрикатора можно подключиться
def check_recommendation_service():
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    element = soup.find('div', {'class': 'rubricator__tab-content tab-content'})
    browser.close()
    return element


# Удаляем файл
# path - строка - путь к файлу, который надо удалить
def remove_file(path):  # path
    os.remove(path)


# Отображаем домашнюю страницу
@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.php')


# Создаем документ и отображаем его на странице
@app.route('/search', methods=['POST'])
def make_recommendation():
    search_req = request.form['search_req']

    recommendations = []
    mkbs = search_req.split("+")

    for mkb in mkbs:
        recommendations.append(get_recommendation_from_db(mkb))

    doc_name = make_pdf(recommendations)

    url = 'static/' + doc_name
    timer = Timer(600, remove_file, args=['static/' + doc_name])
    timer.start()
    return render_template('pdf.html', url=url)


if __name__ == '__main__':
    app.run(debug=True, port=8880)
