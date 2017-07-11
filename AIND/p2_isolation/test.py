# test.py

import itertools
import random
import warnings

from collections import namedtuple

from isolation import Board
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3)
from tournament import play_matches,play_round,update
from time import time

NUM_MATCHES = 5  # number of matches against each opponent
TIME_LIMIT = 150  # number of milliseconds before timeout

Agent = namedtuple("Agent", ["player", "name"])

NUM_MATCHES = 1
t0 = time()
for i in range(NUM_MATCHES):
	#Agent1 = Agent(AlphaBetaPlayer(score_fn=open_move_score), "MM_Open")
	Agent1 = Agent(MinimaxPlayer(score_fn=open_move_score), "MM_Open")
	#Agent2 = Agent(RandomPlayer(), "Random")
	Agent2 = Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
	game = Board(Agent1.player, Agent2.player)

	# initialize all games with a random move and response
	for _ in range(2):
	    move = random.choice(game.get_legal_moves())
	    game.apply_move(move)
	#print(game.to_string())
	# play all games and tally the results
	winner, log, termination = game.play() # real thing happens here
	print(game.to_string())
	print("winner:",winner, "opponet failed due to", termination)
print("total time: ", time()-t0)