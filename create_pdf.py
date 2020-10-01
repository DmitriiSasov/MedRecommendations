# -*- coding: utf-8 -*-
import os
from fpdf import FPDF
from pdfrw import PdfReader, PdfWriter
from sort_document import get_criterias, get_mkbs, get_nosologies, sort
import datetime
import pdfkit


# А - 0, 176, 80
# B - 147, 208, 125
# C - 255, 192, 0

# 1 - 255, 192, 0
# 2 - 125, 212, 23
# 3 - 42, 173, 64
# 4 - 57, 137, 127
# 5 - 68, 84, 106
# 5 (мой вариант) - 100, 117, 140


# Создание PDF-файла на основе переданных рекомендаций
# recommendations - список рекомендаций
def make_pdf(recommendations):
    pdf = FPDF(orientation='P', unit='mm', format='A4')

    pdf.add_font('times', '', 'fonts/times.ttf', uni=True)
    pdf.add_font('timesbd', '', 'fonts/timesbd.ttf', uni=True)
    pdf.add_font('timesi', '', 'fonts/timesi.ttf', uni=True)

    pdf.add_page()
    pdf.set_font('timesbd', size=22)
    pdf.cell(200, 40, txt='Клинические рекомендации', ln=1, align='C')
    pdf.set_font('timesbd', size=18)
    pdf.ln(30)

    mkbs = get_mkbs(recommendations)
    nosologies = get_nosologies(recommendations)
    pdf.cell(200, 10, txt='Нозологии:', ln=1)
    pdf.set_font('times', size=18)
    mkb = ''
    for i in range(len(nosologies)):
        for code in mkbs[i]:
            mkb += code + ', '
        mkb = mkb[0:-2]

        pdf.multi_cell(0, 7, txt=nosologies[i] + ' (' + mkb + ')')
        pdf.ln(3)
        mkb = ''

    pdf.add_page()
    pdf.set_font('timesbd', size=22)
    pdf.cell(200, 10, txt='Оглавление', ln=1)
    pdf.set_font('times', size=18)
    pdf.cell(200, 10, txt='• 1 Диагностика', ln=1)
    pdf.cell(200, 10, txt='• 2 Лечение', ln=1)
    pdf.cell(200, 10, txt='• Критерии оценки качества медицинской помощи', ln=1)

    pdf.add_page()

    recommendation = sort(recommendations)

    make_diagnostics(pdf, recommendation[0])
    pdf.ln()
    if pdf.get_y() > 200:
        pdf.add_page()
    make_treatment(pdf, recommendation[1])
    pdf.ln()

    tmp_doc_name = 'document' + str(datetime.datetime.now().hour) + '_' + str(datetime.datetime.now().minute) + '_' \
                   + str(datetime.datetime.now().second) + '.pdf'
    pdf.output(tmp_doc_name)

    document = PdfReader(tmp_doc_name, decompress=False).pages

    criterias = get_criterias(recommendations)
    table = '<head> <meta content="text/html; charset=utf-8" http-equiv="Content-Type"> </head>' \
            '<body> <h1 style="font-size: 28pt; font-family: times; font-weight: bold; margin-bottom: 50pt"> ' \
            'Критерии оценки качества медицинской помощи </h1>'
    for i in range(len(nosologies)):
        table += '<h2 style="font-size: 22pt; font-family: times; font-weight: bold; margin-bottom: 20pt"> ' \
                 + nosologies[i] + '</h2> </body>' + criterias[i]
        table = table.replace('border="0', 'border="1"')

    path_wkhtmltopdf = r'wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    tmp_table_doc_name = 'criteria' + str(datetime.datetime.now().hour) + '_' + str(
        datetime.datetime.now().minute) + '_' + str(datetime.datetime.now().second) + '.pdf'
    pdfkit.from_string(table, tmp_table_doc_name, configuration=config)

    criteria_page = PdfReader(tmp_table_doc_name, decompress=False).pages

    writer = PdfWriter()
    writer.addpages(document)
    writer.addpages(criteria_page)

    doc_name = 'doc_' + str(datetime.datetime.now().hour) + '_' + str(datetime.datetime.now().minute) + '_' \
               + str(datetime.datetime.now().second) + '.pdf'

    writer.write(doc_name)

    os.replace(doc_name, './static/' + doc_name)

    os.remove(tmp_doc_name)
    os.remove(tmp_table_doc_name)

    return doc_name


# Создание тезиса
# pdf - рабочий PDF-файл
# element - один тезис
def make_thesis(pdf, element):
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
    if text_lcr == 'A':
        pdf.set_fill_color(0, 176, 80)
    elif text_lcr == 'B':
        pdf.set_fill_color(147, 208, 125)
    elif text_lcr == 'C':
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
    elif text_lre == '5':
        pdf.set_fill_color(100, 117, 140)
    pdf.cell(6, 8, txt=text_lre, ln=1, fill=True, align='C')

    pdf.ln(5)


# Создание диагностики
# pdf - рабочий PDF-файл
# dictionary - словарь тезисов Диагностики
def make_diagnostics(pdf, dictionary):
    pdf.set_font('timesbd', size=22)
    pdf.cell(200, 10, txt='1 Диагностика', ln=1)
    pdf.ln()

    num = 1
    for key in dictionary.keys():
        pdf.set_font('timesbd', size=18)

        title = '1.' + str(num) + ' ' + key
        pdf.cell(200, 10, txt=title, ln=1)

        pdf.ln(7)
        for element in dictionary[key]:
            make_thesis(pdf, element)

        if len(dictionary.get(key)) == 0:
            pdf.set_font('times', size=16)
            pdf.multi_cell(0, 6, txt='• Отсутствует')
            pdf.ln(5)

        pdf.ln(10)
        num += 1


# Создание лечения
# pdf - рабочий PDF-файл
# tlist - список тезисов Лечения
def make_treatment(pdf, tlist):
    pdf.set_font('timesbd', size=22)
    pdf.cell(200, 10, txt='2 Лечение', ln=1)
    pdf.ln()

    pdf.set_font('timesbd', size=18)
    pdf.cell(200, 10, txt='2.1 Медикаментозная терапия', ln=1)
    pdf.ln(7)

    if len(tlist) > 0:
        for element in tlist:
            make_thesis(pdf, element)
    else:
        pdf.set_font('times', size=16)
        pdf.multi_cell(0, 6, txt='• Отсутствует')
        pdf.ln(5)

    pdf.ln(10)
