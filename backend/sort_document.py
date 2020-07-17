from operator import attrgetter, itemgetter
import re


def get_mkbs(recommendations):
    mkbs = []
    for rec in recommendations:
        mkbs.append(rec.MKBs)

    return mkbs


def get_nosologies(recommendations):
    nosologies = []
    for rec in recommendations:
        nosologies.append(rec.nozology_name)

    return nosologies


def get_criterias(recommendations):
    criterias = []
    for rec in recommendations:
        criterias.append(rec.table_tag)

    return criterias


def sort(recommendations):
    diagnostic_theses = {'Физикальное обследование': [], 'Лабораторная диагностика': [],
                         'Инструментальная диагностика': [], 'Иные диагностические исследования': []}
    diag_thes = {}
    treatment_theses = []
    recommendation = []
    buff_dict = {}

    for rec in recommendations:
        for key in rec.diagnosticTheses:
            buff = key
            buff = re.sub(r'[^\w\s]+|[\d]+', r'', buff).strip()
            if buff == 'Физикальное обследование' or buff == 'Лабораторная диагностика' \
                    or buff == 'Инструментальная диагностика' or buff == 'Иные диагностические исследования':
                diag_thes[buff] = rec.diagnosticTheses[key]

        buff_dict = diag_thes.copy()
        for key, value in buff_dict.items():
            if key in diagnostic_theses:
                diagnostic_theses[key] = diagnostic_theses.get(key, 0) + value
            else:
                diagnostic_theses[key] = buff_dict.get(key, 0)
        diag_thes.clear()
        treatment_theses += rec.treatmentTheses

        for key in diagnostic_theses:
            for element in diagnostic_theses[key]:
                element.LCR = lcr_replace(str(element.LCR))
                element.LRE = lre_replace(str(element.LRE))
            diagnostic_theses.get(key).sort(key=attrgetter('LCR', 'LRE'))

        treatment_theses.sort(key=attrgetter('LCR', 'LRE'))

        recommendation = [diagnostic_theses, treatment_theses]

    return recommendation


def lcr_replace(lcr):
    lcr = lcr.replace('А', 'A')
    lcr = lcr.replace('В', 'B')
    lcr = lcr.replace('С', 'C')

    return lcr


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