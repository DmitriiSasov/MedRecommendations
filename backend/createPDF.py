# -*- coding: utf-8 -*-
import os
from fpdf import FPDF
from pdfrw import PdfReader, PdfWriter
import datetime
import pdfkit
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
    pdf.cell(200, 40, txt='Клинические рекомендации', ln=1, align='C')
    pdf.set_font('timesbd', size=18)
    pdf.ln(30)
    nozology = recommendation.nozology_name
    mkbs = ''
    for code in recommendation.MKBs:
        mkbs += code + ', '
    mkbs = mkbs[0:-2]
    pdf.cell(200, 10, txt='Нозологии:', ln=1)
    pdf.set_font('times', size=18)
    pdf.cell(200, 10, txt=nozology + ' (' + mkbs + ')')

    pdf.add_page()
    pdf.set_font('timesbd', size=22)
    pdf.cell(200, 10, txt='Оглавление', ln=1)
    pdf.set_font('times', size=18)
    pdf.cell(200, 10, txt='• Диагностика', ln=1)
    pdf.cell(200, 10, txt='• Лечение', ln=1)
    pdf.cell(200, 10, txt='• Критерии оценки качества медицинской помощи', ln=1)

    pdf.add_page()

    make_diagnostics(recommendation.diagnosticTheses)
    pdf.ln()
    make_treatment(recommendation.treatmentTheses)
    pdf.ln()

    pdf.output('document.pdf')

    document = PdfReader('document.pdf', decompress=False).pages

    table = '<head> <meta content="text/html; charset=utf-8" http-equiv="Content-Type"> </head>' \
            '<body> <h1 style="font-size: 28pt; font-family: times; font-weight: bold; margin-bottom: 50pt"> ' \
            'Критерии оценки качества ' \
            'медицинской помощи </h1> </body>' \
            + recommendation.table_tag
    table = table.replace('border="0', 'border="1"')

    path_wkhtmltopdf = r'wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdfkit.from_string(table, 'criteria.pdf', configuration=config)

    criteria_page = PdfReader('criteria.pdf', decompress=False).pages

    writer = PdfWriter()
    writer.addpages(document)
    writer.addpages(criteria_page)

    doc_name = 'doc_'+str(datetime.date.today())+'_'+str(datetime.time.hour)+'-'+str(datetime.time.minute)+'.pdf'

    writer.write(doc_name)

    os.system(doc_name)


def make_thesis(element):
    pdf.set_font('times', size=16)
    text_thesis = '• ' + element.text[1:]
    text_thesis = text_thesis.replace('й', 'й')
    pdf.multi_cell(0, 6, txt=text_thesis)
    pdf.ln(5)

    pdf.set_font('timesbd', size=16)
    text_lcr = element.LCR
    text_lre = element.LRE
    text_full = '(УУР ' + element.LCR + ', УДД ' + element.LRE + ') = '

    pdf.cell(47, 8, txt=text_full)
    if text_lcr == 'A' or text_lcr == 'А':
        pdf.set_fill_color(0, 176, 80)
    elif text_lcr == 'B' or text_lcr == 'В':
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

    pdf.ln(5)


def make_diagnostics(dictionary):
    pdf.set_font('timesbd', size=22)
    pdf.cell(200, 10, txt='1. Диагностика', ln=1)
    pdf.ln()

    num = 1
    for key in dictionary.keys():
        if key.find('Физикальное обследование') != -1 or key.find('Лабораторная диагностика') != -1 \
                or key.find('Инструментальная диагностика') != -1 or key.find(
            'Иные диагностические исследования') != -1:
            pdf.set_font('timesbd', size=18)
            buff = key
            buff = re.sub(r'[^\w\s]+|[\d]+', r'', buff).strip()
            title = '1.' + str(num) + ' ' + buff
            pdf.cell(200, 10, txt=title, ln=1)

            pdf.ln(7)
            for element in dictionary[key]:
                make_thesis(element)

            if len(dictionary.get(key)) == 0:
                pdf.set_font('times', size=16)
                pdf.multi_cell(0, 6, txt='• Не рекомендуется')
                pdf.ln(5)

            pdf.ln(10)
            num += 1


def make_treatment(dictionary):
    pdf.set_font('timesbd', size=22)
    pdf.cell(200, 10, txt='2. Лечение', ln=1)
    pdf.ln()

    pdf.set_font('timesbd', size=18)
    pdf.cell(200, 10, txt='2.1 Медикаментозная терапия', ln=1)
    pdf.ln(7)

    if len(dictionary) > 0:
        for element in dictionary:
            make_thesis(element)
    else:
        pdf.set_font('times', size=16)
        pdf.multi_cell(0, 6, txt='• Отсутствует')
        pdf.ln(5)

    pdf.ln(10)
