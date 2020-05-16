import numpy as np
from shared.probabilities import probability_table as pt


class Handler(object):
    """Handler class for managing bet probability retrieval"""

    def __init__(self):
        super(Handler, self).__init__()
        self.probs_table = pt.get()

    def get_probability_vector(self, cards=None, others_card_num=0):
        if cards is None:
            raise TypeError("No 'cards' provided.")
        if not all(isinstance(x, int) for x in cards):
            raise TypeError("'cards' is not an iterable of integers")
        self.cards = cards

        if others_card_num <= 0 or others_card_num >= 24:
            raise ValueError("No valid 'others_card_num' provided")
        self.others_card_num = others_card_num

        return np.fromfunction(np.vectorize(self.get_bet_prob), (88,))

    def get_bet_prob(self, action_id):
        if action_id in range(6):
            if action_id in self.cards:
                return 1.0
            else:
                index = len(self.cards)*100 + self.others_card_num
                return self.probs_table.loc[[index], ["highcard"]].values[0]
        else:
            return 0.0
