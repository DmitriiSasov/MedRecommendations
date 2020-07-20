import unittest
from backend.sort_document import get_mkbs, get_criterias, get_nosologies, lcr_replace, lre_replace, sort, \
    combine_recommendations, sort_treatment_theses, sort_diagnostic_theses
from backend.data_structures import Recommendation, Thesis

recommendation1 = Recommendation()
recommendation1.MKBs = ['H80']
recommendation1.table_tag = 'first criteria'
recommendation1.nozology_name = 'first nosology'
diagnostic_thesis1_rec1 = Thesis()
diagnostic_thesis1_rec1.text = 'Первый тезис в физикальном обследовании первой рекоммендации'
diagnostic_thesis1_rec1.LCR = 'А'
diagnostic_thesis1_rec1.LRE = 'I'
recommendation1.diagnosticTheses = {'Физикальное обследование': [diagnostic_thesis1_rec1]}
treatment_thesis1_rec1 = Thesis()
treatment_thesis1_rec1.text = 'Первый тезис в Лечении первой рекомендации'
treatment_thesis1_rec1.LCR = 'B'
treatment_thesis1_rec1.LRE = '2'
treatment_thesis2_rec1 = Thesis()
treatment_thesis2_rec1.text = 'Второй тезис в Лечении первой рекомендации'
treatment_thesis2_rec1.LCR = 'A'
treatment_thesis2_rec1.LRE = '3'
treatment_theses_rec1 = [treatment_thesis1_rec1, treatment_thesis2_rec1]
recommendation1.treatmentTheses = treatment_theses_rec1

recommendation2 = Recommendation()
recommendation2.MKBs = ['I10', 'I11', 'I12', 'I13']
recommendation2.table_tag = 'second criteria'
recommendation2.nozology_name = 'second nosology'
diagnostic_thesis1_rec2 = Thesis()
diagnostic_thesis1_rec2.text = 'Первый тезис в физикальном обследовании второй рекоммендации'
diagnostic_thesis1_rec2.LCR = 'С'
diagnostic_thesis1_rec2.LRE = 'II'
diagnostic_thesis2_rec2 = Thesis()
diagnostic_thesis2_rec2.text = 'Второй тезис в физикальном обследовании второй рекоммендации'
diagnostic_thesis2_rec2.LCR = 'В'
diagnostic_thesis2_rec2.LRE = 'III'
diagnostic_thesis3_rec2 = Thesis()
diagnostic_thesis3_rec2.text = 'Первый тезис в лабораторной диагностике второй рекоммендации'
diagnostic_thesis3_rec2.LCR = 'А'
diagnostic_thesis3_rec2.LRE = 'V'
diagnostic_thesis4_rec2 = Thesis()
diagnostic_thesis4_rec2.text = 'Первый тезис в инструментальной диагностике второй рекоммендации'
diagnostic_thesis4_rec2.LCR = 'А'
diagnostic_thesis4_rec2.LRE = 'IV'
recommendation2.diagnosticTheses = {'Физикальное обследование': [diagnostic_thesis1_rec2, diagnostic_thesis2_rec2],
                                    'Лабораторная диагностика': [diagnostic_thesis3_rec2],
                                    'Инструментальная диагностика': [diagnostic_thesis4_rec2]}
treatment_thesis1_rec2 = Thesis()
treatment_thesis1_rec2.text = 'Первый тезис в Лечении второй рекомендации'
treatment_thesis1_rec2.LCR = 'C'
treatment_thesis1_rec2.LRE = '5'
treatment_thesis2_rec2 = Thesis()
treatment_thesis2_rec2.text = 'Второй тезис в Лечении второй рекомендации'
treatment_thesis2_rec2.LCR = 'C'
treatment_thesis2_rec2.LRE = '4'
treatment_thesis3_rec2 = Thesis()
treatment_thesis3_rec2.text = 'Третий тезис в Лечении второй рекомендации'
treatment_thesis3_rec2.LCR = 'C'
treatment_thesis3_rec2.LRE = '4'
treatment_theses_rec2 = [treatment_thesis1_rec2, treatment_thesis2_rec2, treatment_thesis3_rec2]
recommendation2.treatmentTheses = treatment_theses_rec2

