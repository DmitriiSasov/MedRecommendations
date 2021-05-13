import json
import unittest

import requests
from selenium import webdriver

import recommendation_seeker


class TestParser(unittest.TestCase):

    # Создать тесты на случаи, когда не находятся теги или содержимое внутри тегов.

    rec_seeker = recommendation_seeker.RecommendationSeeker()

    def test_find_criteria(self):
        recommendation_content = requests.get(self.rec_seeker.RECOMMENDATION_URL.replace('__ID', '504_2'))
        self.rec_seeker._RecommendationSeeker__recommendation_content_json = json.loads(recommendation_content.text)
        res = self.rec_seeker._RecommendationSeeker__find_criteria()
        self.assertTrue(res.text.__contains__('Выполнено КТорганов грудной полости, брюшной полости с '
                                              'контрастирование, МРТ малого таза с контрастированием'))

    def test_find_mkbs(self):
        recommendation_content = requests.get(self.rec_seeker.RECOMMENDATION_URL.replace('__ID', '237_5'))
        self.rec_seeker._RecommendationSeeker__recommendation_content_json = json.loads(recommendation_content.text)
        res = self.rec_seeker._RecommendationSeeker__find_mkbs()
        self.assertEqual(res, ['C15', 'C16.0'])

    def test_is_diagnosis_block_no_diagnosis_block(self):
        res = self.rec_seeker._RecommendationSeeker__is_diagnosis_block('Термины и определения')
        self.assertFalse(res)

    def test_is_diagnosis_block_diagnosis_block(self):
        res = self.rec_seeker._RecommendationSeeker__is_diagnosis_block('2. Диагностика')
        self.assertTrue(res)

    def test_is_diagnosis_block_diagnosis_subblock(self):
        res = self.rec_seeker._RecommendationSeeker__is_diagnosis_block('2.3 Лабораторные диагностические исследования')
        self.assertTrue(res)

    def test_transform_diagn_section_name_to_my_section_name_correct_name(self):
        res = self.rec_seeker._RecommendationSeeker__transform_diagn_section_name_to_my_section_name(
            '2.3 Лабораторные диагностические исследования')
        self.assertTrue(res == 'Лабораторная диагностика')

    def test_transform_diagn_section_name_to_my_section_name_incorrect_name_without_numbers(self):
        res = self.rec_seeker._RecommendationSeeker__transform_diagn_section_name_to_my_section_name(
            'Ключевые слова')
        self.assertTrue(res == '')

    def test_transform_diagn_section_name_to_my_section_name_incorrect_name_with_numbers(self):
        res = self.rec_seeker._RecommendationSeeker__transform_diagn_section_name_to_my_section_name(
            '1.6 Клиническая картина заболевания или состояния (группы заболеваний или состояний)')
        self.assertTrue(res == '')
