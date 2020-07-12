from selenium import webdriver
from data_structures import Recommendation
from data_structures import Theses
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

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
    search_area.send_keys(nosology_id[len(nosology_id) - 1])
    browser.implicitly_wait(3)

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


browser = webdriver.Chrome('chromedriver.exe')
go_to_recommendation_page(browser, 'e10')


