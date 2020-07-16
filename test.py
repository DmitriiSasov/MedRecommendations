from operator import attrgetter, itemgetter


class Thesis:
    def __init__(self, text, LCR, LRE):
        self.text = text
        self.LCR = LCR
        self.LRE = LRE


theses = [Thesis('раз', 'B', '2'),
          Thesis('раз', 'C', '1'),
          Thesis('раз', 'C', '5'),
          Thesis('раз', 'A', '3'),
          Thesis('раз', 'A', '1'),
          Thesis('раз', 'B', '3'),
          Thesis('раз', 'C', '4'),
          Thesis('раз', 'A', '4'),
          Thesis('раз', 'B', '2')]

theses.sort(key=attrgetter('LCR', 'LRE'))

a = 10

treatments = [['раз', 'B', '2'],
              ['раз', 'C', '1'],
              ['раз', 'C', '5'],
              ['раз', 'A', '3'],
              ['раз', 'A', '1'],
              ['раз', 'B', '3'],
              ['раз', 'C', '4'],
              ['раз', 'A', '4'],
              ['раз', 'B', '2']]

list.sort(key=itemgetter(1, 2))

a = 10
