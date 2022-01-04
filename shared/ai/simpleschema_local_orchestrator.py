from multiprocessing import Process
from copy import deepcopy
import shared.api.simpleschema_local_manager as game_manager
from conservative_ai.agent import ConservativeAgent
from time import time


def run_game(n_agents, verbose=False):
    game = game_manager.create_game(n_agents, verbose=verbose)
    while game.get("cp_nickname"):
        t1 = time()
        action = ConservativeAgent.determine_action(game)
        t2 = time()
        game_manager.play(game, action, verbose=verbose)
        t3 = time()
        if verbose:
            print(f"Agent: {t2-t1}; engine: {t3-t2}")
    print("Game finished")


def run_games(n_games, n_agents, verbose=False):
    for _ in range(n_games):
        run_game(n_agents, verbose=verbose)
