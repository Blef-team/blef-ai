from shared.api import game_manager
from shared.probabilities import handler


class Agent(object):
    """Bass/parent class for AI agents to play Blef."""

    def __init__(self, base_url=None):
        super(Agent, self).__init__()
        self.nickname = "Anonymous Intelligence"  # Overwrite this in a child class
        if base_url is not None:
            self.game_manager = game_manager.GameManager(base_url)
        else:
            self.game_manager = game_manager.GameManager()
        self.prob_handler = handler.Handler()

    def join_game(self, game_uuid, nickname=None, run=True):
        """
            Join an existing game of Blef using GameManager.
            If successful, start playing the game.
            return: succeeded(bool)
        """
        if isinstance(nickname, str) and len(nickname) > 0:
            self.nickname = nickname
        succeeded, _ = self.game_manager.join_game(game_uuid, self.nickname)
        if not run:
            return succeeded
        if succeeded:
            return self.run()
        return False

    def run(self):
        """
            Stub function - overwrite in a child class
        """
        print("There's no gameplay logic implemented in the AI agent!")
        return False
