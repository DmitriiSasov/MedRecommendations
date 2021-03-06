from bs4 import BeautifulSoup
from data_structures import Recommendation
from data_structures import Thesis
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

URL = 'http://cr.rosminzdrav.ru/#!/'


# browser - webdriver
# nosology_id - строка с идентификатором нозологии
def go_to_recommendation_page(browser, nosology_id):
    res = get_recommendation_page_url(browser, nosology_id)
    if not res:
        return False
    else:
        browser.get(res)
        return True


def get_recommendation_page_url(browser, nosology_id):
    if nosology_id == "":
        print("Идентификатор нозологии указан неверно")
        return False

    browser.get(URL)
    try:
        search_area = browser.find_element_by_class_name("main-menu__search")
    except NoSuchElementException:
        print("Поиск временно недоступен")
        browser.close()
        return False
    except TimeoutException:
        print("Поиск временно недоступен")
        browser.close()
        return False

    if len(nosology_id) != 1:
        search_area.send_keys(nosology_id[:len(nosology_id) - 1])
        time.sleep(1)

    search_area.send_keys(nosology_id[len(nosology_id) - 1])
    time.sleep(1)

    try:
        browser.implicitly_wait(2)
        search_result = browser.find_elements_by_class_name('main-menu__search-result-item-text')
        browser.implicitly_wait(10)
        if len(search_result) == 0:
            print("Не удалось найти результат")
            browser.close()
            return False
    except NoSuchElementException:
        print("Не удалось найти результат")
        browser.close()
        return False
    except TimeoutException:
        print("Не удалось найти результат")
        browser.close()
        return False

    newHref = str(search_result[0].get_attribute('href'))
    newHref = newHref.replace('recomend', 'schema')
    print(newHref)
    search_area.clear()
    return newHref


# browser - webdriver на котором открыта страница с документом, с рекомендациям
# return - название нозологии
def get_nozology_name(browser):
    try:
        browser.find_element_by_id('mkb')
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        name = soup.find('div', {'class': 'main-text'}).find('h1', {'class': 'ng-binding'})
    except NoSuchElementException:
        print("Название болезни отсуствует")
        return ""
    except TimeoutException:
        print("Название болезни отсуствует")
        return ""

    return name.text


# browser - webdriver на котором открыта страница с документом, с которого можно считать MKB
# return - список кодов МКБ
def get_MKBs(browser):
    try:
        browser.find_element_by_id('mkb')
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        mkbs = soup.find(id='mkb')
    except NoSuchElementException:
        print("Коды МКБ отсутствуют")
        return []
    except TimeoutException:
        print("Коды МКБ отсутствуют")
        return []

    return mkbs.text.split('/')


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
    if text.__contains__("УДД") or text.__contains__("УУД") or text.__contains__(
            "уровень достоверности доказательств") or \
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
            if attrs_count == 0 or not current_element.attrs.keys().__contains__("type"):
                theses_text = current_element.text
                if new_theses is None:
                    new_theses = Thesis()
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


# browser - webdriver на котором открыта страница с документом, с рекомендациями
# return - список тегов, в блоке, посвященном медикаментозному лечению
def get_treatment_tags(browser):
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    header_of_treatment_div = soup.find(id="doc_3")
    treatment_div = header_of_treatment_div.findParent()
    if treatment_div is None:
        return {}

    all_tags = list(
        list(treatment_div.findAll(True, recursive=False))[1].findChild().findAll(True, recursive=False))

    first_tag_index = -1
    last_tag_index = -1
    index = 0
    tags = []
    for tag in all_tags:
        if first_tag_index != -1 and tag.name == "h2":
            last_tag_index = index
        if tag.name == "h2" and tag.text.__contains__("Медикаментозная терапия"):
            first_tag_index = index
        if first_tag_index != -1 and last_tag_index == -1:
            tags.append(tag)
        index += 1
    return tags


# browser - webdriver на котором открыта страница с документом, с рекомендациями
# return - словарь с рекомендациями по лечению заболевания
def get_treatment_theses(browser):
    theses_list = []

    all_tags = get_treatment_tags(browser)

    index = 0
    new_theses = None
    while index < len(all_tags):
        current_element = all_tags[index]
        if current_element.name == "ul":
            attrs_count = len(current_element.attrs.keys())
            if attrs_count == 0:
                theses_text = current_element.text
                if new_theses is None:
                    new_theses = Thesis()
                    new_theses.text = theses_text
                else:
                    new_theses.text += '\n' + theses_text
                if index + 1 < len(all_tags) and all_tags[index + 1].name == "p":
                    after_theses_tag = all_tags[index + 1]
                    LCR = get_LCR(str(after_theses_tag.text))
                    LRE = get_LRE(str(after_theses_tag.text))
                    if LCR == "" or LRE == "":
                        new_theses.text += '\n' + str(after_theses_tag.text)
                    else:
                        new_theses.LCR = LCR
                        new_theses.LRE = LRE
                        theses_list.append(new_theses)
                        new_theses = None
                else:
                    new_theses = None
        index += 1

    return theses_list


def find_criteria_for_evaluating_div(browser):
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    header_of_criteria_div = soup.find(id="doc_criteria")
    criteria_div = header_of_criteria_div.findParent()
    return criteria_div


def get_criteria_for_evaluating(browser):
    criteria_div = find_criteria_for_evaluating_div(browser)
    if criteria_div is None:
        return ""

    table_tag = str(criteria_div.find('table'))
    return table_tag


# browser - webdriver на котором открыта страница с документом, с которого можно считать MKB
# return - объект Recommendation
def get_recommdendation_info(browser):
    recommendation = Recommendation()
    recommendation.nozology_name = get_nozology_name(browser)
    print(recommendation.nozology_name)
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
    recommendation.treatmentTheses = get_treatment_theses(browser)
    for element in recommendation.treatmentTheses:
        print(element.text)
        print(element.LCR)
        print(element.LRE)
        print("\n")
    recommendation.table_tag = get_criteria_for_evaluating(browser)
    print(recommendation.table_tag)
    return recommendation
