from shared.api import game_manager
from shared.probabilities import handler


class Agent(object):
    """Autonomous AI Agent class to play Blef."""

    def __init__(self, base_url):
        super(Agent, self).__init__()
        self.nickname = "Honorable Gentleman"
        self.game_manager = game_manager.GameManager(base_url)
        self.prob_handler = handler.Handler()

    def join_game(self, game_uuid):
        """
            Join an existing game of Blef using GameManager.
            If successful, start playing the game.
        """
        succeeded, _ = self.game_manager.join_game(game_uuid, self.nickname)
        if succeeded:
            self.run()

    def run(self):
        """
            Play the game.
        """
        pass
