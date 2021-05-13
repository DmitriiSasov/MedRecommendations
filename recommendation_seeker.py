import re
import time
from typing import Dict

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
                all_headers = [html_parser.find_all('h2'), html_parser.find_all('h3')]
                for header_group in all_headers:
                    for header in header_group:
                        if bool(re.search(
                                '(((Медикаментозное)|(Лекарственное)) лечение)|(((Медикаментозная)|(Лекарственная)) терапия)',
                                header.text)):
                            theses = self.__extract_theses_from_block(header)

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

        def __contains_LCR_and_LRE(self, text: str):
            return re.search(r'(УУР.*УДД)|(У|уровень убедительности рекомендаций.*уровень достоверности доказательств)',
                      text) is not None

        def __get_LCR(self, text: str):
            res = re.match(r'((?<=ровень убедительности рекомендаций )|(?<=УУР ))\w((?= )|(?=\())', text)
            return res.group()

        def __get_LRE(self, text: str):
            res = re.match(r'"((?<=ровень достоверности доказательств )|(?<=ровень достоверности доказательств - )|(?<=УДД )|(?<=УДД - ))\d|[IV]{1,3}((?= )|(?=\)))"gm', text)
            return res.group()

        def extract_thesis(self):
            thesis = Thesis()
            if self.contains_thesis():
                if self.__contains_LCR_and_LRE(self.tag.text):
                    for sentence in self.tag.text.split('.'):
                        if not self.__contains_LCR_and_LRE(sentence):
                            thesis.text += sentence + '.'
                        else:
                            thesis.LCR = self.__get_LCR(sentence)
                            thesis.LRE = self.__get_LRE(sentence)
                else:
                    thesis.text = self.tag.text
                    thesis.LCR = self.__get_LCR(self.tag.next_sibling.text)
                    thesis.LRE = self.__get_LRE(self.tag.next_sibling.text)
            return thesis

    def __is_diagnosis_block(self, title: str):
        res = title == self.GLOBAL_DOCUMENT_SECTIONS[0]
        for section in self.DIAGNOSIS_SECTIONS:
            res = res or title == section
        return res

    def __is_diagnosis_subblock(self, title: str):
        res = False
        for diagnonis_section in self.DIAGNOSIS_SECTIONS:
            res = res or title.__contains__(diagnonis_section)
        return res

    def __transform_diagn_section_name_to_my_section_name(self, previous_section_name: str):
        name_without_numbers = ''
        words = previous_section_name.split(' ')
        if words[0] != '' and not words[0][0].isdigit():
            name_without_numbers += ' ' + words[0]
        for index in range(1, len(words)):
            if words[index] != '' and not words[index][0].isdigit():
                name_without_numbers += ' ' + words[index]

        new_section_name = ''
        if self.DIAGNOSIS_SECTIONS_TO_MY_DOC_SECTIONS.keys().__contains__(name_without_numbers):
            new_section_name = self.DIAGNOSIS_SECTIONS_TO_MY_DOC_SECTIONS[name_without_numbers]

        return new_section_name

    def __extract_theses_from_block(self, block_header: PageElement):
        theses = []
        current_subblock_tag = block_header.next_element
        thesis_seeker = self.ThesisSeeker(current_subblock_tag)
        while current_subblock_tag is not None and not ((current_subblock_tag.name == 'h2' or
                                                         current_subblock_tag.name == 'h3') and
                                                        block_header.name < current_subblock_tag.name):
            thesis_seeker.set_tag(current_subblock_tag)
            if thesis_seeker.contains_thesis():
                theses.append(thesis_seeker.extract_thesis())
            current_subblock_tag = current_subblock_tag.next_element
        return theses

    def __find_diagnosis_theses(self):
        theses = {self.DIAGNOSIS_SECTIONS[0]: [], self.DIAGNOSIS_SECTIONS[2]: [], self.DIAGNOSIS_SECTIONS[4]: [],
                  self.DIAGNOSIS_SECTIONS[5]: []}
        for section in self.__recommendation_content_json['obj']['sections']:
            if self.__is_diagnosis_block(section['title']) and section["content"] is not None:
                html_parser = BeautifulSoup(section["content"], 'html.parser')
                if section['title'].__contains__(self.GLOBAL_DOCUMENT_SECTIONS[0]):
                    all_headers = [html_parser.find_all('h2'), html_parser.find_all('h3')]
                    for header_group in all_headers:
                        for header in header_group:
                            if self.__is_diagnosis_subblock(header.text):
                                theses[self.__transform_diagn_section_name_to_my_section_name(header.text)] = \
                                    self.__extract_theses_from_block(header)
                else:
                    all_tags = html_parser.findAll(True, recursive=False)
                    thesis_seeker = self.ThesisSeeker(all_tags[0])
                    for tag in all_tags:
                        thesis_seeker.set_tag(tag)
                        if thesis_seeker.contains_thesis():
                            theses[self.__transform_diagn_section_name_to_my_section_name(section['title'])] = \
                                (thesis_seeker.extract_thesis())
        return theses

    def __find_mkbs(self):
        return list(filter(lambda a: a != '', re.split(r'[^\wа-яА-Я.]', self.__recommendation_content_json['mkb'])))

    def __find_criteria(self):
        for section in self.__recommendation_content_json['obj']['sections']:
            if section['title'] == "Критерии оценки качества медицинской помощи":
                html_parser = BeautifulSoup(section["content"], 'html.parser')
                criteria_table = html_parser.find('table')
                return criteria_table
