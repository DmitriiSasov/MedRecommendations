import os
from fpdf import FPDF

# А - 0, 176, 80
# B - 147, 208, 125
# C - 255, 192, 0

# 1 - 255, 192, 0
# 2 - 125, 212, 23
# 3 - 42, 173, 64
# 4 - 57, 137, 127
# 5 - 68, 84, 106
# 5 (мой вариант) - 100, 117, 140


def create_pdf():
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_font('times', '', 'times.ttf', uni=True)
    pdf.add_font('timesbd', '', 'timesbd.ttf', uni=True)
    pdf.add_font('timesi', '', 'timesi.ttf', uni=True)

    pdf.add_page()

    pdf.set_font('timesbd', size=18)
    pdf.cell(200, 10, txt='Оглавление', ln=1)
    pdf.set_font('times', size=16)
    pdf.cell(200, 10, txt='• Диагностика', ln=1)
    pdf.cell(200, 10, txt='• Лечение', ln=1)
    pdf.cell(200, 10, txt='• Критерии оценки качества медицинской помощи', ln=1)

    pdf.add_page()

    pdf.set_font('timesbd', size=18)
    pdf.cell(200, 10, txt='1. Диагностика', ln=1)
    pdf.cell(200, 5, txt='', ln=1)
    pdf.set_font('timesbd', size=16)
    pdf.cell(200, 10, txt='1.1 Физикальное обследование:', ln=1)
    pdf.set_font('times', size=16)
    pdf.cell(200, 5, txt='', ln=1)
    pdf.multi_cell(0, 5, txt='• Всем пациентам с АГ рекомендуется пальпировать пульс в покое для измерения его '
                             'частоты и ритмичности с целью выявления аритмий [21; 32; 43].')
    pdf.cell(200, 5, txt='', ln=1)

    pdf.set_font('timesbd', size=16)
    pdf.cell(47, 8, txt='(УУР В, УДД 2) = ')
    pdf.set_fill_color(147, 208, 125)
    pdf.cell(6, 8, txt='В', fill=True, align='C')
    pdf.set_fill_color(125, 212, 23)
    pdf.cell(6, 8, txt='2', ln=1, fill=True, align='C')
    pdf.cell(200, 5, txt='', ln=1)

    pdf.set_font('times', size=16)
    pdf.multi_cell(0, 5, txt='• Всем пациентам с АГ рекомендуется определение антропометрических данных для выявления '
                             'избыточной массы тела/ожирения, оценка неврологического статуса и когнитивной функции, '
                             'исследование глазного дна для выявления гипертонической ретинопатии, пальпация и '
                             'аускультация сердца и сонных артерий, пальпация и аускультация периферических артерий '
                             'для выявления патологических шумов, сравнение АД между руками хотя бы однократно [21].')
    pdf.cell(200, 5, txt='', ln=1)

    pdf.set_font('timesbd', size=16)
    pdf.cell(47, 8, txt='(УУР С, УДД 5) = ')
    pdf.set_fill_color(255, 192, 0)
    pdf.cell(6, 8, txt='C', fill=True, align='C')
    pdf.set_fill_color(100, 117, 140)
    pdf.cell(6, 8, txt='5', ln=1, fill=True, align='C')

    pdf.output('newGuide.pdf')
    os.system('newGuide.pdf')


create_pdf()
