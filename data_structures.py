class Recommendation:
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


class Thesis:

    def __init__(self, text: str, LCR: str, LRE: str):
        self.LRE = LRE
        self.LCR = LCR
        self.text = text
