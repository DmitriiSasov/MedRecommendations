from bs4 import BeautifulSoup
from selenium import webdriver
from data_structures import Recommendation
from data_structures import Theses
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time

URL = 'http://cr.rosminzdrav.ru/#!/'


class IllegalArgumentException(Exception):
    pass


# browser - webdriver
# nosology_id - строка с идентификатором нозологии
def go_to_recommendation_page(browser, nosology_id):
    if nosology_id == "":
        raise IllegalArgumentException("Идентификатор нозологии указан неверно")

    browser.get(URL)
    try:
        search_area = browser.find_element_by_class_name("main-menu__search")
    except NoSuchElementException:
        print("Поиск по временно недоступен")
        browser.close()
        return False

    search_area.send_keys(nosology_id[:len(nosology_id) - 1])
    time.sleep(1)
    search_area.send_keys(nosology_id[len(nosology_id) - 1])
    time.sleep(1)

    try:
        search_result = browser.find_elements_by_class_name('main-menu__search-result-item-text')
    except NoSuchElementException:
        print("Не удалось найти результат")
        return False

    newHref = str(search_result[0].get_attribute('href'))
    newHref = newHref.replace('recomend', 'schema')
    browser.get(newHref)
    print(newHref)


def get_recommendation_page_url(browser, nosology_id):
    if nosology_id == "":
        raise IllegalArgumentException("Идентификатор нозологии указан неверно")

    browser.get(URL)
    try:
        search_area = browser.find_element_by_class_name("main-menu__search")
    except NoSuchElementException:
        print("Поиск по временно недоступен")
        browser.close()
        return False

    search_area.send_keys(nosology_id[:len(nosology_id) - 1])
    time.sleep(1)
    search_area.send_keys(nosology_id[len(nosology_id) - 1])
    time.sleep(1)

    try:
        search_result = browser.find_elements_by_class_name('main-menu__search-result-item-text')
    except NoSuchElementException:
        print("Не удалось найти результат")
        return False

    newHref = str(search_result[0].get_attribute('href'))
    newHref = newHref.replace('recomend', 'schema')
    browser.get(newHref)
    print(newHref)
    return newHref


# browser - webdriver на котором открыта страница с документом, с которого можно считать MKB
# return - список кодов МКБ
def get_MKBs(browser):
    try:
        WebDriverWait(browser, 10).until(ec.visibility_of_element_located((By.ID, "mkb")))
        mkbs = browser.find_element_by_id('mkb')
    except NoSuchElementException:
        print("Коды МКБ отсутствуют")
        return []
    except TimeoutException:
        print("Коды МКБ отсутствуют")
        return []

    return str(mkbs.text).split('/')


def get_LCR(text):
    if text.__contains__("УУР") or text.__contains__("Уровень убедительности рекомендаций") or \
            text.__contains__("рекомендаций") and text.__contains__("доказательств"):
        if text.__contains__("УУР"):
            substr = text[text.find("УУР") + 3: text.find(",")]
        else:
            substr = text[text.find("рекомендаций") + 12: text.find("(")]

        for char in substr:
            if char.isalpha() and char.isupper():
                return char
    else:
        return ""


def get_LRE(text):
    result = ""
    if text.__contains__("УДД") or text.__contains__("УУД") or text.__contains__("уровень достоверности доказательств") or \
            text.__contains__("рекомендаций") and text.__contains__("доказательств"):
        if text.__contains__("УДД"):
            substr = text[text.find("УДД") + 3: text.find(")")]
        elif text.__contains__("УУД"):
            substr = text[text.find("УУД") + 3: text.find(")")]
        else:
            substr = text[text.find("доказательств") + 13: text.find(")")]

        for char in substr:
            if char.isdigit() or char == 'V' or char == 'I':
                result += char
    return result


# browser - webdriver на котором открыта страница с документом, с рекомендациями
# return - словарь тезисов по темам
def get_diagnosys_theses(browser):
    theses_dict = {}

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    header_of_diagnosys_div = soup.find(id="doc_2")
    current_header = header_of_diagnosys_div.get_text()
    theses_dict[current_header] = []
    diagnosys_div = header_of_diagnosys_div.findParent()
    if diagnosys_div is None:
        return {}

    all_elements_in_diag_div = list(
        list(diagnosys_div.findAll(True, recursive=False))[1].findChild().findAll(True, recursive=False))

    index = 0
    new_theses = None
    while index < len(all_elements_in_diag_div):
        current_element = all_elements_in_diag_div[index]
        if current_element.name == "h2":
            current_header = current_element.get_text()
            if not theses_dict.keys().__contains__(current_header):
                theses_dict[current_header] = []
        elif current_element.name == "ul":
            attrs_count = len(current_element.attrs.keys())
            if attrs_count == 0:
                theses_text = current_element.text
                if new_theses is None:
                    new_theses = Theses()
                    new_theses.text = theses_text
                else:
                    new_theses.text += '\n' + theses_text
                if index + 1 < len(all_elements_in_diag_div) and all_elements_in_diag_div[index + 1].name == "p":
                    after_theses_tag = all_elements_in_diag_div[index + 1]
                    LCR = get_LCR(str(after_theses_tag.text))
                    LRE = get_LRE(str(after_theses_tag.text))
                    if LCR == "" or LRE == "":
                        new_theses.text += '\n' + str(after_theses_tag.text)
                    else:
                        new_theses.LCR = LCR
                        new_theses.LRE = LRE
                        theses_dict.get(current_header).append(new_theses)
                        new_theses = None
                else:
                    new_theses = None
        index += 1

    return theses_dict


# browser - webdriver на котором открыта страница с документом, с которого можно считать MKB
# return - объект Recommendation
def get_recommdendation_info(browser):
    recommendation = Recommendation()
    recommendation.MKBs = get_MKBs(browser)
    print(recommendation.MKBs)
    recommendation.diagnosticTheses = get_diagnosys_theses(browser)
    for key in recommendation.diagnosticTheses.keys():
        print(key)
        for element in recommendation.diagnosticTheses[key]:
            print(element.text)
            print(element.LCR)
            print(element.LRE)
        print("\n")


browser = webdriver.Chrome('chromedriver.exe')
browser.implicitly_wait(30)
go_to_recommendation_page(browser, 'e10')
get_recommdendation_info(browser)