recommendation3 = Recommendation()
recommendation3.MKBs = ['H25.1', 'H25.2', 'H25.3']
recommendation3.table_tag = 'third criteria'
recommendation3.nozology_name = 'third nosology'
diagnostic_thesis1_rec3 = Thesis()
diagnostic_thesis1_rec3.text = 'Первый тезис в физикальном обследовании третьей рекоммендации'
diagnostic_thesis1_rec3.LCR = 'C'
diagnostic_thesis1_rec3.LRE = '5'
diagnostic_thesis2_rec3 = Thesis()
diagnostic_thesis2_rec3.text = 'Второй тезис в физикальном обследовании третьей рекоммендации'
diagnostic_thesis2_rec3.LCR = 'C'
diagnostic_thesis2_rec3.LRE = '3'
diagnostic_thesis3_rec3 = Thesis()
diagnostic_thesis3_rec3.text = 'Первый тезис в лабораторной диагностике третьей рекоммендации'
diagnostic_thesis3_rec3.LCR = 'B'
diagnostic_thesis3_rec3.LRE = '2'
diagnostic_thesis4_rec3 = Thesis()
diagnostic_thesis4_rec3.text = 'Второй тезис в лабораторной диагностике третьей рекоммендации'
diagnostic_thesis4_rec3.LCR = 'A'
diagnostic_thesis4_rec3.LRE = '4'
diagnostic_thesis5_rec3 = Thesis()
diagnostic_thesis5_rec3.text = 'Первый тезис в инструментальной диагностике третьей рекоммендации'
diagnostic_thesis5_rec3.LCR = 'B'
diagnostic_thesis5_rec3.LRE = '3'
diagnostic_thesis6_rec3 = Thesis()
diagnostic_thesis6_rec3.text = 'Первый тезис в иных диагностических исследованиях третьей рекоммендации'
diagnostic_thesis6_rec3.LCR = 'A'
diagnostic_thesis6_rec3.LRE = '1'
recommendation3.diagnosticTheses = {'Физикальное обследование': [diagnostic_thesis1_rec3, diagnostic_thesis2_rec3],
                                    'Лабораторная диагностика': [diagnostic_thesis3_rec3, diagnostic_thesis4_rec3],
                                    'Инструментальная диагностика': [diagnostic_thesis5_rec3],
                                    'Иные диагностические исследования': [diagnostic_thesis6_rec3]}
treatment_thesis1_rec3 = Thesis()
treatment_thesis1_rec3.text = 'Первый тезис в Лечении третьей рекомендации'
treatment_thesis1_rec3.LCR = 'A'
treatment_thesis1_rec3.LRE = '1'
treatment_thesis2_rec3 = Thesis()
treatment_thesis2_rec3.text = 'Второй тезис в Лечении третьей рекомендации'
treatment_thesis2_rec3.LCR = 'B'
treatment_thesis2_rec3.LRE = '2'
treatment_thesis3_rec3 = Thesis()
treatment_thesis3_rec3.text = 'Третий тезис в Лечении третьей рекомендации'
treatment_thesis3_rec3.LCR = 'A'
treatment_thesis3_rec3.LRE = '4'
treatment_theses_rec3 = [treatment_thesis1_rec3, treatment_thesis2_rec3, treatment_thesis3_rec3]
recommendation3.treatmentTheses = treatment_theses_rec3

recommendations1 = [recommendation1]
recommendations2 = [recommendation2]
recommendations3 = [recommendation1, recommendation2, recommendation3]
recommendations_empty = []


def thesis_compare(first, second):
    if first.text == second.text and \
            first.LCR == second.LCR and \
            first.LRE == second.LRE:
        return 1
    else:
        return 0


