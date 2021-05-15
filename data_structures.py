
class Recommendation:

    nozology_name = ""

    #Все коды МКБ-10 из нозологии в виде строк
    MKBs = []

    #Словарь (название группы тезисов : список тезисов) тезисов, относящихся к диагностике
    diagnosticTheses = {}

    #Словарь (название группы тезисов : список тезисов) тезисов, относящихся к медикаментозному лечению (может быть пустым!!!) (список объектов класса Theses)
    treatmentTheses = []

    #Критерии оценки качества медицинской помощи (каждый из перечисленных ниже пунктов может быть пустым )

    table_tag = ""


class Thesis:

    def __init__(self):
        # Текст тезиса
        self.text = ""
        # УУР (A-C)
        self.LCR = ""
        # УДД (1-5)
        self.LRE = ""

    def __init__(self, text: str, LCR: str, LRE: str):
        self.LRE = LRE
        self.LCR = LCR
        self.text = text








