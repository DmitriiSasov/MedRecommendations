from operator import attrgetter


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