def make_diagnostic_theses_for_combine_test():
    expected_physical_theses1 = Thesis()
    expected_physical_theses1.text = 'Первый тезис в физикальном обследовании первой рекоммендации'
    expected_physical_theses1.LCR = 'А'
    expected_physical_theses1.LRE = 'I'
    expected_physical_theses2 = Thesis()
    expected_physical_theses2.text = 'Первый тезис в физикальном обследовании второй рекоммендации'
    expected_physical_theses2.LCR = 'С'
    expected_physical_theses2.LRE = 'II'
    expected_physical_theses3 = Thesis()
    expected_physical_theses3.text = 'Второй тезис в физикальном обследовании второй рекоммендации'
    expected_physical_theses3.LCR = 'В'
    expected_physical_theses3.LRE = 'III'
    expected_physical_theses4 = Thesis()
    expected_physical_theses4.text = 'Первый тезис в физикальном обследовании третьей рекоммендации'
    expected_physical_theses4.LCR = 'C'
    expected_physical_theses4.LRE = '5'
    expected_physical_theses5 = Thesis()
    expected_physical_theses5.text = 'Второй тезис в физикальном обследовании третьей рекоммендации'
    expected_physical_theses5.LCR = 'C'
    expected_physical_theses5.LRE = '3'

    expected_lab_theses1 = Thesis()
    expected_lab_theses1.text = 'Первый тезис в лабораторной диагностике второй рекоммендации'
    expected_lab_theses1.LCR = 'А'
    expected_lab_theses1.LRE = 'V'
    expected_lab_theses2 = Thesis()
    expected_lab_theses2.text = 'Первый тезис в лабораторной диагностике третьей рекоммендации'
    expected_lab_theses2.LCR = 'B'
    expected_lab_theses2.LRE = '2'
    expected_lab_theses3 = Thesis()
    expected_lab_theses3.text = 'Второй тезис в лабораторной диагностике третьей рекоммендации'
    expected_lab_theses3.LCR = 'A'
    expected_lab_theses3.LRE = '4'

    expected_instrumental_theses1 = Thesis()
    expected_instrumental_theses1.text = 'Первый тезис в инструментальной диагностике второй рекоммендации'
    expected_instrumental_theses1.LCR = 'А'
    expected_instrumental_theses1.LRE = 'IV'
    expected_instrumental_theses2 = Thesis()
    expected_instrumental_theses2.text = 'Первый тезис в инструментальной диагностике третьей рекоммендации'
    expected_instrumental_theses2.LCR = 'B'
    expected_instrumental_theses2.LRE = '3'

    expected_other_theses1 = Thesis()
    expected_other_theses1.text = 'Первый тезис в иных диагностических исследованиях третьей рекоммендации'
    expected_other_theses1.LCR = 'A'
    expected_other_theses1.LRE = '1'

    expected_diagnostic_theses = \
        {'Физикальное обследование': [expected_physical_theses1,
                                      expected_physical_theses2,
                                      expected_physical_theses3,
                                      expected_physical_theses4,
                                      expected_physical_theses5],
         'Лабораторная диагностика': [expected_lab_theses1,
                                      expected_lab_theses2,
                                      expected_lab_theses3],
         'Инструментальная диагностика': [expected_instrumental_theses1,
                                          expected_instrumental_theses2],
         'Иные диагностические исследования': [expected_other_theses1]}

    return expected_diagnostic_theses


