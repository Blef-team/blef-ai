from time import sleep
from shared.api import game_manager
from shared.probabilities import handler


class Agent(object):
    """Autonomous AI Agent class to play Blef."""

    def __init__(self, base_url=None):
        super(Agent, self).__init__()
        self.nickname = "Honorable_Gentleman"
        if base_url is not None:
            self.game_manager = game_manager.GameManager(base_url)
        else:
            self.game_manager = game_manager.GameManager()
        self.prob_handler = handler.Handler()

    def join_game(self, game_uuid, nickname=None):
        """
            Join an existing game of Blef using GameManager.
            If successful, start playing the game.
            return: succeeded(bool)
        """
        if isinstance(nickname, str) and len(nickname) > 0:
            self.nickname = nickname
        succeeded, _ = self.game_manager.join_game(game_uuid, self.nickname)
        if succeeded:
            return self.run()
        return False

    def run(self):
        """
            Play the game.
        """
        done = False
        while not done:
            sleep(1) # DEBUG / DEV
            succeeded, game_state = self.game_manager.get_game_state()
            if not succeeded:
                print("Can't get the game state.")
                continue
            if game_state.get("status") != "Running":
                if game_state.get("status") != "Finished":
                    print("Game not yet started")
                else:
                    print("Game finished")
                    break
                continue
            if game_state.get("cp_nickname") != self.nickname:
                print("It's not my turn")
                continue
            matching_hands = [hand for hand in game_state.get("hands", []) if hand.get("nickname") == self.nickname]
            if len(matching_hands) != 1:
                print("Can't get my hand from the game state.")
                continue
            hand = [(card["value"], card["colour"]) for card in matching_hands[0]["hand"]]
            players = game_state.get("players", [])
            others_card_num = sum([player.get("n_cards") for player in players if player.get("nickname", self.nickname) != self.nickname])
            if not players or not others_card_num:
                print("Can't get my hand or other player's card numbers from the game state.")
                continue
            print("Here's my move")
