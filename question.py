
import random
from fractions import Fraction

class Question:

    def __init__(self):
        self.left_question = Fraction(random.randrange(1,10),random.randrange(1,10))
        self.right_question = Fraction(random.randrange(1,10),random.randrange(1,10))
        self.populate_multiple_choice()

    def populate_multiple_choice(self):
        self.answer = random.randrange(4)
        self.answers = []
        for num in range(0,4):
            if num == self.answer:
                self.answers.append(self.left_question+self.right_question)
            else:
                self.answers.append(Fraction(random.randrange(1,10),random.randrange(1,10)))

    def is_answer(self,fraction):
        return (fraction == self.answers[self.answer])