def make_treatment_theses_for_combine_test():
    expected_treatment_thesis1 = Thesis()
    expected_treatment_thesis1.text = 'Первый тезис в Лечении первой рекомендации'
    expected_treatment_thesis1.LCR = 'B'
    expected_treatment_thesis1.LRE = '2'
    expected_treatment_thesis2 = Thesis()
    expected_treatment_thesis2.text = 'Второй тезис в Лечении первой рекомендации'
    expected_treatment_thesis2.LCR = 'A'
    expected_treatment_thesis2.LRE = '3'
    expected_treatment_thesis3 = Thesis()
    expected_treatment_thesis3.text = 'Первый тезис в Лечении второй рекомендации'
    expected_treatment_thesis3.LCR = 'C'
    expected_treatment_thesis3.LRE = '5'
    expected_treatment_thesis4 = Thesis()
    expected_treatment_thesis4.text = 'Второй тезис в Лечении второй рекомендации'
    expected_treatment_thesis4.LCR = 'C'
    expected_treatment_thesis4.LRE = '4'
    expected_treatment_thesis5 = Thesis()
    expected_treatment_thesis5.text = 'Третий тезис в Лечении второй рекомендации'
    expected_treatment_thesis5.LCR = 'C'
    expected_treatment_thesis5.LRE = '4'
    expected_treatment_thesis6 = Thesis()
    expected_treatment_thesis6.text = 'Первый тезис в Лечении третьей рекомендации'
    expected_treatment_thesis6.LCR = 'A'
    expected_treatment_thesis6.LRE = '1'
    expected_treatment_thesis7 = Thesis()
    expected_treatment_thesis7.text = 'Второй тезис в Лечении третьей рекомендации'
    expected_treatment_thesis7.LCR = 'B'
    expected_treatment_thesis7.LRE = '2'
    expected_treatment_thesis8 = Thesis()
    expected_treatment_thesis8.text = 'Третий тезис в Лечении третьей рекомендации'
    expected_treatment_thesis8.LCR = 'A'
    expected_treatment_thesis8.LRE = '4'
    expected_treatment_theses = [expected_treatment_thesis1, expected_treatment_thesis2, expected_treatment_thesis3,
                                 expected_treatment_thesis4, expected_treatment_thesis5, expected_treatment_thesis6,
                                 expected_treatment_thesis7, expected_treatment_thesis8]

    return expected_treatment_theses


def make_diagnostic_theses_for_sort_test():
    expected_physical_theses1 = Thesis()
    expected_physical_theses1.text = 'Первый тезис в физикальном обследовании первой рекоммендации'
    expected_physical_theses1.LCR = 'A'
    expected_physical_theses1.LRE = '1'
    expected_physical_theses2 = Thesis()
    expected_physical_theses2.text = 'Второй тезис в физикальном обследовании второй рекоммендации'
    expected_physical_theses2.LCR = 'B'
    expected_physical_theses2.LRE = '3'
    expected_physical_theses3 = Thesis()
    expected_physical_theses3.text = 'Первый тезис в физикальном обследовании второй рекоммендации'
    expected_physical_theses3.LCR = 'C'
    expected_physical_theses3.LRE = '2'
    expected_physical_theses4 = Thesis()
    expected_physical_theses4.text = 'Второй тезис в физикальном обследовании третьей рекоммендации'
    expected_physical_theses4.LCR = 'C'
    expected_physical_theses4.LRE = '3'
    expected_physical_theses5 = Thesis()
    expected_physical_theses5.text = 'Первый тезис в физикальном обследовании третьей рекоммендации'
    expected_physical_theses5.LCR = 'C'
    expected_physical_theses5.LRE = '5'

    expected_lab_theses1 = Thesis()
    expected_lab_theses1.text = 'Второй тезис в лабораторной диагностике третьей рекоммендации'
    expected_lab_theses1.LCR = 'A'
    expected_lab_theses1.LRE = '4'
    expected_lab_theses2 = Thesis()
    expected_lab_theses2.text = 'Первый тезис в лабораторной диагностике второй рекоммендации'
    expected_lab_theses2.LCR = 'A'
    expected_lab_theses2.LRE = '5'
    expected_lab_theses3 = Thesis()
    expected_lab_theses3.text = 'Первый тезис в лабораторной диагностике третьей рекоммендации'
    expected_lab_theses3.LCR = 'B'
    expected_lab_theses3.LRE = '2'

    expected_instrumental_theses1 = Thesis()
    expected_instrumental_theses1.text = 'Первый тезис в инструментальной диагностике второй рекоммендации'
    expected_instrumental_theses1.LCR = 'A'
    expected_instrumental_theses1.LRE = '4'
    expected_instrumental_theses2 = Thesis()
    expected_instrumental_theses2.text = 'Первый тезис в инструментальной диагностике третьей рекоммендации'
    expected_instrumental_theses2.LCR = 'B'
    expected_instrumental_theses2.LRE = '3'

    expected_other_theses1 = Thesis()
    expected_other_theses1.text = 'Первый тезис в иных диагностических исследованиях третьей рекоммендации'
    expected_other_theses1.LCR = 'A'
    expected_other_theses1.LRE = '1'

    expected_diagnostic_theses = \
        {'Физикальное обследование': [expected_physical_theses1,
                                      expected_physical_theses2,
                                      expected_physical_theses3,
                                      expected_physical_theses4,
                                      expected_physical_theses5],
         'Лабораторная диагностика': [expected_lab_theses1,
                                      expected_lab_theses2,
                                      expected_lab_theses3],
         'Инструментальная диагностика': [expected_instrumental_theses1,
                                          expected_instrumental_theses2],
         'Иные диагностические исследования': [expected_other_theses1]}

    return expected_diagnostic_theses


