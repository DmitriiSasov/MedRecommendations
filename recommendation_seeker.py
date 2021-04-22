import re
import time
import requests
import json

from bs4 import BeautifulSoup, PageElement
from data_structures import Recommendation
from data_structures import Thesis


class RecommendationSeeker:
    RECOMMENDATION_URL = 'https://democenter.nitrosbase.com/clinrecalg5/API.ashx?op=GetClinrec2&id=__ID&ssid=undefined'

    GLOBAL_DOCUMENT_SECTIONS = ['2. Диагностика', '3. Лечение']
    DIAGNOSIS_SECTIONS = ['Физикальное обследование', 'Лабораторные диагностические исследования',
                          'Лабораторная диагностика', 'Инструментальные диагностические исследования',
                          'Инструментальная диагностика', 'Иные диагностические исследования']
    DIAGNOSIS_SECTIONS_TO_MY_DOC_SECTIONS = {'Физикальное обследование': 'Физикальное обследование',
                                             'Лабораторные диагностические исследования': 'Лабораторная диагностика',
                                             'Лабораторная диагностика': 'Лабораторная диагностика',
                                             'Инструментальные диагностические исследования': 'Инструментальная диагностика',
                                             'Инструментальная диагностика': 'Инструментальная диагностика',
                                             'Иные диагностические исследования': 'Иные диагностические исследования'}

    __recommendation_content_json = None

    def find_recommendation(self, identifier: str):
        recommendation_content = requests.get(self.RECOMMENDATION_URL.replace('__ID', identifier))
        if recommendation_content.status_code != 200:
            return False
        self.__recommendation_content_json = json.loads(recommendation_content.text)
        recommendation = Recommendation()
        recommendation.MKBs = self.__find_mkbs()
        recommendation.nozology_name = self.__recommendation_content_json['name']
        recommendation.table_tag = self.__find_criteria()
        recommendation.diagnosticTheses = self.__find_diagnosis_theses()
        recommendation.treatmentTheses = self.__find_treatment_theses()

    def __find_treatment_theses(self):
        theses = []
        for section in self.__recommendation_content_json['obj']['sections']:
            if section['title'] == self.GLOBAL_DOCUMENT_SECTIONS[1]:
                html_parser = BeautifulSoup(section["content"], 'html.parser')
                all_headers = [html_parser.find_all('h1'), html_parser.find_all('h2'), html_parser.find_all('h3')]
                medical_treatment_tag = None
                for header_group in all_headers:
                    for header in header_group:
                        if bool(re.search('(((Медикаментозное)|(Лекарственное)) лечение)|(((Медикаментозная)|(Лекарственная)) терапия)',
                                header.text)):
                            medical_treatment_tag = header
                            next_tag = header.next_element
                            thesis_seeker = self.ThesisSeeker(next_tag)
                            while not next_tag.name.__contains__('h1') and not next_tag.name.__contains__('h2') \
                                    and not next_tag.name.__contains__('h3'):
                                if thesis_seeker.contains_thesis():
                                    theses.append(thesis_seeker.extract_thesis())
                                next_tag = next_tag.next_element
                                thesis_seeker.set_tag(next_tag)
        return theses

    class ThesisSeeker:

        tag: PageElement = None

        def __init__(self, tag: PageElement):
            self.tag = tag

        def set_tag(self, tag: PageElement):
            self.tag = tag

        def contains_thesis(self):
            return self.tag.name.__contains__('ul') and \
                   (self.__contains_LCR_and_LRE(self.tag) or
                    self.tag.next_sibling is not None and
                    self.__contains_LCR_and_LRE(self.tag.next_sibling) and
                    self.tag.next_sibling.name.__contains__('p'))

        def __contains_LCR_and_LRE(self, tag: PageElement):
            # TODO
            return

        def extract_thesis(self):
            
            return Thesis()

    def __is_diagnosis_block(self, title: str):
        res = title == self.GLOBAL_DOCUMENT_SECTIONS[0]
        for section in self.DIAGNOSIS_SECTIONS:
            res = res or title == section
        return res

    def __find_diagnosis_theses(self):
        theses = {self.DIAGNOSIS_SECTIONS[0]: [], self.DIAGNOSIS_SECTIONS[2]: [], self.DIAGNOSIS_SECTIONS[4]: [],
                  self.DIAGNOSIS_SECTIONS[5]: []}
        for section in self.__recommendation_content_json['obj']['sections']:
            if self.__is_diagnosis_block(section['title']) and section["content"] is not None:
                html_parser = BeautifulSoup(section["content"], 'html.parser')
                if section['title'] != "2. Диагностика":

                    for tag in html_parser.findAll(True, recursive=False):
                        thesis_seeker = self.ThesisSeeker(tag)

        return theses

    def __find_mkbs(self):
        return list(filter(lambda a: a != '', re.split(r'[^\wа-яА-Я.]', self.__recommendation_content_json['mkb'])))

    def __find_criteria(self):
        for section in self.__recommendation_content_json['obj']['sections']:
            if section['title'] == "Критерии оценки качества медицинской помощи":
                html_parser = BeautifulSoup(section["content"], 'html.parser')
                criteria_table = html_parser.find('table')
                return criteria_table
