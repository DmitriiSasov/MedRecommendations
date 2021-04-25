# -*- coding: utf-8 -*-

import pymysql
from data_structures import Recommendation, Thesis
from create_pdf import make_pdf

DB_HOST = 'localhost'
DB_NAME = 'mydb'
DB_USER = 'root'
DB_PASS = 'SlenderHospice123'


def insert_recommendation_into_db(recommendation):

    con = pymysql.connect(host=DB_HOST, user=DB_USER,
                          password=DB_PASS, database=DB_NAME, autocommit=True)

    with con:
        cur = con.cursor()

        insert_rec_info_into_db(cur, recommendation.nozology_name, recommendation.table_tag)

        cur.execute("SELECT LAST_INSERT_ID()")

        row = cur.fetchone()
        rec_id = "{0}".format(row[0])

        insert_mkbs_into_db(cur, recommendation.MKBs, rec_id)

        insert_diagnostic_into_db(cur, recommendation.diagnosticTheses, rec_id)

        insert_treatment_into_db(cur, recommendation.treatmentTheses, rec_id)


def insert_rec_info_into_db(cur, name, table):

    sql = "INSERT INTO `recommendation` (`name`, `table`) VALUES (%s, %s)"
    cur.execute(sql, (name, table))


def insert_mkbs_into_db(cur, mkbs, rec_id):

    sql = "INSERT INTO `mkb10` (`name`, `recommendation_id`) VALUES (%s, %s)"

    for mkb in mkbs:
        cur.execute(sql, (mkb, rec_id))


def insert_diagnostic_into_db(cur, diagnostics, rec_id):

    sql1 = "INSERT INTO `diagnostic` (`name`, `recommendation_id`) VALUES (%s, %s)"

    sql2 = "INSERT INTO `diagnostic_thesis` (`text`, `LCR`, `LRE`, `diagnostic_id`) VALUES(%s, %s, %s, %s)"

    for name in diagnostics.keys():
        cur.execute(sql1, (name, rec_id))

        cur.execute("SELECT LAST_INSERT_ID()")

        row = cur.fetchone()
        diag_id = "{0}".format(row[0])

        for thesis in diagnostics[name]:
            cur.execute(sql2, (thesis.text, thesis.LCR, thesis.LRE, diag_id))


def insert_treatment_into_db(cur, treatments, rec_id):

    sql = "INSERT INTO `treatment_thesis` (`text`, `LCR`, `LRE`, `recommendation_id`) VALUES(%s, %s, %s, %s)"

    for treatment in treatments:
        cur.execute(sql, (treatment.text, treatment.LCR, treatment.LRE, rec_id))


def get_recommendation_from_db(mkb):

    recommendation = Recommendation()

    con = pymysql.connect(host=DB_HOST, user=DB_USER,
                          password=DB_PASS, database=DB_NAME)

    with con:
        cur = con.cursor()

        recommendation_id = get_recommendation_id_by_mkb(cur, mkb)
        recommendation.MKBs = get_mkbs_by_recommendation_id(cur, recommendation_id)
        recommendation.nozology_name = get_nozology_name_by_recommendation_id(cur, recommendation_id)
        recommendation.table_tag = get_table_tag_by_recommendation_id(cur, recommendation_id)
        recommendation.diagnosticTheses = get_diagnostic_theses_by_recommendation_id(cur, recommendation_id)
        recommendation.treatmentTheses = get_treatment_theses_by_recommendation_id(cur, recommendation_id)

    return recommendation


def get_recommendation_id_by_mkb(cur, mkb):

    cur.execute("SELECT `recommendation_id` FROM `mkb10` WHERE `name`=%s LIMIT 1", mkb)

    row = cur.fetchone()

    recommendation_id = "{0}".format(row[0])

    return recommendation_id


def get_mkbs_by_recommendation_id(cur, recommendation_id):

    cur.execute("SELECT `name` FROM `mkb10` WHERE `recommendation_id`=%s", int(recommendation_id))

    rows = cur.fetchall()

    mkbs = []

    for row in rows:
        mkbs.append("{0}".format(row[0]))

    return mkbs


def get_nozology_name_by_recommendation_id(cur, recommendation_id):

    cur.execute("SELECT `name` FROM `recommendation` WHERE `id`=%s LIMIT 1", int(recommendation_id))

    row = cur.fetchone()

    nozology_name = "{0}".format(row[0])

    return nozology_name


def get_table_tag_by_recommendation_id(cur, recommendation_id):

    cur.execute("SELECT `table` FROM `recommendation` WHERE `id`=%s LIMIT 1", int(recommendation_id))

    row = cur.fetchone()

    table_tag = "{0}".format(row[0])

    return table_tag


def get_diagnostic_theses_by_recommendation_id(cur, recommendation_id):

    cur.execute("SELECT * FROM `diagnostic` WHERE `recommendation_id`=%s", int(recommendation_id))

    rows = cur.fetchall()

    diagnostic = {}
    for row in rows:
        diagnostic_id = "{0}".format(row[0])
        diagnostic_name = "{0}".format(row[1])

        cur.execute("SELECT * FROM `diagnostic_thesis` WHERE `diagnostic_id`=%s", int(diagnostic_id))

        theses = cur.fetchall()

        diagnostic[diagnostic_name] = []
        for elem in theses:
            thesis = Thesis()

            thesis.text = "{0}".format(elem[1])
            thesis.LCR = "{0}".format(elem[2])
            thesis.LRE = "{0}".format(elem[3])
            diagnostic[diagnostic_name] += [thesis]

    return diagnostic


