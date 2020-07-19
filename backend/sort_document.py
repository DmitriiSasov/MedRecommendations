from operator import attrgetter, itemgetter
import re


# Получить список кодов МКБ-10 из списка рекомендаций
# recommenations - список рекомендаций
# return - список кодов МКБ-10
def get_mkbs(recommendations):
    mkbs = []
    for rec in recommendations:
        mkbs.append(rec.MKBs)

    return mkbs


# Получить список названий нозологий из списка рекомендаций
# recommendations - список рекомендаций
# return - список названий нозологий
def get_nosologies(recommendations):
    nosologies = []
    for rec in recommendations:
        nosologies.append(rec.nozology_name)

    return nosologies


# Получить список критериев из списка рекомендаций
# recommendations - список рекомендаций
# return - список HTML-таблиц критериев
def get_criterias(recommendations):
    criterias = []
    for rec in recommendations:
        criterias.append(rec.table_tag)

    return criterias


# Объединение списка рекомендаций в единую рекомендацию
# recommendations - список рекомендаций
# return - рекомендация (список из словаря тезисов Диагностики и списка тезисов Лечения)
def combine_recommendations(recommendations):
    diagnostic_theses = {'Физикальное обследование': [], 'Лабораторная диагностика': [],
                         'Инструментальная диагностика': [], 'Иные диагностические исследования': []}
    diag_thes = {}
    treatment_theses = []

    for rec in recommendations:
        for key in rec.diagnosticTheses:
            buff = key
            buff = re.sub(r'[^\w\s]+|[\d]+', r'', buff).strip()
            if buff == 'Физикальное обследование' or buff == 'Лабораторная диагностика' \
                    or buff == 'Инструментальная диагностика' or buff == 'Иные диагностические исследования'\
                    or buff == 'Лабораторные диагностические исследования' \
                    or buff == 'Инструментальные диагностические исследования':
                if buff == 'Лабораторные диагностические исследования':
                    diag_thes['Лабораторная диагностика'] = rec.diagnosticTheses[key]
                elif buff == 'Инструментальные диагностические исследования':
                    diag_thes['Инструментальная диагностика'] = rec.diagnosticTheses[key]
                else:
                    diag_thes[buff] = rec.diagnosticTheses[key]

        buff_dict = diag_thes.copy()
        for key, value in buff_dict.items():
            if key in diagnostic_theses:
                diagnostic_theses[key] = diagnostic_theses.get(key, 0) + value
            else:
                diagnostic_theses[key] = buff_dict.get(key, 0)
        diag_thes.clear()
        treatment_theses += rec.treatmentTheses

    recommendation = [diagnostic_theses, treatment_theses]

    return recommendation


# Сортировка всех тезисов в рекомендации
# recommendations - список рекомендаций
# return - рекомендация (список из словаря тезисов Диагностики и списка тезисов Лечения)
def sort(recommendations):

    recommendation = combine_recommendations(recommendations)

    recommendation[0] = sort_diagnostic_theses(recommendation[0])

    recommendation[1] = sort_treatment_theses(recommendation[1])

    return recommendation


# Сортировка тезисов Диагностики в рекомендации
# diagnostic - словарь тезисов Диагностики
# return - отсортированный словарь тезисов Диагностики
def sort_diagnostic_theses(diagnostic):
    for key in diagnostic:
        for element in diagnostic[key]:
            element.LCR = lcr_replace(str(element.LCR))
            element.LRE = lre_replace(str(element.LRE))
        diagnostic.get(key).sort(key=attrgetter('LCR', 'LRE'))

    return diagnostic


# Сортировка тезисов Лечения в рекомендации
# diagnostic - список тезисов Диагностики
# return - отсортированный список тезисов Диагностики
def sort_treatment_theses(treatment):
    treatment.sort(key=attrgetter('LCR', 'LRE'))

    return treatment


# Замена букв, написанных на кириллице, на латинские аналоги
# lcr - символ УУР (кириллица или латиница)
# return - символ УУР на латинице
def lcr_replace(lcr):
    lcr = lcr.replace('А', 'A')
    lcr = lcr.replace('В', 'B')
    lcr = lcr.replace('С', 'C')

    return lcr


# Замена римских цифр на арабские аналоги
# lre - символ УДД (римская или арабская цифра)
# return - символ УУР в виде арабской цифры
def lre_replace(lre):
    if lre == 'I':
        lre = lre.replace('I', '1')
    elif lre == 'II':
        lre = lre.replace('II', '2')
    elif lre == 'III':
        lre = lre.replace('III', '3')
    elif lre == 'IV':
        lre = lre.replace('IV', '4')
    elif lre == 'V':
        lre = lre.replace('V', '5')

    return lre
