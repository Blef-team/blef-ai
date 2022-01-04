import uuid
from math import floor
from random import shuffle, sample, choice
from itertools import islice, product
import json
import os


CHECK = 88

INDEXATION_CSV = """action_id,set_type,detail_1,detail_2
0,High card,0,
1,High card,1,
2,High card,2,
3,High card,3,
4,High card,4,
5,High card,5,
6,Pair,0,
7,Pair,1,
8,Pair,2,
9,Pair,3,
10,Pair,4,
11,Pair,5,
12,Two pairs,1,0
13,Two pairs,2,0
14,Two pairs,2,1
15,Two pairs,3,0
16,Two pairs,3,1
17,Two pairs,3,2
18,Two pairs,4,0
19,Two pairs,4,1
20,Two pairs,4,2
21,Two pairs,4,3
22,Two pairs,5,0
23,Two pairs,5,1
24,Two pairs,5,2
25,Two pairs,5,3
26,Two pairs,5,4
27,Small straight,,
28,Big straight,,
29,Great straight,,
30,Three of a kind,0,
31,Three of a kind,1,
32,Three of a kind,2,
33,Three of a kind,3,
34,Three of a kind,4,
35,Three of a kind,5,
36,Full house,0,1
37,Full house,0,2
38,Full house,0,3
39,Full house,0,4
40,Full house,0,5
41,Full house,1,0
42,Full house,1,2
43,Full house,1,3
44,Full house,1,4
45,Full house,1,5
46,Full house,2,0
47,Full house,2,1
48,Full house,2,3
49,Full house,2,4
50,Full house,2,5
51,Full house,3,0
52,Full house,3,1
53,Full house,3,2
54,Full house,3,4
55,Full house,3,5
56,Full house,4,0
57,Full house,4,1
58,Full house,4,2
59,Full house,4,3
60,Full house,4,5
61,Full house,5,0
62,Full house,5,1
63,Full house,5,2
64,Full house,5,3
65,Full house,5,4
66,Colour,0,
67,Colour,1,
68,Colour,2,
69,Colour,3,
70,Four of a kind,0,
71,Four of a kind,1,
72,Four of a kind,2,
73,Four of a kind,3,
74,Four of a kind,4,
75,Four of a kind,5,
76,Small flush,0,
77,Small flush,1,
78,Small flush,2,
79,Small flush,3,
80,Big flush,0,
81,Big flush,1,
82,Big flush,2,
83,Big flush,3,
84,Great flush,0,
85,Great flush,1,
86,Great flush,2,
87,Great flush,3,"""


def load_indexation():
    header = None
    indexation = []
    for line in INDEXATION_CSV.split("\n"):
        if not header:
            header = line
            continue
        action_id, set_type, detail_1, detail_2 = line.split(",")
        indexation.append({"action_id": action_id,
                           "set_type": set_type,
                           "detail_1": detail_1,
                           "detail_2": detail_2
                           })
    return indexation

INDEXATION = load_indexation()


def save(game, dir="games"):
    state_id = game["game_uuid"] + "_" + str(int(game['round_number']))
    filename = os.path.join(dir, state_id)
    with open(filename, "w") as filehandle:
        json.dump(game, filehandle)


def determine_set_existence(cards, action_id):
    try:
        action_id = int(action_id)
        set_row = INDEXATION[action_id]
        set_type = set_row["set_type"]
        detail_1 = int(set_row["detail_1"]) if set_row["detail_1"] else None
        detail_2 = int(set_row["detail_2"]) if set_row["detail_2"] else None
        card_values = [card["value"] for card in cards]
        card_colours = [card["colour"] for card in cards]

        if set_type == "High card":
            return card_values.count(detail_1) >= 1
        elif set_type == "Pair":
            return card_values.count(detail_1) >= 2
        elif set_type == "Two pairs":
            return card_values.count(detail_1) >= 2 and card_values.count(detail_2) >= 2
        elif set_type == "Small straight":
            return card_values.count(0) > 0 and card_values.count(1) > 0 and card_values.count(2) > 0 and card_values.count(3) > 0 and card_values.count(4) > 0
        elif set_type == "Big straight":
            return card_values.count(1) > 0 and card_values.count(2) > 0 and card_values.count(3) > 0 and card_values.count(4) > 0 and card_values.count(5) > 0
        elif set_type == "Great straight":
            return card_values.count(0) > 0 and card_values.count(1) > 0 and card_values.count(2) > 0 and card_values.count(3) > 0 and card_values.count(4) > 0 and card_values.count(5) > 0
        elif set_type == "Three of a kind":
            return card_values.count(detail_1) >= 3
        elif set_type == "Full house":
            return card_values.count(detail_1) >= 3 and card_values.count(detail_2) >= 2
        elif set_type == "Colour":
            return card_colours.count(detail_1) >= 5
        elif set_type == "Four of a kind":
            return card_values.count(detail_1) >= 4
        elif set_type == "Small flush":
            relevant_values = [card["value"] for card in cards if card["colour"] == detail_1]
            if not relevant_values:
                return False
            return relevant_values.count(0) > 0 and relevant_values.count(1) > 0 and relevant_values.count(2) > 0 and relevant_values.count(3) > 0 and relevant_values.count(4) > 0
        elif set_type == "Big flush":
            relevant_values = [card["value"] for card in cards if card["colour"] == detail_1]
            if not relevant_values:
                return False
            return relevant_values.count(1) > 0 and relevant_values.count(2) > 0 and relevant_values.count(3) > 0 and relevant_values.count(4) > 0 and relevant_values.count(5) > 0
        elif set_type == "Great flush":
            relevant_values = [card["value"] for card in cards if card["colour"] == detail_1]
            if not relevant_values:
                return False
            return relevant_values.count(0) > 0 and relevant_values.count(1) > 0 and relevant_values.count(2) > 0 and relevant_values.count(3) > 0 and relevant_values.count(4) > 0 and relevant_values.count(5) > 0

        return False

    except Exception as err:
        raise type(err)(f"{err} \n Failed in determine_set_existence")


