import os
from fpdf import FPDF
import re

# А - 0, 176, 80
# B - 147, 208, 125
# C - 255, 192, 0

# 1 - 255, 192, 0
# 2 - 125, 212, 23
# 3 - 42, 173, 64
# 4 - 57, 137, 127
# 5 - 68, 84, 106
# 5 (мой вариант) - 100, 117, 140

pdf = FPDF(orientation='P', unit='mm', format='A4')


def create_pdf(recommendation):
    pdf.add_font('times', '', 'times.ttf', uni=True)
    pdf.add_font('timesbd', '', 'timesbd.ttf', uni=True)
    pdf.add_font('timesi', '', 'timesi.ttf', uni=True)

    pdf.add_page()

    pdf.set_font('timesbd', size=22)
    pdf.cell(200, 10, txt='Оглавление', ln=1)
    pdf.set_font('times', size=18)
    pdf.cell(200, 10, txt='• Диагностика', ln=1)
    pdf.cell(200, 10, txt='• Лечение', ln=1)
    pdf.cell(200, 10, txt='• Критерии оценки качества медицинской помощи', ln=1)

    pdf.add_page()

    make_diagnostics(recommendation.diagnosticTheses)
    pdf.cell(200, 10, txt='', ln=1)
    make_treatment(recommendation.treatmentTheses)
    pdf.cell(200, 10, txt='', ln=1)

    pdf.set_font('timesbd', size=22)
    pdf.cell(200, 10, txt='Критерии оценки качества медицинской помощи', ln=1)
    pdf.cell(200, 10, txt='', ln=1)

    pdf.set_font('timesi', size=16)
    pdf.cell(200, 10, txt='при сборе анамнеза:', ln=1)
    make_criteria(recommendation.anamnesisCollectionDefects)
    pdf.set_font('timesi', size=16)
    pdf.cell(200, 10, txt='при обследовании пациентов:', ln=1)
    make_criteria(recommendation.patientExaminationDefects)
    pdf.set_font('timesi', size=16)
    pdf.cell(200, 10, txt='при постановке диагноза:', ln=1)
    make_criteria(recommendation.diagnosisDefects)
    pdf.set_font('timesi', size=16)
    pdf.cell(200, 10, txt='при проведении лечения:', ln=1)
    make_criteria(recommendation.treatmentDefects)
    pdf.set_font('timesi', size=16)
    pdf.cell(200, 10, txt='при обеспечении преемственности:', ln=1)
    make_criteria(recommendation.ensuringContinuityDefects)

    pdf.output('newGuide.pdf')
    os.system('newGuide.pdf')


def make_theses(element):
    pdf.set_font('times', size=16)
    text_theses = '• ' + element.text[1:]
    text_theses = text_theses.replace('й', 'й')
    pdf.multi_cell(0, 6, txt=text_theses)
    pdf.cell(200, 5, txt='', ln=1)

    pdf.set_font('timesbd', size=16)
    text_lcr = element.LCR
    text_lre = element.LRE
    text_full = '(УУР ' + element.LCR + ', УДД ' + element.LRE + ') = '

    pdf.cell(47, 8, txt=text_full)
    if text_lcr == 'A':
        pdf.set_fill_color(0, 176, 80)
    elif text_lcr == 'B':
        pdf.set_fill_color(147, 208, 125)
    else:
        pdf.set_fill_color(255, 192, 0)
    pdf.cell(6, 8, txt=text_lcr, fill=True, align='C')

    if text_lre == '1':
        pdf.set_fill_color(255, 192, 0)
    elif text_lre == '2':
        pdf.set_fill_color(125, 212, 23)
    elif text_lre == '3':
        pdf.set_fill_color(42, 173, 64)
    elif text_lre == '4':
        pdf.set_fill_color(57, 137, 127)
    else:
        pdf.set_fill_color(100, 117, 140)
    pdf.cell(6, 8, txt=text_lre, ln=1, fill=True, align='C')

    pdf.cell(200, 5, txt='', ln=1)


def make_diagnostics(dictionary):
    pdf.set_font('timesbd', size=22)
    pdf.cell(200, 10, txt='1. Диагностика', ln=1)
    pdf.cell(200, 10, txt='', ln=1)

    num = 1
    for key in dictionary.keys():
        if key.find('Физикальное обследование') != -1 or key.find('Лабораторная диагностика') != -1 \
                or key.find('Инструментальная диагностика') != -1 or key.find('Иные диагностические исследования') != -1:
            pdf.set_font('timesbd', size=18)
            buff = key
            buff = re.sub(r'[^\w\s]+|[\d]+', r'', buff).strip()
            title = '1.' + str(num) + ' ' + buff
            pdf.cell(200, 10, txt=title, ln=1)

            pdf.cell(200, 7, txt='', ln=1)
            for element in dictionary[key]:
                make_theses(element)

            pdf.cell(200, 10, txt='', ln=1)
            num += 1


def make_treatment(dictionary):
    pdf.set_font('timesbd', size=22)
    pdf.cell(200, 10, txt='2. Лечение', ln=1)
    pdf.cell(200, 10, txt='', ln=1)

    num = 1
    for key in dictionary.keys():
        if key.find('Медикаментозная терапия') != -1:
            pdf.set_font('timesbd', size=18)
            buff = key
            buff = re.sub(r'[^\w\s]+|[\d]+', r'', buff).strip()
            title = '2.' + str(num) + ' ' + buff
            pdf.cell(200, 10, txt=title, ln=1)

            pdf.cell(200, 7, txt='', ln=1)
            for element in dictionary[key]:
                make_theses(element)

            pdf.cell(200, 10, txt='', ln=1)
            num += 1


def make_criteria(dictionary):
    pdf.set_font('timesi', size=16)
    pdf.cell(200, 7, txt='', ln=1)
    for element in dictionary:
        text_theses = '• ' + element
        text_theses = text_theses.replace('й', 'й')
        pdf.multi_cell(0, 6, txt=text_theses)
        pdf.cell(200, 5, txt='', ln=1)

    pdf.cell(200, 10, txt='', ln=1)
