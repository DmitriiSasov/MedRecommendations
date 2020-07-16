from flask import Flask, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
from backend import _parser
from backend.createPDF import create_pdf

app = Flask(__name__)

URL = 'http://cr.rosminzdrav.ru/#!/rubricator/adults'


def check_recommendation_service():
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    element = soup.find('div', {'class': 'rubricator__not-found-message'})
    browser.close()
    return element


@app.route('/', methods=['GET'])
def home_page():
    if check_recommendation_service() is None:
        return jsonify({'is_service_ready': True}), 200
    else:
        return jsonify({'is_service_ready': False}), 400


@app.route('/search/<string:search_req>', methods=['GET'])
def make_recommendation(search_req):

    if check_recommendation_service() is not None:
        return jsonify({'is_service_ready': False}), 400

    recommendations = []
    mkbs = search_req.split("+")
    browser = webdriver.Chrome('chromedriver.exe')
    browser.implicitly_wait(60)

    for mkb in mkbs:
        if not _parser.go_to_recommendation_page(browser, mkb):
            return jsonify({'Код мкб - ' + mkb + ' введен неверно или не существует': True}), 401
        recommendations.append(_parser.get_recommdendation_info(browser))

    doc_name = create_pdf(recommendations)

    return jsonify({'url': doc_name}), 200


if __name__ == '__main__':
    app.run(debug=True)