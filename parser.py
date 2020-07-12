from selenium import webdriver
from data_structures import Recommendation
from data_structures import Theses
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
URL = 'http://cr.rosminzdrav.ru/#!/'



class IllegalArgumentException(Exception):
    pass

#browser - webdriver
#nosology_id - строка с идентификатором нозологии
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
    time.sleep(3)

    try:
        search_result = browser.find_elements_by_class_name('main-menu__search-result-item-text')
    except NoSuchElementException:
        print("Не удалось найти результат")
        return False

    newHref = str(search_result[0].get_attribute('href'))
    newHref = newHref.replace('recomend', 'schema')
    browser.get(newHref)
    WebDriverWait(browser, 10).until(ec.visibility_of_element_located((By.ID, "mkb")))
    print(newHref)

#browser - webdriver на котором открыта страница с документом, с которого можно считать MKB
#return - список кодов МКБ
def get_MKBs(browser):

    try:
        mkbs = browser.find_element_by_id('mkb')
    except NoSuchElementException:
        print("Коды МКБ отсутствуют")
        return []

    return str(mkbs.text).split('/')

#browser - webdriver на котором открыта страница с документом, с которого можно считать MKB
#return - объект Recommendation
def get_recommdendation_info(browser):
    recommendation = Recommendation()
    recommendation.MKBs = get_MKBs(browser)
    print(recommendation.MKBs)


browser = webdriver.Chrome('chromedriver.exe')
go_to_recommendation_page(browser, 'e10')
get_recommdendation_info(browser)


