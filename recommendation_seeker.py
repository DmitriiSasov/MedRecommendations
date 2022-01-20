import re
import time
from typing import Dict

import requests
import json

from bs4 import BeautifulSoup, PageElement
from data_structures import Recommendation
from data_structures import Thesis


class RecommendationSeeker:
    RECOMMENDATION_URL = 'https://apicr.minzdrav.gov.ru/api.ashx?op=GetClinrec2&id=__ID&ssid=undefined'

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

    REGEX_FOR_LONG_LCR_AND_LRE = r'ровень убедительности рекомендаци[^0-9IV]*([АВСA-C])[^АВСA-C1-9IV].*ровень достоверности доказательств[^a-zA-Zа-яА-Я]*([1-5]|[IV]{1,3})([^a-zA-Zа-яА-Я]+|$)'
    REGEX_FOR_SHORT_LCR_AND_LRE = r'УУР[^0-9IV]*([АВСA-C])[^АВСA-C1-9IV]*УДД[^a-zA-Zа-яА-Я]*([1-5]|[IV]{1,3})([^a-zA-Zа-яА-Я]+|$)'
    __recommendation_content_json = None

    def find_recommendation(self, identifier: str):
        recommendation_content = requests.get(self.RECOMMENDATION_URL.replace('__ID', identifier))
        if recommendation_content.status_code != 200:
            return False
        self.__recommendation_content_json = json.loads(recommendation_content.text)
        recommendation = Recommendation(self.__recommendation_content_json['name'],
                                        self.__find_mkbs(),
                                        self.__find_diagnosis_theses(),
                                        self.__find_treatment_theses(),
                                        self.__find_criteria(),
                                        self.__find_creation_date())
        return recommendation

    def __find_creation_date(self):
        return self.__recommendation_content_json['created']

    def __find_treatment_theses(self):
        theses = []
        for section in self.__recommendation_content_json['obj']['sections']:
            if section['title'] == self.GLOBAL_DOCUMENT_SECTIONS[1]:
                html_parser = BeautifulSoup(section["content"], 'html.parser')
                all_tags = html_parser.find_all(['h2', 'h3', 'ul', 'p'], recursive=False)
                treatment_header_tag_index = -1
                index = 0
                while index < len(all_tags) and treatment_header_tag_index == -1:
                    if (all_tags[index].name == 'h2' or all_tags[index].name == 'h3') and \
                            bool(re.search(
                                r'(((Медикаментозное)|(Лекарственное)) лечение)|(((Медикаментозная)|(Лекарственная)) терапия)',
                                all_tags[index].text)):
                        treatment_header_tag_index = index
                    index += 1
                if treatment_header_tag_index != -1:
                    index = treatment_header_tag_index + 1
                    tags = []
                    while index < len(all_tags) and not ((all_tags[index].name == 'h2' or all_tags[index].name == 'h3')
                                                         and all_tags[treatment_header_tag_index].name >= all_tags[
                                                             index].name):
                        tags.append(all_tags[index])
                        index += 1
                    theses = self.__extract_theses_from_block(tags)

        return theses

    class ThesisSeeker:

        tag: PageElement = None

        next_tag: PageElement = None

        def __init__(self, tag: PageElement, next_tag):
            self.tag = tag
            self.next_tag = next_tag

        def set_tags(self, tag: PageElement, next_tag):
            self.tag = tag
            self.next_tag = next_tag

        def contains_thesis(self):
            try:
                res = self.tag.name.__contains__('ul') and \
                      (self.__contains_LCR_and_LRE(self.tag.text) or
                       self.next_tag is not None and
                       self.__contains_LCR_and_LRE(self.next_tag.text) and
                       self.next_tag.name.__contains__('p'))
            except Exception:
                res = False
            return res

        def __contains_LCR_and_LRE(self, text):
            res = re.search(RecommendationSeeker.REGEX_FOR_LONG_LCR_AND_LRE, text) is not None or \
                  re.search(RecommendationSeeker.REGEX_FOR_SHORT_LCR_AND_LRE, text) is not None
            return res

        def __get_LCR(self, text):
            res = re.search(RecommendationSeeker.REGEX_FOR_LONG_LCR_AND_LRE, text)
            if res is None:
                res = re.search(RecommendationSeeker.REGEX_FOR_SHORT_LCR_AND_LRE, text)
            if res is None:
                return ''
            else:
                return res.group(1)

        def __get_LRE(self, text):
            res = re.search(RecommendationSeeker.REGEX_FOR_LONG_LCR_AND_LRE, text)
            if res is None:
                res = re.search(RecommendationSeeker.REGEX_FOR_SHORT_LCR_AND_LRE, text)
            if res is None:
                return ''
            else:
                return res.group(2)

        def extract_thesis(self):
            thesis = Thesis("", "", "")
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
                    thesis.LCR = self.__get_LCR(self.next_tag.text)
                    thesis.LRE = self.__get_LRE(self.next_tag.text)
            return thesis

    def __is_diagnosis_block(self, title: str):
        return title == self.GLOBAL_DOCUMENT_SECTIONS[0] or self.__is_diagnosis_subblock(title)

    def __is_diagnosis_subblock(self, title: str):
        res = False
        for diagnonis_section in self.DIAGNOSIS_SECTIONS:
            res = res or title.__contains__(diagnonis_section)
        return res

    def __transform_diagn_section_name_to_my_section_name(self, previous_section_name: str):
        name_without_numbers = ''
        words = previous_section_name.split(' ')
        for index in range(1, len(words)):
            if words[index] != '' and not words[index][0].isdigit():
                if name_without_numbers != '':
                    name_without_numbers += ' '
                name_without_numbers += words[index]

        new_section_name = ''
        if list(self.DIAGNOSIS_SECTIONS_TO_MY_DOC_SECTIONS.keys()).count(name_without_numbers) > 0:
            new_section_name = self.DIAGNOSIS_SECTIONS_TO_MY_DOC_SECTIONS[name_without_numbers]

        return new_section_name

    def __extract_theses_from_block(self, tags: list):
        theses = []
        if len(tags) == 0:
            return theses
        thesis_seeker = self.ThesisSeeker(tags[0], None)
        for index in range(0, len(tags)):
            if index == len(tags) - 1:
                thesis_seeker.set_tags(tags[index], None)
            else:
                thesis_seeker.set_tags(tags[index], tags[index + 1])
            if thesis_seeker.contains_thesis():
                theses.append(thesis_seeker.extract_thesis())

        return theses

    def __find_diagnosis_theses(self):
        theses = {self.DIAGNOSIS_SECTIONS[0]: [], self.DIAGNOSIS_SECTIONS[2]: [], self.DIAGNOSIS_SECTIONS[4]: [],
                  self.DIAGNOSIS_SECTIONS[5]: []}
        for section in self.__recommendation_content_json['obj']['sections']:
            if self.__is_diagnosis_block(section['title']) and section["content"] is not None:
                html_parser = BeautifulSoup(section["content"], 'html.parser')
                if section['title'].__contains__(self.GLOBAL_DOCUMENT_SECTIONS[0]):
                    all_tags = html_parser.find_all(['h2', 'h3', 'ul', 'p'], recursive=False)
                    index = 0
                    tags = []
                    current_header_index = -1
                    while index < len(all_tags):
                        # находим заголовок нужного раздела диагностики
                        if (all_tags[index].name == 'h2' or all_tags[index].name == 'h3') and \
                                self.__is_diagnosis_subblock(all_tags[index].text):
                            if current_header_index != -1:
                                theses[self.__transform_diagn_section_name_to_my_section_name(
                                    all_tags[current_header_index].text)] = self.__extract_theses_from_block(tags)
                            tags = []
                            current_header_index = index
                        # находим заголовок ненужного раздела диагностики
                        if current_header_index != -1 and \
                                (all_tags[index].name == 'h2' or all_tags[index].name == 'h3') and \
                                not self.__is_diagnosis_subblock(all_tags[index].text) and \
                                all_tags[current_header_index].name >= all_tags[index].name:
                            theses[self.__transform_diagn_section_name_to_my_section_name(
                                all_tags[current_header_index].text)] = self.__extract_theses_from_block(tags)
                            tags = []
                            current_header_index = - 1
                        # добавляем тезис из текущего раздела
                        if current_header_index != -1:
                            tags.append(all_tags[index])
                        index += 1
                        if index == len(all_tags) and current_header_index != -1:
                            theses[self.__transform_diagn_section_name_to_my_section_name(
                                all_tags[current_header_index].text)] = self.__extract_theses_from_block(tags)
                            tags = []
                else:
                    all_tags = html_parser.findAll(['ul', 'p'], recursive=False)
                    theses[self.__transform_diagn_section_name_to_my_section_name(section['title'])] = \
                        self.__extract_theses_from_block(all_tags)
        return theses

    def __find_mkbs(self):
        return list(filter(lambda a: a != '', re.split(r'[^\wа-яА-Я.]', self.__recommendation_content_json['mkb'])))

    def __find_criteria(self):
        for section in self.__recommendation_content_json['obj']['sections']:
            if section['title'] == "Критерии оценки качества медицинской помощи":
                html_parser = BeautifulSoup(section["content"], 'html.parser')
                criteria_table = html_parser.find('table')
                return criteria_table
