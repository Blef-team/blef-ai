import random
from time import sleep
from multiprocessing import Process
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

    def orchestrate_games(self, n_games=0, n_agents=0):
        for i in range(n_games):
            n_agents = n_agents if n_agents else random.choice(range(2,9))
            self.orchestrate_single_game(n_agents=n_agents)

    def orchestrate_single_game(self, n_agents=2):
        if not isinstance(n_agents, int) or n_agents not in range(1,9):
            raise ValueError("n_agents must be an integer from 1 to 8 (inclusive)")
        admin_agent = ConservativeAgent(base_url=self.base_url)
        nonadmin_agents = [ConservativeAgent(base_url=self.base_url) for i in range(n_agents - 1)]

        succeeded, game_uuid = self.game_manager.create_game()
        admin_agent.join_game(game_uuid, "admin_bot", run=False)
        for i, agent in enumerate(nonadmin_agents):
            agent.join_game(game_uuid, "bot_{}".format(i), run=False)
        admin_agent.start_game()

        agents = nonadmin_agents + [admin_agent]
        self.run_single_game(agents)

    def run_single_game(self, agents):
        agent_jobs = []
        for agent in agents:
            p = Process(target=agent.run)
            agent_jobs.append(p)
            p.start()
        done = False
        while not done:
            for agent_job in agent_jobs:
                agent_job.join(timeout=0.1)
                if agent_job.is_alive():
                    sleep(0.1)
                    break
            else:
                done = True
        print("All agents finished the game")
