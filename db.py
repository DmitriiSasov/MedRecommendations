# -*- coding: utf-8 -*-

import pymysql
from data_structures import Recommendation, Thesis

DB_HOST = 'localhost'
DB_NAME = 'mydb'
DB_USER = 'root'
DB_PASS = 'SlenderHospice123'


def get_recommendation_from_db(mkb):

    recommendation = Recommendation()
    thesis = Thesis()

    con = pymysql.connect(host=DB_HOST, user=DB_USER,
                          password=DB_PASS, database=DB_NAME)

    with con:
        cur = con.cursor()

        recommendation_id = get_recommendation_id_by_mkb(cur, mkb)
        recommendation.MKBs = get_mkbs_by_recommendation_id(cur, recommendation_id)
        recommendation.nozology_name = get_nozology_name_by_recommendation_id(cur, recommendation_id)
        recommendation.table_tag = get_table_tag_by_recommendation_id(cur, recommendation_id)

    return recommendation


def get_recommendation_id_by_mkb(cur, mkb):

    cur.execute("SELECT recommendation_id FROM mkb10 WHERE name=%s LIMIT 1", mkb)

    row = cur.fetchone()

    recommendation_id = "{0}".format(row[0])

    return recommendation_id


def get_mkbs_by_recommendation_id(cur, recommendation_id):

    cur.execute("SELECT `name` FROM mkb10 WHERE recommendation_id=%s", int(recommendation_id))

    rows = cur.fetchall()

    mkbs = []

    for row in rows:
        mkbs.append("{0}".format(row[0]))

    return mkbs


def get_nozology_name_by_recommendation_id(cur, recommendation_id):

    cur.execute("SELECT `name` FROM recommendation WHERE id=%s LIMIT 1", int(recommendation_id))

    row = cur.fetchone()

    nozology_name = "{0}".format(row[0])

    return nozology_name


def get_table_tag_by_recommendation_id(cur, recommendation_id):

    cur.execute("SELECT `table` FROM recommendation WHERE id=%s LIMIT 1", int(recommendation_id))

    row = cur.fetchone()

    table_tag = "{0}".format(row[0])

    return table_tag


test1 = get_recommendation_from_db("i10")
