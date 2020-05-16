from os import path
from scipy.special import binom
from itertools import product
import pandas as pd
import numpy as np


def generate(filename="bet_probabilities.csv"):
    """
        Generate a dataframe of conditional probabilities
        of the occurance of a bet, given
        n = number of cards of the player
        o = number of cards of other players
        The rows are indexed with an integer:
        100*n + o
        i.e. 305 = I have 3 cards and others have 5,
             1012 = I have 10 cards and others have 12
    """
    rows = []
    # Enumerate n (your card number) and o (other player card number) combinations
    for player_card_num in range(1, 12):
        for others_card_num in range(1, 25-player_card_num):

            n = player_card_num
            o = others_card_num

            # Compute all possibilities - omega
            all_states = binom(24-n, o)

            # High card
            frequency = sum([binom(4, i) * binom(24-n-4, o-i) for i in range(1, 5)])
            highcard_prob = frequency / all_states

            # High card have 1
            frequency = sum([binom(3, i) * binom(24-n-3, o-i) for i in range(1, 4)])
            highcard_have_1_prob = frequency / all_states

            # High card have 2
            frequency = sum([binom(2, i) * binom(24-n-2, o-i) for i in range(1, 3)])
            highcard_have_2_prob = frequency / all_states

            # High card have 3
            frequency = binom(24-n-1, o-1)
            highcard_have_3_prob = frequency / all_states

            # Pair
            frequency = sum([binom(4, i) * binom(24-n-4, o-i) for i in range(2, 5)])
            pair_prob = frequency / all_states

            # Pair have 1
            frequency = sum([binom(3, i) * binom(24-n-3, o-i) for i in range(2, 4)])
            pair_have_1_prob = frequency / all_states

            # Pair have 2
            frequency = binom(24-n-2, o-2)
            pair_have_2_prob = frequency / all_states

            # Two pairs
            occurance_combinations = product(range(2, 5), range(2, 5))
            frequency = sum([binom(4, c1)*binom(4, c2)*binom(24-n-8, o-c1-c2) for c1, c2 in occurance_combinations])
            twopairs_prob = frequency / all_states

            # Three
            frequency = binom(4, 3) * binom(24-n-4, o-3) + binom(4,4) * binom(24-n-4, o-4)
            three_prob = frequency / all_states

            # Three have 1
            frequency = binom(24-n-3, o-3)
            three_have_1_prob = frequency / all_states

            # Four
            frequency = binom(24-n-4, o-4)
            four_prob = frequency / all_states

            # Colour
            frequency = binom(6,5) * binom(24-n-6, o-5) + binom(6,6) * binom(24-n-6, o-6)
            colour_prob = frequency / all_states

            # Colour have 1
            frequency = 0
            if n >= 1:
                frequency = binom(5,4) * binom(24-n-5, o-4) + binom(5,5) * binom(24-n-5, o-5)
            colour_have_1_prob = frequency / all_states

            # Colour have 2
            frequency = 0
            if n >= 2:
                frequency = binom(4,3) * binom(24-n-4, o-3) + binom(4,4) * binom(24-n-4, o-4)
            colour_have_2_prob = frequency / all_states

            # Colour have 3
            frequency = 0
            if n >= 3:
                frequency = binom(3,2) * binom(24-n-3, o-2) + binom(3,3) * binom(24-n-3, o-3)
            colour_have_3_prob = frequency / all_states

            # Colour have 4
            frequency = 0
            if n >= 4:
                frequency = binom(2,1) * binom(24-n-2, o-1) + binom(2,2) * binom(24-n-2, o-2)
            colour_have_4_prob = frequency / all_states

            # Straight
            frequency = pow(binom(4, 1), 5) * binom(24-n-5*4, o-5)
            straight_prob = frequency / all_states

            # Straight have 1
            frequency = 0
            if n >= 1:
                frequency = pow(binom(4, 1), 4) * binom(24-n-4*4, o-4)
            straight_have_1_prob = frequency / all_states

            # Straight have 2
            frequency = 0
            if n >= 2:
                frequency = pow(binom(4, 1), 3) * binom(24-n-3*4, o-3)
            straight_have_2_prob = frequency / all_states

            # Straight have 3
            frequency = 0
            if n >= 3:
                frequency = pow(binom(4, 1), 2) * binom(24-n-2*4, o-2)
            straight_have_3_prob = frequency / all_states

            # Straight have 4
            frequency = 0
            if n >= 4:
                frequency = binom(4, 1) * binom(24-n-1*4, o-1)
            straight_have_4_prob = frequency / all_states

            # Flush
            frequency = binom(24-n-5, o-5)
            flush_prob = frequency / all_states

            # Flush have 1
            frequency = 0
            if n >= 1:
                frequency = binom(24-n-4, o-4)
            flush_have_1_prob = frequency / all_states

            # Flush have 2
            frequency = 0
            if n >= 2:
                frequency = binom(24-n-3, o-3)
            flush_have_2_prob = frequency / all_states

            # Flush have 3
            frequency = 0
            if n >= 3:
                frequency = binom(24-n-2, o-2)
            flush_have_3_prob = frequency / all_states

            # Flush have 4
            frequency = 0
            if n >= 4:
                frequency = binom(24-n-1, o-1)
            flush_have_4_prob = frequency / all_states

            # Flush great
            frequency = binom(24-n-6, o-6)
            flush_great_prob = frequency / all_states

            # Full house
            occurance_combinations = product(range(3, 5), range(2, 5))
            frequency = sum([binom(4, c1)*binom(4, c2)*binom(24-n-8, o-c1-c2) for c1, c2 in occurance_combinations])
            fullhouse_prob = frequency / all_states

            # Full house have 0 and 1
            occurance_combinations = product(range(3, 5), range(1, 4))
            frequency = 0
            if n >= 1:
                frequency = sum([binom(4, c1)*binom(3, c2)*binom(24-n-7, o-c1-c2) for c1, c2 in occurance_combinations])
            fullhouse_have_0_and_1_prob = frequency / all_states

            # Full house have 1 and 0
            occurance_combinations = product(range(2, 4), range(2, 5))
            frequency = 0
            if n >= 1:
                frequency = sum([binom(3, c1)*binom(4, c2)*binom(24-n-7, o-c1-c2) for c1, c2 in occurance_combinations])
            fullhouse_have_1_and_0_prob = frequency / all_states

            # Full house have 1 and 1
            occurance_combinations = product(range(2, 4), range(1, 4))
            frequency = 0
            if n >= 2:
                frequency = sum([binom(3, c1)*binom(3, c2)*binom(24-n-6, o-c1-c2) for c1, c2 in occurance_combinations])
            fullhouse_have_1_and_1_prob = frequency / all_states

            # Full house have 2 and 0
            occurance_combinations = product(range(1, 3), range(2, 5))
            frequency = 0
            if n >= 2:
                frequency = sum([binom(2, c1)*binom(4, c2)*binom(24-n-6, o-c1-c2) for c1, c2 in occurance_combinations])
            fullhouse_have_2_and_0_prob = frequency / all_states

            # Full house have 2 and 1
            occurance_combinations = product(range(1, 3), range(1, 4))
            frequency = 0
            if n >= 3:
                frequency = sum([binom(2, c1)*binom(3, c2)*binom(24-n-5, o-c1-c2) for c1, c2 in occurance_combinations])
            fullhouse_have_2_and_1_prob = frequency / all_states

            # Row index
            index = n*100 + o

            row = {
                "index": index,
                "highcard": highcard_prob,
                "highcard_have_1": highcard_have_1_prob,
                "highcard_have_2": highcard_have_2_prob,
                "highcard_have_3": highcard_have_3_prob,
                "pair": pair_prob,
                "pair_have_1": pair_have_1_prob,
                "pair_have_2": pair_have_2_prob,
                "twopairs": twopairs_prob,
                "three": three_prob,
                "three_have_1": three_have_1_prob,
                "four": four_prob,
                "colour": colour_prob,
                "colour_have_1": colour_have_1_prob,
                "colour_have_2": colour_have_2_prob,
                "colour_have_3": colour_have_3_prob,
                "colour_have_4": colour_have_4_prob,
                "straight": straight_prob,
                "straight_have_1": straight_have_1_prob,
                "straight_have_2": straight_have_2_prob,
                "straight_have_3": straight_have_3_prob,
                "straight_have_4": straight_have_4_prob,
                "flush": flush_prob,
                "flush_have_1": flush_have_1_prob,
                "flush_have_2": flush_have_2_prob,
                "flush_have_3": flush_have_3_prob,
                "flush_have_4": flush_have_4_prob,
                "flush_great": flush_great_prob,
                "fullhouse": fullhouse_prob,
                "fullhouse_have_1_and_0": fullhouse_have_1_and_0_prob,
                "fullhouse_have_2_and_0": fullhouse_have_2_and_0_prob,
                "fullhouse_have_0_and_1": fullhouse_have_0_and_1_prob,
                "fullhouse_have_1_and_1": fullhouse_have_1_and_1_prob,
                "fullhouse_have_2_and_1": fullhouse_have_2_and_1_prob
            }

            assert all(map(lambda x: (row[x] <= 1.0 or np.isnan(row[x]) or x == "index"), row)) # Probabilities need to <= 1.0
            rows.append(row)

    table = pd.DataFrame.from_dict(rows)
    table.set_index(["index"], inplace=True, verify_integrity=True)
    if filename:
        table.to_csv(filename)

    return table


def load(filename="bet_probabilities.csv"):
    if filename and path.exists(filename):
        return pd.read_csv(filename, index_col="index")
    else:
        raise FileNotFoundError("Got no valid filename. filename: {}".format(filename))


def get():
    try:
        return load()
    except FileNotFoundError:
        return generate()


if __name__ == "__main__":
    """ Run script manually - generate and save a table of probabilities """
    table = generate()
    print("Generated a probability table with {} rows and {} columns.".format(table.shape[0], table.shape[1]))
