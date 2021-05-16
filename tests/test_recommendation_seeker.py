import json
import unittest

import requests
from selenium import webdriver

import recommendation_seeker
from data_structures import Thesis


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

    def test_find_treatment_theses_short_LCR_LRE(self):
        recommendation_content = requests.get(self.rec_seeker.RECOMMENDATION_URL.replace('__ID', '62_2'))
        self.rec_seeker._RecommendationSeeker__recommendation_content_json = json.loads(recommendation_content.text)
        res = self.rec_seeker._RecommendationSeeker__find_treatment_theses()
        expected_thesis_count = 8
        expected_thesis_text = ['Всем пациентам с АГ (кроме пациентов низкого риска с АД<150/90 мм рт. ст., пациентов',
                                'Пациентам, не достигшим целевого АД на фоне двойной',
                                'Пациентам с АГ, не достигшим целевого АД на фоне тройной',
                                'Всем пациентам с АГ не рекомендуется назначение комбинации двух блокаторов',
                                'У пациентов, не достигших целевого АД при приеме моно-',
                                'ББ рекомендованы в качестве антигипертензивной',
                                'Моксонидин для лечения АГ рекомендуется пациентам с МС',
                                'Альфа-адероноблокаторы рекомендуются при резистентной АГ'
                                ]
        expected_thesis_LCR = ['А', 'В', 'А', 'A', 'А', 'С', 'B', 'B']
        expected_thesis_LRE = ['1', '1', '1', '1', '1', '5', '3', '2']

        self.assertEqual(len(res), expected_thesis_count)
        for index in range(0, len(res)):
            self.assertTrue(res[index].text.__contains__(expected_thesis_text[index]))
            self.assertEqual(res[index].LCR, expected_thesis_LCR[index])
            self.assertEqual(res[index].LRE, expected_thesis_LRE[index])

    def test_find_treatment_theses_long_LCR_LRE(self):
        recommendation_content = requests.get(self.rec_seeker.RECOMMENDATION_URL.replace('__ID', '622_4'))
        self.rec_seeker._RecommendationSeeker__recommendation_content_json = json.loads(recommendation_content.text)
        res = self.rec_seeker._RecommendationSeeker__find_treatment_theses()
        expected_thesis_count = 6
        expected_thesis_text = ['Рекомендуется у детей с СД2 в возрасте >10 лет',
                                'Рекомендуется у детей с СД2 применение инсулинов длительного',
                                'Рекомендуется у детей с СД2 применение инсулинов',
                                'Рекомендуется у детей в возрасте >10 лет с СД2',
                                'Рекомендуется у детей с СД2, получающих инсулинотерапию, проводить',
                                'Рекомендуется у детей с СД2, получающих инсулинотерапию, при каждой инъекции',
                                ]
        expected_thesis_LCR = ['B', 'С', 'С', 'В', 'С', 'С']
        expected_thesis_LRE = ['2', '5', '5', '2', '5', '5']

        self.assertEqual(len(res), expected_thesis_count)
        for index in range(0, len(res)):
            self.assertTrue(res[index].text.__contains__(expected_thesis_text[index]))
            self.assertEqual(res[index].LCR, expected_thesis_LCR[index])
            self.assertEqual(res[index].LRE, expected_thesis_LRE[index])
