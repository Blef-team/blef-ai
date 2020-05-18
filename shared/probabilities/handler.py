import itertools
from collections import defaultdict
import numpy as np
from shared.probabilities import probability_table as pt


class Cards(object):
    """A class for card information storage."""

    def __init__(self, cards):
        super(Cards, self).__init__()
        cards = sorted(cards) # itertools.groupby won't work if cards not sorted
        self.__raw = cards
        self.values = set(list(zip(*cards))[0])
        self.colours = set(list(zip(*cards))[1])
        # Group cards by colour and value
        self.with_value = self.group_cards(cards, by="value")
        self.with_colour = self.group_cards(cards, by="colour")

    def __getitem__(self, index):
        return self.__raw[index]

    def __len__(self):
         return len(self.__raw)

    @staticmethod
    def group_cards(cards, by="value"):
        if by == "value":
            with_value = defaultdict(list)
            for value, grouped_cards in itertools.groupby(cards, lambda x: x[0]):
                with_value[value].extend(list(grouped_cards))
            return with_value
        if by == "colour":
            with_colour = defaultdict(list)
            for colour, grouped_cards in itertools.groupby(cards, lambda x: x[1]):
                with_colour[colour].extend(list(grouped_cards))
            return with_colour
        raise ValueError("'by' needs to be either 'value' or 'colour'")



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
        self.card_values_for_bet = {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [0], 7: [1], 8: [2], 9: [3], 10: [4], 11: [5], 12: [0, 1], 13: [0, 2], 14: [1, 2], 15: [0, 3], 16: [1, 3], 17: [2, 3], 18: [0, 4], 19: [1, 4], 20: [2, 4], 21: [3, 4], 22: [0, 5], 23: [1, 5], 24: [2, 5], 25: [3, 5], 26: [4, 5], 27: [0, 1, 2, 3, 4], 28: [1, 2, 3, 4, 5], 29: [0, 1, 2, 3, 4, 5], 30: [0], 31: [1], 32: [2], 33: [3], 34: [4], 35: [5], 36: [0, 1], 37: [0, 2], 38: [0, 3], 39: [0, 4], 40: [0, 5], 41: [1, 0], 42: [1, 2], 43: [1, 3], 44: [1, 4], 45: [1, 5], 46: [2, 0], 47: [2, 1], 48: [2, 3], 49: [2, 4], 50: [2, 5], 51: [3, 0], 52: [3, 1], 53: [3, 2], 54: [3, 4], 55: [3, 5], 56: [4, 0], 57: [4, 1], 58: [4, 2], 59: [4, 3], 60: [4, 5], 61: [5, 0], 62: [5, 1], 63: [5, 2], 64: [5, 3], 65: [5, 4], 70: [0], 71: [1], 72: [2], 73: [3], 74: [4], 75: [5], 76: [0, 1, 2, 3, 4], 77: [0, 1, 2, 3, 4], 78: [0, 1, 2, 3, 4], 79: [0, 1, 2, 3, 4], 80: [1, 2, 3, 4, 5], 81: [1, 2, 3, 4, 5], 82: [1, 2, 3, 4, 5], 83: [1, 2, 3, 4, 5], 84: [0, 1, 2, 3, 4, 5], 85: [0, 1, 2, 3, 4, 5], 86: [0, 1, 2, 3, 4, 5], 87: [0, 1, 2, 3, 4, 5]}
        self.card_colour_for_bet = {66: 0, 67: 1, 68: 2, 69: 3, 76: 0, 77: 1, 78: 2, 79: 3, 80: 0, 81: 1, 82: 2, 83: 3, 84: 0, 85: 1, 86: 2, 87: 3}

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
            value_1_num = len(self.cards.with_value[value_1])
            value_2_num = len(self.cards.with_value[value_2])
            if value_1_num >= 2 and value_2_num >= 2:
                return 1.0
            if value_1_num >= 2 and value_2_num == 1:
                return self.get_table_value(pt.BetType.PAIR_HAVE_1)
            if value_1_num == 1 and value_2_num >= 2:
                return self.get_table_value(pt.BetType.PAIR_HAVE_1)
            if value_1_num >= 2 and value_2_num == 0:
                return self.get_table_value(pt.BetType.PAIR)
            if value_1_num == 0 and value_2_num >= 2:
                return self.get_table_value(pt.BetType.PAIR)
            if value_1_num == 1 and value_2_num == 1:
                return self.get_table_value(pt.BetType.TWOPAIRS_HAVE_1_HAVE_1)
            if value_1_num == 1 and value_2_num == 0:
                return self.get_table_value(pt.BetType.TWOPAIRS_HAVE_1)
            if value_1_num == 0 and value_2_num == 1:
                return self.get_table_value(pt.BetType.TWOPAIRS_HAVE_1)
            return self.get_table_value(pt.BetType.TWOPAIRS)

        elif action_id in {27, 28}:
            # Small straight & Big straight
            have_n_cards = sum([bool(self.cards.with_value[value]) for value in self.card_values_for_bet[action_id]])
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

        elif action_id in range(30, 36):
            # Three of a kind
            value = self.card_values_for_bet[action_id][0]
            if len(self.cards.with_value[value]) >= 3:
                return 1.0
            if len(self.cards.with_value[value]) == 2:
                return self.get_table_value(pt.BetType.THREE_HAVE_2)
            if len(self.cards.with_value[value]) == 1:
                return self.get_table_value(pt.BetType.THREE_HAVE_1)
            return self.get_table_value(pt.BetType.THREE)

        elif action_id in range(36, 66):
            # Full house
            value_1, value_2 = self.card_values_for_bet[action_id]
            value_1_num = len(self.cards.with_value[value_1])
            value_2_num = len(self.cards.with_value[value_2])
            if value_1_num >= 3 and value_2_num >= 2:
                return 1.0
            if value_1_num == 2 and value_2_num == 2:
                return self.get_table_value(pt.BetType.THREE_HAVE_2)
            if value_1_num == 1 and value_2_num == 2:
                return self.get_table_value(pt.BetType.THREE_HAVE_1)
            if value_1_num == 0 and value_2_num == 2:
                return self.get_table_value(pt.BetType.THREE)
            if value_1_num >= 3 and value_2_num == 1:
                return self.get_table_value(pt.BetType.PAIR_HAVE_1)
            if value_1_num == 2 and value_2_num == 1:
                return self.get_table_value(pt.BetType.FULLHOUSE_HAVE_2_AND_1)
            if value_1_num == 1 and value_2_num == 1:
                return self.get_table_value(pt.BetType.FULLHOUSE_HAVE_1_AND_1)
            if value_1_num == 0 and value_2_num == 1:
                return self.get_table_value(pt.BetType.FULLHOUSE_HAVE_0_AND_1)
            if value_1_num >= 3 and value_2_num == 0:
                return self.get_table_value(pt.BetType.PAIR)
            if value_1_num == 2 and value_2_num == 0:
                return self.get_table_value(pt.BetType.FULLHOUSE_HAVE_2_AND_0)
            if value_1_num == 1 and value_2_num == 0:
                return self.get_table_value(pt.BetType.FULLHOUSE_HAVE_1_AND_1)
            return self.get_table_value(pt.BetType.FULLHOUSE)

        elif action_id in range(66, 70):
            # Colour
            colour = self.card_colour_for_bet[action_id]
            if len(self.cards.with_colour[colour]) >= 5:
                return 1.0
            if len(self.cards.with_colour[colour]) == 4:
                return self.get_table_value(pt.BetType.COLOUR_HAVE_4)
            if len(self.cards.with_colour[colour]) == 3:
                return self.get_table_value(pt.BetType.COLOUR_HAVE_3)
            if len(self.cards.with_colour[colour]) == 2:
                return self.get_table_value(pt.BetType.COLOUR_HAVE_2)
            if len(self.cards.with_colour[colour]) == 1:
                return self.get_table_value(pt.BetType.COLOUR_HAVE_1)
            return self.get_table_value(pt.BetType.COLOUR)

        elif action_id in range(70, 76):
            # Four of a kind
            value = self.card_values_for_bet[action_id][0]
            if len(self.cards.with_value[value]) == 4:
                return 1.0
            if len(self.cards.with_value[value]) == 3:
                return self.get_table_value(pt.BetType.FOUR_HAVE_3)
            if len(self.cards.with_value[value]) == 2:
                return self.get_table_value(pt.BetType.FOUR_HAVE_2)
            if len(self.cards.with_value[value]) == 1:
                return self.get_table_value(pt.BetType.FOUR_HAVE_1)
            return self.get_table_value(pt.BetType.FOUR)

        elif action_id in range(76, 84):
            # Small flush & big flush
            colour = self.card_colour_for_bet[action_id]
            relevant_cards = [card for value in self.card_values_for_bet[action_id] for card in self.cards.with_value[value]]
            have_n_cards = len(Cards.group_cards(relevant_cards, by="colour")[colour])
            if have_n_cards == 5:
                return 1.0
            if have_n_cards == 4:
                return self.get_table_value(pt.BetType.FLUSH_HAVE_4)
            if have_n_cards == 3:
                return self.get_table_value(pt.BetType.FOUR_HAVE_3)
            if have_n_cards == 2:
                return self.get_table_value(pt.BetType.FLUSH_HAVE_2)
            if have_n_cards == 1:
                return self.get_table_value(pt.BetType.FOUR_HAVE_1)
            return self.get_table_value(pt.BetType.FLUSH)

        elif action_id in range(84, 88):
            # Great flush
            colour = self.card_colour_for_bet[action_id]
            have_n_cards = len(self.cards.with_colour[colour])
            if have_n_cards == 6:
                return 1.0
            if have_n_cards == 5:
                return self.get_table_value(pt.BetType.FLUSH_HAVE_4)
            if have_n_cards == 4:
                return self.get_table_value(pt.BetType.FOUR_HAVE_3)
            if have_n_cards == 3:
                return self.get_table_value(pt.BetType.FLUSH_HAVE_2)
            if have_n_cards == 2:
                return self.get_table_value(pt.BetType.FOUR_HAVE_1)
            if have_n_cards == 1:
                return self.get_table_value(pt.BetType.FLUSH)
            return self.get_table_value(pt.BetType.FLUSH_GREAT)
        else:
            raise ValueError("action_id must be from 0 to 87 (inclusive)")
