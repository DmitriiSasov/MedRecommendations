# -*- coding: utf-8 -*-

import pymysql
from data_structures import Recommendation, Thesis
import dateutil.parser

DB_HOST = 'localhost'
DB_NAME = 'clin_rec_db'
DB_USER = 'root'
DB_PASS = 'SlenderHospice123'


def is_rec_not_exist(cur, nozology_name, date):
    cur.execute("SELECT `id` FROM `recommendation` WHERE `name`=%s AND `creation_date`=%s", (nozology_name, date))

    row = cur.fetchone()

    if row is None:
        return True

    return False


def insert_recommendation_into_db(recommendation):
    con = pymysql.connect(host=DB_HOST, user=DB_USER,
                          password=DB_PASS, database=DB_NAME, autocommit=True)

    with con:
        cur = con.cursor()

        if is_rec_not_exist(cur, recommendation.nozology_name, recommendation.creation_date):
            insert_rec_info_into_db(cur, recommendation.nozology_name, recommendation.table_tag,
                                    recommendation.creation_date)

            cur.execute("SELECT LAST_INSERT_ID()")

            row = cur.fetchone()
            rec_id = "{0}".format(row[0])

            insert_mkbs_into_db(cur, recommendation.MKBs, rec_id)

            insert_diagnostic_into_db(cur, recommendation.diagnosticTheses, rec_id)

            insert_treatment_into_db(cur, recommendation.treatmentTheses, rec_id)


def insert_rec_info_into_db(cur, name, table, creation_date):
    sql = "INSERT INTO `recommendation` (`name`, `table`, `creation_date`) VALUES (%s, %s, %s)"
    cur.execute(sql, (name, table, creation_date))


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

        if recommendation_id is False:
            return False

        recommendation.MKBs = get_mkbs_by_recommendation_id(cur, recommendation_id)
        recommendation.nozology_name = get_nozology_name_by_recommendation_id(cur, recommendation_id)
        recommendation.table_tag = get_table_tag_by_recommendation_id(cur, recommendation_id)
        recommendation.diagnosticTheses = get_diagnostic_theses_by_recommendation_id(cur, recommendation_id)
        recommendation.treatmentTheses = get_treatment_theses_by_recommendation_id(cur, recommendation_id)

    return recommendation


def get_creation_date_by_rec_id(cur, recommendation_id):
    cur.execute("SELECT `creation_date` FROM `recommendation` WHERE `id`=%s", recommendation_id)

    row = cur.fetchone()

    creation_date = "{0}".format(row[0])

    return creation_date


def get_recommendation_id_by_mkb(cur, mkb):
    cur.execute("SELECT `recommendation_id` FROM `mkb10` WHERE `name`=%s", mkb)

    row = cur.fetchall()

    recommendation_id = 0

    if len(row) > 1:
        dates = []
        for el in row:
            date = dateutil.parser.parse(get_creation_date_by_rec_id(cur, "{0}".format(el[0])))
            dates.append(date)
        last_rec_date = greater_date(dates)
        recommendation_id = get_recommendation_id_by_creation_date(cur, last_rec_date)
    elif len(row) == 0:
        return False
    else:
        for el in row:
            recommendation_id = "{0}".format(el[0])

    return recommendation_id


def get_recommendation_id_by_creation_date(cur, date):

    cur.execute("SELECT `id` FROM `recommendation` WHERE `creation_date`=%s", date)

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
            thesis = Thesis("{0}".format(elem[1]), "{0}".format(elem[2]), "{0}".format(elem[3]))

            diagnostic[diagnostic_name] += [thesis]

    return diagnostic


def get_treatment_theses_by_recommendation_id(cur, recommendation_id):
    cur.execute("SELECT * FROM `treatment_thesis` WHERE `recommendation_id`=%s", int(recommendation_id))

    rows = cur.fetchall()

    treatment_theses = []
    for row in rows:
        thesis = Thesis("{0}".format(row[1]), "{0}".format(row[2]), "{0}".format(row[3]))
        treatment_theses.append(thesis)

    return treatment_theses


def greater_date(dates):
    dates.sort()

    return dates[-1]