def make_treatment_theses_for_sort_test():
    expected_treatment_thesis1 = Thesis()
    expected_treatment_thesis1.text = 'Первый тезис в Лечении третьей рекомендации'
    expected_treatment_thesis1.LCR = 'A'
    expected_treatment_thesis1.LRE = '1'
    expected_treatment_thesis2 = Thesis()
    expected_treatment_thesis2.text = 'Второй тезис в Лечении первой рекомендации'
    expected_treatment_thesis2.LCR = 'A'
    expected_treatment_thesis2.LRE = '3'
    expected_treatment_thesis3 = Thesis()
    expected_treatment_thesis3.text = 'Третий тезис в Лечении третьей рекомендации'
    expected_treatment_thesis3.LCR = 'A'
    expected_treatment_thesis3.LRE = '4'
    expected_treatment_thesis4 = Thesis()
    expected_treatment_thesis4.text = 'Первый тезис в Лечении первой рекомендации'
    expected_treatment_thesis4.LCR = 'B'
    expected_treatment_thesis4.LRE = '2'
    expected_treatment_thesis5 = Thesis()
    expected_treatment_thesis5.text = 'Второй тезис в Лечении третьей рекомендации'
    expected_treatment_thesis5.LCR = 'B'
    expected_treatment_thesis5.LRE = '2'
    expected_treatment_thesis6 = Thesis()
    expected_treatment_thesis6.text = 'Второй тезис в Лечении второй рекомендации'
    expected_treatment_thesis6.LCR = 'C'
    expected_treatment_thesis6.LRE = '4'
    expected_treatment_thesis7 = Thesis()
    expected_treatment_thesis7.text = 'Третий тезис в Лечении второй рекомендации'
    expected_treatment_thesis7.LCR = 'C'
    expected_treatment_thesis7.LRE = '4'
    expected_treatment_thesis8 = Thesis()
    expected_treatment_thesis8.text = 'Первый тезис в Лечении второй рекомендации'
    expected_treatment_thesis8.LCR = 'C'
    expected_treatment_thesis8.LRE = '5'
    expected_treatment_theses = [expected_treatment_thesis1, expected_treatment_thesis2, expected_treatment_thesis3,
                                 expected_treatment_thesis4, expected_treatment_thesis5, expected_treatment_thesis6,
                                 expected_treatment_thesis7, expected_treatment_thesis8]

    return expected_treatment_theses


