import unittest
import _parser


class TestParser(unittest.TestCase):

    def test_get_recommendation_page_url_empty_nosology_name(self):
        pass

    def test_get_recommendation_page_url_invalid_nosology_name(self):
        pass

    def test_get_recommendation_page_url_valid_nosology_name(self):
        pass

    def test_get_nozology_name_invalid_page(self):
        pass

    def test_get_nozology_name_valid_page(self):
        pass

    def test_get_MKBs_invalid_page(self):
        pass

    def test_get_MKBs_one_MKB(self):
        pass

    def test_get_MKBs_some_MKBs(self):
        pass

    def test_get_LCR_text_without_LCR(self):
        pass

    def test_get_LCR_text_with_correct_LCR_abbreviation(self):
        pass

    def test_get_LCR_text_with_LCR_no_abbreviation(self):
        pass

    def test_get_LCR_text_with_specific_LCR_wording(self):
        pass

    def test_get_LRE_text_without_LRE(self):
        pass

    def test_get_LRE_text_with_correct_LRE_abbreviation(self):
        pass

    def test_get_LRE_text_with_LRE_no_abbreviation(self):
        pass

    def test_get_LRE_text_with_specific_LRE_wording(self):
        pass

    def test_get_diagnosys_theses_invalid_page(self):
        pass

    def test_get_diagnosys_theses_page_with_usual_theses(self):
        pass

    def test_get_diagnosys_theses_page_with_unusual_theses(self):
        pass

    def test_get_treatment_tags_invalid_page(self):
        pass

    def test_get_treatment_tags_page_without_medication(self):
        pass

    def test_get_treatment_tags_page_with_medication(self):
        pass

    def test_get_treatment_theses_page_with_medication(self):
        pass

    def test_find_criteria_for_evaluating_div_invalid_page(self):
        pass

    def test_find_criteria_for_evaluating_div_valid_page(self):
        pass

    def test_get_criteria_for_evaluating_invalid_page(self):
        pass

    def test_get_criteria_for_evaluating_text_after_table(self):
        pass

    def test_get_criteria_for_evaluating_only_table(self):
        pass

    def test_get_recommendation_info_invalid_page(self):
        pass

    def test_get_recommendation_info_page_with_all_blocks(self):
        pass

    def test_get_recommendation_info_page_without_medication_block(self):
        pass

