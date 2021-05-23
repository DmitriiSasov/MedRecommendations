# -*- coding: utf-8 -*-
import os
from fpdf import FPDF
from pdfrw import PdfReader, PdfWriter
import datetime
import pdfkit
from db import get_recommendation_from_db
from operator import attrgetter
import re


class DocGenerator:

    # Создание раздела содержания в документе
    # pdf - текущее состояние документа
    def make_table_of_content(self, pdf):
        pdf.add_page()
        pdf.set_font('timesbd', size=22)
        pdf.cell(200, 10, txt='Оглавление', ln=1)
        pdf.set_font('times', size=18)
        pdf.cell(200, 10, txt='• 1 Диагностика', ln=1)
        pdf.cell(200, 10, txt='• 2 Лечение', ln=1)
        pdf.cell(200, 10, txt='• Критерии оценки качества медицинской помощи', ln=1)

    # Создание PDF-файла на основе переданных рекомендаций
    # recommendations - список рекомендаций
    def make_pdf(self, mkbs):

        not_exist = False
        for mkb in mkbs:
            rec = get_recommendation_from_db(mkb)
            if rec is False:
                not_exist = True

        if not_exist:
            return False

        recommendations = []
        for mkb in mkbs:
            recommendation = get_recommendation_from_db(mkb)
            recommendations.append(recommendation)

        pdf = FPDF(orientation='P', unit='mm', format='A4')

        pdf.add_font('times', '', 'fonts/times.ttf', uni=True)
        pdf.add_font('timesbd', '', 'fonts/timesbd.ttf', uni=True)
        pdf.add_font('timesi', '', 'fonts/timesi.ttf', uni=True)

        pdf.add_page()
        pdf.set_font('timesbd', size=22)
        pdf.cell(200, 40, txt='Клинические рекомендации', ln=1, align='C')
        pdf.set_font('timesbd', size=18)
        pdf.ln(30)

        mkbs = self.get_mkbs(recommendations)
        nosologies = self.get_nosologies(recommendations)
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

        self.make_table_of_content(pdf)

        pdf.add_page()

        recommendation = self.sort(recommendations)

        self.make_diagnostics(pdf, recommendation[0])
        pdf.ln()
        if pdf.get_y() > 200:
            pdf.add_page()
        self.make_treatment(pdf, recommendation[1])
        pdf.ln()

        tmp_doc_name = 'document' + str(datetime.datetime.now().hour) + '_' + str(datetime.datetime.now().minute) + '_' \
                       + str(datetime.datetime.now().second) + '.pdf'
        pdf.output(tmp_doc_name)

        document = PdfReader(tmp_doc_name, decompress=False).pages

        criterias = self.get_criterias(recommendations)
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
    @staticmethod
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
    def make_diagnostics(self, pdf, dictionary):
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
                self.make_thesis(pdf, element)

            if len(dictionary.get(key)) == 0:
                pdf.set_font('times', size=16)
                pdf.multi_cell(0, 6, txt='• Отсутствует')
                pdf.ln(5)

            pdf.ln(10)
            num += 1

    # Создание лечения
    # pdf - рабочий PDF-файл
    # tlist - список тезисов Лечения
    def make_treatment(self, pdf, tlist):
        pdf.set_font('timesbd', size=22)
        pdf.cell(200, 10, txt='2 Лечение', ln=1)
        pdf.ln()

        pdf.set_font('timesbd', size=18)
        pdf.cell(200, 10, txt='2.1 Медикаментозная терапия', ln=1)
        pdf.ln(7)

        if len(tlist) > 0:
            for element in tlist:
                self.make_thesis(pdf, element)
        else:
            pdf.set_font('times', size=16)
            pdf.multi_cell(0, 6, txt='• Отсутствует')
            pdf.ln(5)

        pdf.ln(10)

    # Получить список кодов МКБ-10 из списка рекомендаций
    # recommenations - список рекомендаций
    # return - список кодов МКБ-10
    def get_mkbs(self, recommendations):
        mkbs = []
        for rec in recommendations:
            mkbs.append(rec.MKBs)

        return mkbs

    # Получить список названий нозологий из списка рекомендаций
    # recommendations - список рекомендаций
    # return - список названий нозологий
    def get_nosologies(self, recommendations):
        nosologies = []
        for rec in recommendations:
            nosologies.append(rec.nozology_name)

        return nosologies

    # Получить список критериев из списка рекомендаций
    # recommendations - список рекомендаций
    # return - список HTML-таблиц критериев
    def get_criterias(self, recommendations):
        criterias = []
        for rec in recommendations:
            criterias.append(rec.table_tag)

        return criterias

    # Объединение списка рекомендаций в единую рекомендацию
    # recommendations - список рекомендаций
    # return - рекомендация (список из словаря тезисов Диагностики и списка тезисов Лечения)
    def combine_recommendations(self, recommendations):
        diagnostic_theses = {'Физикальное обследование': [], 'Лабораторная диагностика': [],
                             'Инструментальная диагностика': [], 'Иные диагностические исследования': []}
        diag_thes = {}
        treatment_theses = []

        for rec in recommendations:
            for key in rec.diagnosticTheses:
                buff = key
                buff = re.sub(r'[^\w\s]+|[\d]+', r'', buff).strip()
                if buff == 'Физикальное обследование' or buff == 'Лабораторная диагностика' \
                        or buff == 'Инструментальная диагностика' or buff == 'Иные диагностические исследования' \
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
    def sort(self, recommendations):
        recommendation = self.combine_recommendations(recommendations)

        recommendation[0] = self.sort_diagnostic_theses(recommendation[0])

        recommendation[1] = self.sort_treatment_theses(recommendation[1])

        return recommendation

    # Сортировка тезисов Диагностики в рекомендации
    # diagnostic - словарь тезисов Диагностики
    # return - отсортированный словарь тезисов Диагностики
    def sort_diagnostic_theses(self, diagnostic):
        for key in diagnostic:
            for element in diagnostic[key]:
                element.LCR = self.lcr_replace(str(element.LCR))
                element.LRE = self.lre_replace(str(element.LRE))
            diagnostic.get(key).sort(key=attrgetter('LCR', 'LRE'))

        return diagnostic

    # Сортировка тезисов Лечения в рекомендации
    # diagnostic - список тезисов Диагностики
    # return - отсортированный список тезисов Диагностики
    def sort_treatment_theses(self, treatment):
        for element in treatment:
            element.LCR = self.lcr_replace(str(element.LCR))
            element.LRE = self.lre_replace(str(element.LRE))

        treatment.sort(key=attrgetter('LCR', 'LRE'))

        return treatment

    # Замена букв, написанных на кириллице, на латинские аналоги
    # lcr - символ УУР (кириллица или латиница)
    # return - символ УУР на латинице
    def lcr_replace(self, lcr):
        lcr = lcr.replace('А', 'A')
        lcr = lcr.replace('В', 'B')
        lcr = lcr.replace('С', 'C')

        return lcr

    # Замена римских цифр на арабские аналоги
    # lre - символ УДД (римская или арабская цифра)
    # return - символ УУР в виде арабской цифры
    def lre_replace(self, lre):
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