def get_treatment_theses_by_recommendation_id(cur, recommendation_id):

    cur.execute("SELECT * FROM `treatment_thesis` WHERE `recommendation_id`=%s", int(recommendation_id))

    rows = cur.fetchall()

    treatment_theses = []
    thesis = Thesis()
    for row in rows:
        thesis.text = "{0}".format(row[1])
        thesis.LCR = "{0}".format(row[2])
        thesis.LRE = "{0}".format(row[3])
        treatment_theses.append(thesis)

    return treatment_theses


test1 = [get_recommendation_from_db("i10")]

make_pdf(test1)

rec = Recommendation()

rec.nozology_name = "Болезнь"
rec.MKBs = ['D10', 'D11']
rec.table_tag = '<table border="0" width="100%" cellspacing="0" cellpadding="0">\
<tbody>\
<tr>\
<td valign="top" width="8%">\
<p><strong>№</strong></p>\
</td>\
<td valign="top" width="58%">\
<p><strong>Критерий качества</strong></p>\
</td>\
<td valign="top" width="21%">\
<p align="center"><strong>E</strong><strong>ОК</strong></p>\
<p align="center"><strong>Класс и уровень</strong></p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/</strong></p>\
<p align="center"><strong>нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>1</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>Установлен диагноз АГ согласно рекомендациям. Зафиксировано повышение офисного (клинического) АД выше 140 и/или 90 мм рт. ст. на повторных визитах, либо на основании СМАД<em> (</em>среднее за 24 часа ≥130 мм и/или ≥80 мм рт. ст.)</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">IA</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>2</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>Выполнен общий анализ крови</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">-</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>3</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>Выполнен биохимический анализ крови (креатинин, расчетная скорость клубочковой фильтрации, глюкоза, калий, натрий, мочевая кислота, ОХ, ЛПНП, ТГ, ЛПВП)</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">IB</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>4</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>Выполнен общий анализ мочи</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">IВ</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>5</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>Выполнена качественная оценка протеинурии тест-полоской или количественное определение альбуминурии</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">IВ</p>\
<p align="center">&nbsp;</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>6</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>Выполнена ЭКГ в 12 отведениях</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">IВ</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>7</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>Даны рекомендации по модификации образа жизни (ограничение потребления натрия, увеличение физической активности, снижение избыточной массы тела, отказ от курения, ограничение потребления алкоголя)</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">IA</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>8</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>Поставлен клинический диагноз с указанием стадии заболевания, степени повышения АД (при отсутствии терапии), категории риска, наличия ПОМ и АКС</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">-</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>9</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>У пациентов с АГ 1-й степени, относящимся к категориям низкого/среднего риска, начата антигипертензивная лекарственная терапия одним из препаратов рекомендованных классов после 3-го месяца модификации образа жизни</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">IA</p>\
<p align="center">&nbsp;</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>10</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>Лицам с АГ второй степени и выше назначена комбинированная двухкомпонентная антигипертензивная терапия сразу после постановки диагноза и проведена ее интенсификация для достижения целевого АД.</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">IA</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>11</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>Достигнут целевой уровень&nbsp; САД&lt;140 мм рт. ст. и ДАД &lt; 90 мм рт. ст. через 3 месяца от начала лечения. При недостижении целевого АД приведено объяснение необходимости индивидуального уровня АД и скорости его снижения (плохая переносимость, побочные эффекты лекарственной терапии, низкая приверженность пациента к лечению, включая невыполнения рекомендаций врача, необходимость ревизии поставленного диагноза для исключения симптоматической АГ, наличие сопутствующей патологии или лекарственной терапии, затрудняющей контроль АД)</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">IA</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
<tr>\
<td valign="top" width="8%">\
<p><strong>12</strong></p>\
</td>\
<td valign="top" width="58%">\
<p>Пациент взят под диспансерное наблюдение</p>\
</td>\
<td valign="top" width="21%">\
<p align="center">-</p>\
</td>\
<td valign="top" width="10%">\
<p align="center"><strong>Да/нет</strong></p>\
</td>\
</tr>\
</tbody>\
</table>'

diag_thesis1 = Thesis()
diag_thesis1.text = "Текст тезиса для Диагностика 1"
diag_thesis1.LCR = "A"
diag_thesis1.LRE = "5"

diag_thesis2 = Thesis()
diag_thesis2.text = "Текст тезиса для Диагностика 2"
diag_thesis2.LCR = "B"
diag_thesis2.LRE = "4"

diags = {
    "Диагностика 1": [diag_thesis1],
    "Диагностика 2": [diag_thesis2]
}

rec.diagnosticTheses = diags

treat1 = Thesis()
treat1.text = "Текст для 1 тезиса Лечение"
treat1.LCR = "A"
treat1.LRE = "1"

treat2 = Thesis()
treat2.text = "Текст для 2 тезиса Лечение"
treat2.LCR = "B"
treat2.LRE = "2"

treat3 = Thesis()
treat3.text = "Текст для 3 тезиса Лечение"
treat3.LCR = "C"
treat3.LRE = "5"

treat4 = Thesis()
treat4.text = "Текст для 4 тезиса Лечение"
treat4.LCR = "A"
treat4.LRE = "3"

treats = [
    treat1,
    treat2,
    treat3,
    treat4
]

rec.treatmentTheses = treats

insert_recommendation_into_db(rec)
