import itertools
import numpy as np
from shared.probabilities import probability_table as pt

class Cards(object):
    """A class for card information storage."""

    def __init__(self, cards):
        super(Cards, self).__init__()
        self.__raw = cards
        self.values = set(list(zip(*cards))[0])
        self.colours = set(list(zip(*cards))[1])
        self.with_value = {i: [] for i in range(4)}
        self.with_colour = {i: [] for i in range(4)}
        self.with_value.update({tup[0]: list(tup[1]) for tup in itertools.groupby(cards, lambda x: x[0])})
        self.with_colour.update({tup[0]: list(tup[1]) for tup in itertools.groupby(cards, lambda x: x[1])})

    def __getitem__(self, index):
        return self.__raw[index]

    def __len__(self):
         return len(self.__raw)

    def all_with_colour(c):
        if isinstance(c, int) and c >= 0 and c <= 3:
            return


class Handler(object):
    """Handler class for managing bet probability retrieval"""

    def __init__(self):
        super(Handler, self).__init__()
        self.probs_table = pt.get()

    def get_probability_vector(self, cards=None, others_card_num=0):
        if cards is None:
            raise TypeError("No 'cards' provided.")
        if not all(len(c) == 2 and all(isinstance(val, int) for val in c) for c in cards):
            raise TypeError("'cards' is not an iterable of integer tuples")
        self.cards = Cards(cards)

        if others_card_num <= 0 or others_card_num >= 24:
            raise ValueError("No valid 'others_card_num' provided")
        self.others_card_num = others_card_num

        return np.fromfunction(np.vectorize(self.get_bet_prob), (88,))

    def get_table_value(self, column):
        index = len(self.cards)*100 + self.others_card_num
        return self.probs_table.loc[[index], [column]].values[0]

    def get_bet_prob(self, action_id):
        if action_id in range(6):
            if action_id in self.cards.values:
                return 1.0
            else:
                return self.get_table_value("highcard")
        else:
            return 0.0
