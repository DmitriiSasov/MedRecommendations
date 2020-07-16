from backend import createPDF
from operator import attrgetter


def sort(mkbs, recommendations):
    diagnos_dic = {}

    for rec in recommendations:
        diagnostic_theses = rec.diagnosticTheses
        for key in diagnostic_theses:
            for element in diagnostic_theses[key]:
                element.LCR = lcr_replace(str(element.LCR))
                element.LRE = lre_replace(str(element.LRE))
            value = diagnostic_theses.get(key)
            value.sort(key=attrgetter('LCR', 'LRE'))


def lcr_replace(lcr):
    lcr.replace('А', 'A')
    lcr.replace('В', 'B')
    lcr.replace('С', 'C')

    return lcr


def lre_replace(lre):
    lre.replace('I', '1')
    lre.replace('II', '2')
    lre.replace('III', '3')
    lre.replace('IV', '4')
    lre.replace('V', '5')

    return lre
