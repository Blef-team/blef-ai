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
        self.with_value = {i: [] for i in range(6)}
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
        # Validate probs_table - check header for all bet types
        bet_types = [getattr(pt.BetType, attr) for attr in dir(pt.BetType) if not callable(getattr(pt.BetType, attr)) and not attr.startswith("__")]
        if not all(bet_type in self.probs_table.columns for bet_type in bet_types):
            print([(bet_type, bet_type in self.probs_table.columns) for bet_type in bet_types])
            raise ValueError("The probability table is corrupted! Consider deleting the CSV.")
        self.card_values_for_bet = {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [0], 7: [1], 8: [2], 9: [3], 10: [4], 11: [5], 12: [0, 1], 13: [0, 2], 14: [1, 2], 15: [0, 3], 16: [1, 3], 17: [2, 3], 18: [0, 4], 19: [1, 4], 20: [2, 4], 21: [3, 4], 22: [0, 5], 23: [1, 5], 24: [2, 5], 25: [3, 5], 26: [4, 5], 30: [0], 31: [1], 32: [2], 33: [3], 34: [4], 35: [5], 36: [0, 1], 37: [0, 2], 38: [0, 3], 39: [0, 4], 40: [5], 41: [1], 42: [1, 2], 43: [1, 3], 44: [1, 4], 45: [1, 5], 46: [0, 2], 47: [1, 2], 48: [2, 3], 49: [2, 4], 50: [2, 5], 51: [0, 3], 52: [1, 3], 53: [2, 3], 54: [3, 4], 55: [3, 5], 56: [0, 4], 57: [1, 4], 58: [2, 4], 59: [3, 4], 60: [4, 5], 61: [0, 5], 62: [1, 5], 63: [2, 5], 64: [3, 5], 65: [4, 5], 70: [0], 71: [1], 72: [2], 73: [3], 74: [4], 75: [5]}

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
        try:
            action_id = int(action_id)
        except (ValueError, TypeError) as e:
            raise e("action_id is not valid: {}".format(action_id))
        if action_id in range(6):
            # High card
            if action_id in self.cards.values:
                return 1.0
            else:
                return self.get_table_value("highcard")
        elif action_id in range(6, 12):
            # Pair
            value = self.card_values_for_bet[action_id][0]
            if len(self.cards.with_value[value]) >= 2:
                return 1.0
            if len(self.cards.with_value[value]) == 1:
                return self.get_table_value(pt.BetType.PAIR_HAVE_1)
            return self.get_table_value(pt.BetType.PAIR)
        elif action_id in range(12, 27):
            # Two cards
            value_1, value_2 = self.card_values_for_bet[action_id]
            if len(self.cards.with_value[value_1]) >= 2 and len(self.cards.with_value[value_2]) >= 2:
                return 1.0
            if len(self.cards.with_value[value_1]) >= 2 and len(self.cards.with_value[value_2]) == 1:
                return self.get_table_value(pt.BetType.PAIR_HAVE_1)
            if len(self.cards.with_value[value_1]) == 1 and len(self.cards.with_value[value_2]) >= 2:
                return self.get_table_value(pt.BetType.PAIR_HAVE_1)
            if len(self.cards.with_value[value_1]) >= 2 and len(self.cards.with_value[value_2]) == 0:
                return self.get_table_value(pt.BetType.PAIR)
            if len(self.cards.with_value[value_1]) == 0 and len(self.cards.with_value[value_2]) >= 2:
                return self.get_table_value(pt.BetType.PAIR)
            if len(self.cards.with_value[value_1]) == 1 and len(self.cards.with_value[value_2]) == 1:
                return self.get_table_value(pt.BetType.TWOPAIRS_HAVE_1_HAVE_1)
            if len(self.cards.with_value[value_1]) == 1 and len(self.cards.with_value[value_2]) == 0:
                return self.get_table_value(pt.BetType.TWOPAIRS_HAVE_1)
            if len(self.cards.with_value[value_1]) == 0 and len(self.cards.with_value[value_2]) == 1:
                return self.get_table_value(pt.BetType.TWOPAIRS_HAVE_1)
            return self.get_table_value(pt.BetType.TWOPAIRS)
        elif action_id in {27, 28}:
            if action_id == 27:
                # Small straight
                have_n_cards = sum([bool(self.cards.with_value[value]) for value in range(5)])
            else:
                # Big straight
                have_n_cards = sum([bool(self.cards.with_value[value]) for value in range(1,6)])
            if have_n_cards == 5:
                return 1.0
            if have_n_cards == 4:
                return self.get_table_value(pt.BetType.STRAIGHT_HAVE_4)
            if have_n_cards == 3:
                return self.get_table_value(pt.BetType.STRAIGHT_HAVE_3)
            if have_n_cards == 2:
                return self.get_table_value(pt.BetType.STRAIGHT_HAVE_2)
            if have_n_cards == 1:
                return self.get_table_value(pt.BetType.STRAIGHT_HAVE_1)
            return self.get_table_value(pt.BetType.STRAIGHT)
        elif action_id == 29:
            # Great straight
            have_n_cards = sum([bool(self.cards.with_value[value]) for value in self.cards.with_value])
            if have_n_cards == 6:
                return 1.0
            if have_n_cards == 5:
                return self.get_table_value(pt.BetType.STRAIGHT_HAVE_4)
            if have_n_cards == 4:
                return self.get_table_value(pt.BetType.STRAIGHT_HAVE_3)
            if have_n_cards == 3:
                return self.get_table_value(pt.BetType.STRAIGHT_HAVE_2)
            if have_n_cards == 2:
                return self.get_table_value(pt.BetType.STRAIGHT_HAVE_1)
            if have_n_cards == 1:
                return self.get_table_value(pt.BetType.STRAIGHT)
            raise ValueError("It's impossible to have no cards matching a great straight! (empty hand?)")

        else:
            return 0.0
