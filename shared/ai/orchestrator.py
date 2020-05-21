from shared.api.game_manager import GameManager
from agent import ConservativeAgent


class Orchestrator(object):
    """Orchestrate games between agents."""

    def __init__(self, base_url=None):
        super(Orchestrator, self).__init__()
        # Test connection
        if base_url is not None:
            self.game_manager = GameManager(base_url)
        else:
            self.game_manager = GameManager()
        self.base_url = self.game_manager.base_url

    def orchestrate_single_game(self, n_agents=2):
        if not isinstance(n_agents, int) or n_agents not in range(1,9):
            raise ValueError("n_agents must be an integer from 1 to 8 (inclusive)")
        admin_agent = ConservativeAgent(base_url = self.base_url)
        nonadmin_agents = [ConservativeAgent(base_url = self.base_url) for i in range(n_agents - 1)]

        succeeded, game_uuid = self.game_manager.create_game()
        admin_agent.join_game(game_uuid, "admin_bot", run=False)
        for i, agent in enumerate(nonadmin_agents):
            agent.join_game(game_uuid, "bot_{}".format(i), run=False)
        print("Will start game?")
        admin_agent.start_game()
        print("Started game?")

        agents = nonadmin_agents + [admin_agent]
        self.run_single_game(agents)

    def run_single_game(self, agents):
        print("All agents finished the game")
