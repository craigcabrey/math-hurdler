class Fraction():
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def ratio(self):
        return float(self.numerator) / float(self.denominator)

    def __eq__(self, other):
        return self.ratio() == other.ratio()

    def __lt__(self, other):
        return self.ratio() < other.ratio()

    def __gt__(self, other):
        return self.ratio() > other.ratio()

    def __le__(self, other):
        return self.ratio() <= other.ratio()

    def __ge__(self, other):
        return self.other() >= other.ratio()

    def __repr__(self):
        return '{0} / {1}'.format(self.numerator, self.denominator)
