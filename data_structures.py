import functools
from datetime import datetime
import collections


class Recommendation:
    _id = ""

    nozology_name = ""

    # Все коды МКБ-10 из нозологии в виде строк
    MKBs = []

    # Словарь (название группы тезисов : список тезисов) тезисов, относящихся к диагностике
    diagnosticTheses = {}

    # Словарь (название группы тезисов : список тезисов) тезисов, относящихся к медикаментозному лечению
    # (может быть пустым!!!) (список объектов класса Theses)
    treatmentTheses = []

    # Критерии оценки качества медицинской помощи (каждый из перечисленных ниже пунктов может быть пустым )

    table_tag = ""

    publication_date = ""

    def __init__(self, nozology_name, MKBs, diagnosticTheses, treatmentTheses, table_tag, publication_date):
        self.nozology_name = nozology_name
        self.MKBs = MKBs
        self.diagnosticTheses = diagnosticTheses
        self.treatmentTheses = treatmentTheses
        self.table_tag = table_tag
        self.publication_date = publication_date
        self._id = nozology_name + str(MKBs) + str(publication_date)

    @staticmethod
    def from_json(json_obj):
        if json_obj is None:
            res = None
        else:
            res = Recommendation(json_obj['nozology_name'], json_obj['MKBs'], json_obj['diagnosticTheses'],
                                 json_obj['treatmentTheses'], json_obj['table_tag'], json_obj['publication_date'])
            for diagnostic_block_name in res.diagnosticTheses:
                theses = []
                for thesis in res.diagnosticTheses[diagnostic_block_name]:
                    theses.append(Thesis.from_json(thesis))
                res.diagnosticTheses[diagnostic_block_name] = theses
            treatment_theses = []
            for thesis in res.treatmentTheses:
                treatment_theses.append(Thesis.from_json(thesis))
            res.treatmentTheses = treatment_theses

        return res

    def serialize(self):
        serialized_obj = {
            '_id': self._id,
            'nozology_name': self.nozology_name,
            'MKBs': self.MKBs,
            'diagnosticTheses': {},
            'treatmentTheses': [],
            'table_tag': str(self.table_tag),
            'publication_date': self.publication_date,
        }
        for diagnostic_block_name in self.diagnosticTheses:
            serialized_obj['diagnosticTheses'][diagnostic_block_name] = []
            for thesis in self.diagnosticTheses[diagnostic_block_name]:
                serialized_obj['diagnosticTheses'][diagnostic_block_name].append(thesis.serialize())
        for treatment_thesis in self.treatmentTheses:
            serialized_obj['treatmentTheses'].append(treatment_thesis.serialize())
        return serialized_obj

    def __eq__(self, o: object) -> bool:
        if type(self) != type(o):
            return False
        res = self.nozology_name == o.nozology_name
        res = res and self._id == o._id
        if len(self.treatmentTheses) == len(o.treatmentTheses):
            for i in range(len(self.treatmentTheses)):
                res = res and self.treatmentTheses[i] == o.treatmentTheses[i]
        else:
            res = False
        if self.diagnosticTheses.keys() == o.diagnosticTheses.keys():
            for key in self.diagnosticTheses:
                for i in range(len(self.diagnosticTheses[key])):
                    res = res and self.diagnosticTheses[key] == o.diagnosticTheses[key][i]
        else:
            res = False
        res = self.diagnosticTheses == o.diagnosticTheses
        res = res and self.MKBs == o.MKBs
        res = res and self.table_tag == o.table_tag
        res = res and self.publication_date == o.publication_date
        return res


class Thesis:

    def __init__(self, text: str, LCR: str, LRE: str):
        self.text = text
        self.LCR = LCR
        self.LRE = LRE

    @staticmethod
    def from_json(json_obj):
        if json_obj is None:
            res = None
        else:
            res = Thesis(json_obj['text'], json_obj['LCR'], json_obj['LRE'])
        return res

    def serialize(self):
        return {
            'text': self.text,
            'LCR': self.LCR,
            'LRE': self.LRE,
        }

    def __eq__(self, o: object) -> bool:
        if type(self) != type(o):
            return False
        if self.text == o.text and \
                self.LCR == o.LCR and \
                self.LRE == o.LRE:
            return True
        else:
            return False
