import unittest

from bs4 import PageElement

from recommendation_seeker import RecommendationSeeker


class MyTestCase(unittest.TestCase):

    thesis_seeker = RecommendationSeeker.ThesisSeeker(PageElement(), None)

    def test_contains_LCR_and_LRE_long_and_many_dashes(self):
        text = 'Уровень убедительности рекомендаций – А (уровень достоверности доказательств – 1)'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertTrue(res)

    def test_contains_LCR_and_LRE_long_and_one_dash(self):
        text = 'Уровень убедительности рекомендаций С (уровень достоверности доказательств – 5)'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertTrue(res)

    def test_contains_LCR_and_LRE_long_and_no_dash(self):
        text = 'Уровень убедительности рекомендации C (уровень достоверности доказательств 5)'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertTrue(res)

    def test_contains_LCR_and_LRE_long_and_arabian_digits(self):
        text = 'Уровень убедительности рекомендаций B (уровень достоверности доказательств – II)'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertTrue(res)

    def test_contains_LCR_and_LRE_long_and_no_brackets(self):
        text = 'Уровень убедительности рекомендаций B Уровень достоверности доказательств 2'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertTrue(res)

    def test_contains_LCR_and_LRE_long_and_extra_digits_before(self):
        text = 'Уровень убедительности рекомендаций 1B Уровень достоверности доказательств 2'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertFalse(res)

    def test_contains_LCR_and_LRE_long_and_extra_digits_after(self):
        text = 'Уровень убедительности рекомендаций B1 Уровень достоверности доказательств 2'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertFalse(res)

    def test_contains_LCR_and_LRE_long_and_extra_char_before(self):
        text = 'Уровень убедительности рекомендаций B Уровень достоверности доказательств a2'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertFalse(res)

    def test_contains_LCR_and_LRE_long_and_extra_char_after(self):
        text = 'Уровень убедительности рекомендаций B Уровень достоверности доказательств IIa'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertFalse(res)

    def test_contains_LCR_and_LRE_long_and_no_LCR_and_LRE(self):
        text = 'до уменьшения воспаления и улучшения остроты зрения с'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertFalse(res)

    def test_contains_LCR_and_LRE_short_and_no_extra_info(self):
        text = 'УУР B, УДД 2'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertTrue(res)

    def test_contains_LCR_and_LRE_short_and_comma(self):
        text = 'ЕОК IС (УУР С, УДД 2).'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertTrue(res)

    def test_contains_LCR_and_LRE_short_and_point_comma(self):
        text = 'ЕОК IIIB (УУР B; УДД 2)'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertTrue(res)

    def test_contains_LCR_and_LRE_short_no_extra_spaces(self):
        text = 'ЕОК IIIB (УУР-BУДД-2)'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertTrue(res)

    def test_contains_LCR_and_LRE_short_extra_spaces(self):
        text = 'ЕОК IIIB (УУР     A          УДД  2)'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertTrue(res)

    def test_contains_LCR_and_LRE_short_arabian_digits(self):
        text = 'ЕОК IС (УУР С, УДД II).'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertTrue(res)

    def test_contains_LCR_and_LRE_extra_char_before_LRE(self):
        text = 'ЕОК IA (УУР B, УДД aV)'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertFalse(res)

    def test_contains_LCR_and_LRE_extra_char_after_LRE(self):
        text = 'ЕОК IA (УУР B, УДД Va)'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertFalse(res)

    def test_contains_LCR_and_LRE_extra_digit_after_LCR(self):
        text = 'ЕОК IA (УУР B1, УДД V)'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertFalse(res)

    def test_contains_LCR_and_LRE_extra_digit_before_LCR(self):
        text = 'ЕОК IA (УУР 1B, УДД V)'
        res = self.thesis_seeker._ThesisSeeker__contains_LCR_and_LRE(text)
        self.assertFalse(res)