def draw_cards(players):
    possible_cards = product(range(6), range(4))
    all_cards_raw = sample(list(possible_cards), sum(int(p["n_cards"]) for p in players))
    all_cards = [{"value": tup[0], "colour": tup[1]} for tup in all_cards_raw]
    card_iterator = iter(all_cards)
    hands = []
    for player in players:
        player_hand = list(islice(card_iterator, 0, int(player["n_cards"])))
        hands.append({"nickname": player['nickname'], "hand": player_hand})
    return hands


def arrange_players(players):
    """
        Order the human and AI players
        for optimal gameplay
    """
    num_total = len(players)
    num_ais = sum(1 for p in players if p.get("ai_agent"))
    offset = choice(range(num_total))

    ai_positions_from_zero = [floor(i * num_total / num_ais) for i in range(num_ais)]
    ai_positions = [(i + offset) % num_total for i in ai_positions_from_zero]
    ai_players = [p for p in players if p.get("ai_agent")]

    human_players = [p for p in players if not p.get("ai_agent")]
    shuffle(human_players)

    players = []

    for i in range(num_total):
        if i in ai_positions and ai_players:
            players.append(ai_players.pop(0))
        elif human_players:
            players.append(human_players.pop(0))

    return players

def create_game(n_agents, verbose=False):
    if n_agents < 2:
        raise ValueError("n_agents < 2")
    game_uuid = str(uuid.uuid4())
    players = [{"nickname": str(i), "n_cards": 1} for i in range(n_agents)]
    return {
        "game_uuid": game_uuid,
        "status": "Running",
        "round_number": 1,
        "max_cards": floor(24 / n_players) if len(players) > 2 else 11,
        "hands": draw_cards(players),
        "players": players,
        "cp_nickname": players[0]["nickname"],
        "history": []
    }


def get_player_by_nickname(players, nickname):
    filtered_players = [p for p in players if p["nickname"] == nickname]
    if filtered_players:
        return filtered_players[0]


def find_next_active_player(players, cp_nickname):
    active_players = [player for player in players if player["n_cards"] != 0 or player["nickname"] == cp_nickname]
    current_player_order = [i for i, player in enumerate(active_players) if player["nickname"] == cp_nickname][0]
    next_active_player = (active_players * 2)[current_player_order + 1]
    return next_active_player


def handle_check(game):
    cp_nickname = game["cp_nickname"]
    cards = [card for hand in game["hands"] for card in hand["hand"]]
    set_exists = determine_set_existence(cards, game["history"][-2]["action_id"])
    if set_exists:
        losing_player = get_player_by_nickname(game["players"], game["history"][-1]["player"])
    else:
        losing_player = get_player_by_nickname(game["players"], game["history"][-2]["player"])

    game["history"].append({"player": losing_player["nickname"], "action_id": 89})
    game["cp_nickname"] = None

    # Store the last round separately
    save(game)

    losing_player["n_cards"] += 1
    # If a player surpasses max cards, make them inactive (set their n_cards to 0) and either finish the game or set up next round
    if losing_player["n_cards"] > game["max_cards"]:
        losing_player["n_cards"] = 0
        # Check if game is finished
        if sum(p["n_cards"] > 0 for p in game["players"]) == 1:
            game["status"] = "Finished"
        else:
            # If the checking player was eliminated, figure out the next player
            # Otherwise the current player doesn't change
            if losing_player["nickname"] == cp_nickname:
                game["cp_nickname"] = find_next_active_player(game["players"], cp_nickname)["nickname"]
            else:
                game["cp_nickname"] = cp_nickname
    else:
        # If no one is kicked out, picking the next player is easier
        game["cp_nickname"] = losing_player["nickname"]

    game["round_number"] += 1
    game["history"] = []
    game["hands"] = draw_cards(game["players"])

    save(game)


def play(game, action_id, verbose=False):
    game["history"].append({"player": game["cp_nickname"], "action_id": action_id})

    if action_id != 88:
        move_name = INDEXATION[action_id]['set_type']
        if verbose:
            print(f"player {game['cp_nickname']} plays {move_name}")
        game["cp_nickname"] = find_next_active_player(game["players"], game["cp_nickname"])["nickname"]

    if action_id == 88:
        if verbose:
            print(f"player {game['cp_nickname']} checks")
        handle_check(game)