class TestSortDocument(unittest.TestCase):

    # Получение кодов МКБ-10 из пустого списка рекомендаций
    def test_get_mkbs_empty(self):
        expected_mkbs = []
        actual_mkbs = get_mkbs(recommendations_empty)

        self.assertEqual(expected_mkbs, actual_mkbs)

    # Получение кодов МКБ-10 из списка рекомендаций, где только одна рекомендация (соответственно одна нозология)
    # и один код МКБ-10
    def test_get_mkbs_one_nosology_one_mkb(self):
        expected_mkbs = [['H80']]
        actual_mkbs = get_mkbs(recommendations1)

        self.assertEqual(expected_mkbs, actual_mkbs)

    # Получение кодов МКБ-10 из списка рекомендаций, где только одна рекомендация (соответственно одна нозология)
    # и несколько кодов МКБ-10
    def test_get_mkbs_one_nosology_few_mkbs(self):
        expected_mkbs = [['I10', 'I11', 'I12', 'I13']]
        actual_mkbs = get_mkbs(recommendations2)

        self.assertEqual(expected_mkbs, actual_mkbs)

    # Получение кодов МКБ-10 из списка рекомендаций, где несколько рекомендаций (соответственно несколько нозологий)
    # и несколько кодов МКБ-10
    def test_get_mkbs_few_nosology_few_mkbs(self):
        expected_mkbs = [['H80'], ['I10', 'I11', 'I12', 'I13'], ['H25.1', 'H25.2', 'H25.3']]
        actual_mkbs = get_mkbs(recommendations3)

        self.assertEqual(expected_mkbs, actual_mkbs)

    # Получение таблицы критериев из пустого списка рекомендаций
    def test_get_criterias_empty(self):
        expected_criterias = []
        actual_criterias = get_criterias(recommendations_empty)

        self.assertEqual(expected_criterias, actual_criterias)

    # Получение таблицы критериев из списка рекомендаций, где только одна рекомендация (соответственно одна таблица)
    def test_get_criterias_one_criteria(self):
        expected_criterias = ['first criteria']
        actual_criterias = get_criterias(recommendations1)

        self.assertEqual(expected_criterias, actual_criterias)

    # Получение таблицы критериев из списка рекомендаций, где несколько рекомендаций (соответственно несколько таблиц)
    def test_get_criterias_few_criterias(self):
        expected_criterias = ['first criteria', 'second criteria', 'third criteria']
        actual_criterias = get_criterias(recommendations3)

        self.assertEqual(expected_criterias, actual_criterias)

    # Получение названий нозологий из списка рекомендаций, где только одна рекомендация (соответственно одно название)
    def test_get_nosologies_empty(self):
        expected_nosologies = []
        actual_nosologies = get_nosologies(recommendations_empty)

        self.assertEqual(expected_nosologies, actual_nosologies)

    # Получение названий нозологий из списка рекомендаций, где только одна рекомендация (соответственно одно название)
    def test_get_nosologies_one_nosology(self):
        expected_nosologies = ['first nosology']
        actual_nosologies = get_nosologies(recommendations1)

        self.assertEqual(expected_nosologies, actual_nosologies)

    # Получение названий нозологий из списка рекомендаций, где несколько рекомендаций
    # (соответственно несколько названий)
    def test_get_nosologies_few_nosology(self):
        expected_nosologies = ['first nosology', 'second nosology', 'third nosology']
        actual_nosologies = get_nosologies(recommendations3)

        self.assertEqual(expected_nosologies, actual_nosologies)

    # Проверка на пустой строке
    def test_lcr_replace_empty(self):
        expected_lcr = ''
        actual_lcr = lcr_replace('')

        self.assertEqual(expected_lcr, actual_lcr)

    # Замена написанной на кириллице буквы А на ее латинский аналог
    def test_lcr_replace_cyrillic(self):
        expected_lcr = 'A'
        actual_lcr = lcr_replace(diagnostic_thesis1_rec1.LCR)

        self.assertEqual(expected_lcr, actual_lcr)

    # В данном случае замены не происходит, так как буква A изначально написана на латинице
    def test_lcr_replace_latin(self):
        expected_lcr = 'A'
        actual_lcr = lcr_replace(diagnostic_thesis1_rec1.LCR)

        self.assertEqual(expected_lcr, actual_lcr)

    # Проверка на пустой строке
    def test_lre_replace_empty(self):
        expected_lre = ''
        actual_lre = lre_replace('')

        self.assertEqual(expected_lre, actual_lre)

    # Замена римской цифры I на ее арабский аналог - 1
    def test_lre_replace_I(self):
        expected_lre = '1'
        actual_lre = lre_replace(diagnostic_thesis1_rec1.LRE)

        self.assertEqual(expected_lre, actual_lre)

    # Замена римской цифры II на ее арабский аналог - 2
    def test_lre_replace_II(self):
        expected_lre = '2'
        actual_lre = lre_replace(diagnostic_thesis1_rec2.LRE)

        self.assertEqual(expected_lre, actual_lre)

    # Замена римской цифры III на ее арабский аналог - 3
    def test_lre_replace_III(self):
        expected_lre = '3'
        actual_lre = lre_replace(diagnostic_thesis2_rec2.LRE)

        self.assertEqual(expected_lre, actual_lre)

    # Замена римской цифры IV на ее арабский аналог - 4
    def test_lre_replace_IV(self):
        expected_lre = '4'
        actual_lre = lre_replace(diagnostic_thesis4_rec2.LRE)

        self.assertEqual(expected_lre, actual_lre)

    # Замена римской цифры V на ее арабский аналог - 5
    def test_lre_replace_V(self):
        expected_lre = '5'
        actual_lre = lre_replace(diagnostic_thesis3_rec2.LRE)

        self.assertEqual(expected_lre, actual_lre)

    # Объединение трех рекоммендаций в единую и проверка тезисов диагностики
    def test_combine_recommendations_diagnostic_theses(self):

        expected_diagnostic_theses = make_diagnostic_theses_for_combine_test()

        actual_recommendation = combine_recommendations(recommendations3)

        for key in expected_diagnostic_theses:
            i = 0
            for thesis in expected_diagnostic_theses[key]:
                self.assertEqual(1, thesis_compare(thesis, actual_recommendation[0][key][i]))
                i += 1

    # Объединение трех рекоммендаций в единую и проверка тезисов лечения
    def test_combine_recommendations_treatment_theses(self):

        expected_treatment_theses = make_treatment_theses_for_combine_test()

        actual_recommendation = combine_recommendations(recommendations3)

        i = 0
        for thesis in expected_treatment_theses:
            self.assertEqual(1, thesis_compare(thesis, actual_recommendation[1][i]))
            i += 1

    # Сортировка всех тезисов и проверка тезисов диагностики
    def test_sort(self):

        expected_diagnostic_theses = make_diagnostic_theses_for_sort_test()
        expected_treatment_theses = make_treatment_theses_for_sort_test()

        recommendation = combine_recommendations(recommendations3)
        actual_diagnostic_theses = sort_diagnostic_theses(recommendation[0])
        actual_treatment_theses = sort_treatment_theses(recommendation[1])

        for key in expected_diagnostic_theses:
            i = 0
            for thesis in expected_diagnostic_theses[key]:
                self.assertEqual(1, thesis_compare(thesis, actual_diagnostic_theses[key][i]))
                i += 1

        i = 0
        for thesis in expected_treatment_theses:
            self.assertEqual(1, thesis_compare(thesis, actual_treatment_theses[i]))
            i += 1

    # Пустой словарь
    def test_sort_diagnostic_theses_empty(self):

        expected_diagnostic_theses = {}

        diagnostic = {}
        actual_diagnostic_theses = sort_diagnostic_theses(diagnostic)

        for key in expected_diagnostic_theses:
            i = 0
            for thesis in expected_diagnostic_theses[key]:
                self.assertEqual(1, thesis_compare(thesis, actual_diagnostic_theses[key][i]))
                i += 1

    # Сортировка всех тезисов и проверка тезисов лечения
    def test_sort_diagnostic_theses(self):

        expected_diagnostic_theses = make_diagnostic_theses_for_sort_test()

        recommendation = combine_recommendations(recommendations3)
        actual_diagnostic_theses = sort_diagnostic_theses(recommendation[0])

        for key in expected_diagnostic_theses:
            i = 0
            for thesis in expected_diagnostic_theses[key]:
                self.assertEqual(1, thesis_compare(thesis, actual_diagnostic_theses[key][i]))
                i += 1

    # Пустой список
    def test_sort_treatment_theses_empty(self):

        expected_treatment_theses = []

        treatment = []
        actual_treatment_theses = sort_treatment_theses(treatment)

        i = 0
        for thesis in expected_treatment_theses:
            self.assertEqual(1, thesis_compare(thesis, actual_treatment_theses[i]))
            i += 1

    # Сортировка всех тезисов и проверка тезисов лечения
    def test_sort_treatment_theses(self):

        expected_treatment_theses = make_treatment_theses_for_sort_test()

        recommendation = combine_recommendations(recommendations3)
        actual_treatment_theses = sort_treatment_theses(recommendation[1])

        i = 0
        for thesis in expected_treatment_theses:
            self.assertEqual(1, thesis_compare(thesis, actual_treatment_theses[i]))
            i += 1