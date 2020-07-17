import os

from flask import Flask, jsonify, request, render_template, make_response
from bs4 import BeautifulSoup
from selenium import webdriver
from backend import _parser
from backend.createPDF import create_pdf
from backend.sort_document import sort

app = Flask(__name__, static_folder="static")

URL = 'http://cr.rosminzdrav.ru/#!/rubricator/adults'


def check_recommendation_service():
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    element = soup.find('div', {'class': 'rubricator__tab-content tab-content'})
    browser.close()
    return element


@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.php')


@app.route('/search', methods=['POST'])
def make_recommendation():
    search_req = request.form['search_req']

    if check_recommendation_service() is None:
        return jsonify({'service_status': 'Сервис временно недоступен'}), 400

    recommendations = []
    mkbs = search_req.split("+")
    browser = webdriver.Chrome('chromedriver.exe')
    browser.implicitly_wait(60)

    for mkb in mkbs:
        if not _parser.go_to_recommendation_page(browser, mkb):
            browser.close()
            return jsonify({'Код мкб - ' + mkb + ' введен неверно или не существует'}), 401
        recommendations.append(_parser.get_recommdendation_info(browser))

    browser.close()

    doc_name = create_pdf(recommendations[0])

    url = 'http://localhost:5000/static/' + doc_name

    return render_template('pdf.html', url=url)


if __name__ == '__main__':
    app.run(debug=True)
