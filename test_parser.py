import unittest

from selenium import webdriver

import backend._parser


class TestParser(unittest.TestCase):

    def test_get_recommendation_page_url_empty_nosology_name(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(10)
        result = backend._parser.get_recommendation_page_url(browser, "")

        self.assertFalse(result)

    def test_get_recommendation_page_url_invalid_nosology_name(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(10)
        result = backend._parser.get_recommendation_page_url(browser, "шапывап")

        self.assertFalse(result)

    def test_get_recommendation_page_url_valid_nosology_name(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(10)
        result = backend._parser.get_recommendation_page_url(browser, "f")
        expected_result = 'http://cr.rosminzdrav.ru/#!/schema/947'
        self.assertEqual(result, expected_result)

    def test_go_to_recommendation_page_invalid_nosology_id(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(10)
        result = backend._parser.go_to_recommendation_page(browser, "шапывап")

        self.assertFalse(result)

    def test_go_to_recommendation_page_valid_nosology_id(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(10)
        result = backend._parser.go_to_recommendation_page(browser, "f")

        self.assertTrue(result)

    def test_get_nozology_name_invalid_page(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/#!/')
        result = backend._parser.get_nozology_name(browser)
        expected_result = ''

        self.assertEqual(result, expected_result)

    def test_get_nozology_name_valid_page(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/#!/schema/964')
        result = backend._parser.get_nozology_name(browser)
        expected_result = 'Сахарный диабет 1 типа у детей'

        self.assertEqual(result, expected_result)

    def test_get_MKBs_invalid_page(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/#!/')
        result = backend._parser.get_MKBs(browser)
        expected_result = []

        self.assertEqual(result, expected_result)

    def test_get_MKBs_one_MKB(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/#!/schema/38')
        result = backend._parser.get_MKBs(browser)
        expected_result = ' H80 '.split('/')

        self.assertEqual(result, expected_result)

    def test_get_MKBs_some_MKBs(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/#!/schema/964')
        result = backend._parser.get_MKBs(browser)
        expected_result = 'E10.1/E10.2/E10.3/E10.4/E10.5/E10.6/E10.7/E10.8/E10.9'.split('/')

        self.assertEqual(result, expected_result)

    def test_get_LCR_text_without_LCR(self):
        text = """Лечение СД1 у детей складывается из следующих основных компонентов:
                инсулинотерапия;
                обучение самоконтролю и проведение его в домашних условиях;
                питание;
                физические нагрузки;
                психологическая помощь. доказательств"""
        result = backend._parser.get_LCR(text)
        expected_result = ''

        self.assertEqual(result, expected_result)

    def test_get_LCR_text_with_correct_LCR_abbreviation(self):
        text = 'ЕОК/ЕОАГ IIаB (УУР B, УДД 1)'
        result = backend._parser.get_LCR(text)
        expected_result = 'B'

        self.assertEqual(result, expected_result)

    def test_get_LCR_text_with_LCR_no_abbreviation(self):
        text = 'Уровень убедительности рекомендаций А (уровень достоверности доказательств – 3)'
        result = backend._parser.get_LCR(text)
        expected_result = 'А'

        self.assertEqual(result, expected_result)

    def test_get_LCR_text_with_specific_LCR_wording(self):
        text = 'Показатель качества рекомендаций А (Показатель уровня доказательств – 3)'
        result = backend._parser.get_LCR(text)
        expected_result = 'А'

        self.assertEqual(result, expected_result)

    def test_get_LRE_text_without_LRE(self):
        text = """Лечение СД1 у детей складывается из следующих основных компонентов:
                        инсулинотерапия;
                        обучение самоконтролю и проведение его в домашних условиях;
                        питание;
                        физические нагрузки;
                        психологическая помощь. доказательств"""
        result = backend._parser.get_LRE(text)
        expected_result = ''

        self.assertEqual(result, expected_result)

    def test_get_LRE_text_with_correct_LRE_abbreviation(self):
        text = 'ЕОК/ЕОАГ IIаB (УУР B, УДД 1)'
        result = backend._parser.get_LRE(text)
        expected_result = '1'

        self.assertEqual(result, expected_result)

    def test_get_LRE_text_with_LRE_no_abbreviation(self):
        text = 'Уровень убедительности рекомендаций А (уровень достоверности доказательств – 3)'
        result = backend._parser.get_LRE(text)
        expected_result = '3'

        self.assertEqual(result, expected_result)

    def test_get_LRE_text_with_specific_LRE_wording(self):
        text = 'Показатель качества рекомендаций А (Показатель уровня доказательств – 3)'
        result = backend._parser.get_LRE(text)
        expected_result = '3'

        self.assertEqual(result, expected_result)

    def test_get_diagnosys_theses_invalid_page(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/')
        result = backend._parser.get_diagnosys_theses(browser)
        expected_result = {}

        self.assertEqual(result, expected_result)

    def test_get_diagnosys_theses_page_with_usual_theses(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(10)
        browser.get('http://cr.rosminzdrav.ru/#!/schema/964')
        browser.find_element_by_id('mkb')
        theses = backend._parser.get_diagnosys_theses(browser)
        result = []
        for key in theses:
            result.append(len(theses[key]))

        expected_result = [0, 0, 0, 4, 2, 0, 0]

        self.assertEqual(result, expected_result)

    def test_get_diagnosys_theses_page_with_unusual_theses(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(10)
        browser.get('http://cr.rosminzdrav.ru/#!/schema/687')
        browser.find_element_by_id('mkb')
        theses = backend._parser.get_diagnosys_theses(browser)
        result = []
        for key in theses:
            result.append(len(theses[key]))

        expected_result = [0, 3, 0, 4, 3, 1, 2, 7, 7, 1]

        self.assertEqual(result, expected_result)

    def test_get_treatment_tags_invalid_page(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/')
        result = backend._parser.get_treatment_tags(browser)
        expected_result = []

        self.assertEqual(result, expected_result)

    def test_get_treatment_tags_page_without_medication(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/#!/schema/964')
        browser.find_element_by_id('mkb')
        result = backend._parser.get_treatment_tags(browser)
        expected_result = []

        self.assertEqual(result, expected_result)

    def test_get_treatment_tags_page_with_medication(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/#!/schema/687')
        browser.find_element_by_id('mkb')
        result = backend._parser.get_treatment_tags(browser)
        expected_result_1 = 56
        expected_result_2 = 'p'
        expected_result_3 = 'ul'

        self.assertEqual(len(result), expected_result_1)
        self.assertEqual(result[55].name, expected_result_2)
        self.assertEqual(result[54].name, expected_result_3)

    def test_get_treatment_theses_page_with_medication(self):

        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/#!/schema/687')
        browser.find_element_by_id('mkb')
        result = backend._parser.get_treatment_theses(browser)
        expected_result_1 = 8
        expected_result_2 = 'B'
        expected_result_3 = '2'

        self.assertEqual(len(result), expected_result_1)
        self.assertEqual(result[7].LCR, expected_result_2)
        self.assertEqual(result[7].LRE, expected_result_3)

    def test_find_criteria_for_evaluating_div_invalid_page(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/')
        result = backend._parser.find_criteria_for_evaluating_div(browser)
        expected_result = None

        self.assertEqual(result, expected_result)

    def test_find_criteria_for_evaluating_div_valid_page(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/#!/schema/687')
        browser.find_element_by_id('mkb')
        result = backend._parser.find_criteria_for_evaluating_div(browser)

        self.assertTrue(result is not None)

    def test_get_criteria_for_evaluating_invalid_page(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/')
        result = backend._parser.get_criteria_for_evaluating(browser)
        expected_result = ''

        self.assertEqual(result, expected_result)

    def test_get_criteria_for_evaluating_text_after_table(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/#!/schema/687')
        browser.find_element_by_id('mkb')
        result = backend._parser.get_criteria_for_evaluating(browser)

        self.assertTrue(result is not None)
        self.assertTrue(result.__contains__('Выполнен общий анализ крови'))
        self.assertFalse(result.__contains__('Типичными дефектами при оказании медицинской '
                                             'помощи пациентам с АГ являются'))

    def test_get_criteria_for_evaluating_only_table(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/#!/schema/964')
        browser.find_element_by_id('mkb')
        result = backend._parser.get_criteria_for_evaluating(browser)

        self.assertTrue(result is not None)
        self.assertTrue(result.__contains__('Выполнено измерение гликемии не реже 6 раз в 24 часа ежедневно'))
        self.assertFalse(result.__contains__('Критерии оценки качества'))
        self.assertFalse(result.__contains__('Список литературы'))

    def test_get_recommendation_info_invalid_page(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(3)
        browser.get('http://cr.rosminzdrav.ru/')
        result = backend._parser.get_recommdendation_info(browser)
        expected_nosology_name = ''
        expected_MKBs = []
        expected_diagnostic_theses = {}
        expected_treatment_theses = []
        expected_table_tag = ''

        self.assertEqual(result.nozology_name, expected_nosology_name)
        self.assertEqual(result.MKBs, expected_MKBs)
        self.assertEqual(result.diagnosticTheses, expected_diagnostic_theses)
        self.assertEqual(result.treatmentTheses, expected_treatment_theses)
        self.assertEqual(result.table_tag, expected_table_tag)

    def test_get_recommendation_info_page_with_all_blocks(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(10)
        backend._parser.go_to_recommendation_page(browser, 'i10')
        result = backend._parser.get_recommdendation_info(browser)
        diagnosys_theses_count_in_groups = []
        for key in result.diagnosticTheses:
            diagnosys_theses_count_in_groups.append(len(result.diagnosticTheses[key]))

        expected_nosology_name = 'Артериальная гипертензия у взрослых'
        expected_MKBs = ' I10/ I11/ I12/ I13/ I15 '.split('/')
        expected_diagnostic_theses_count_in_groups = [0, 3, 0, 4, 3, 1, 2, 7, 7, 1]
        expected_treatment_theses_count = 8
        expected_table_data = 'table border="0" cellpadding="0" cellspacing="0" width="100%"'

        self.assertEqual(result.nozology_name, expected_nosology_name)
        self.assertEqual(result.MKBs, expected_MKBs)
        self.assertEqual(diagnosys_theses_count_in_groups, expected_diagnostic_theses_count_in_groups)
        self.assertEqual(len(result.treatmentTheses), expected_treatment_theses_count)
        self.assertTrue(result.table_tag.__contains__(expected_table_data))

    def test_get_recommendation_info_page_without_medication_block(self):
        browser = webdriver.Chrome('backend\\chromedriver.exe')
        browser.implicitly_wait(10)
        backend._parser.go_to_recommendation_page(browser, 'e10')
        result = backend._parser.get_recommdendation_info(browser)
        diagnosys_theses_count_in_groups = []
        for key in result.diagnosticTheses:
            diagnosys_theses_count_in_groups.append(len(result.diagnosticTheses[key]))

        expected_nosology_name = 'Сахарный диабет 1 типа у детей'
        expected_MKBs = 'E10.1/E10.2/E10.3/E10.4/E10.5/E10.6/E10.7/E10.8/E10.9'.split('/')
        expected_diagnostic_theses_count_in_groups =  [0, 0, 0, 4, 2, 0, 0]
        expected_treatment_theses_count = 0
        expected_table_data = '<table border="1" cellpadding="0" cellspacing="0" width="101%">'

        self.assertEqual(result.nozology_name, expected_nosology_name)
        self.assertEqual(result.MKBs, expected_MKBs)
        self.assertEqual(diagnosys_theses_count_in_groups, expected_diagnostic_theses_count_in_groups)
        self.assertEqual(len(result.treatmentTheses), expected_treatment_theses_count)
        self.assertTrue(result.table_tag.__contains__(expected_table_data))
