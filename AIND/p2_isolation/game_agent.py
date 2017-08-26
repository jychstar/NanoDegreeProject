"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(- opp_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(2*own_moves - opp_moves)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 2*opp_moves)



class IsolationPlayer:
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):

    def get_move(self, game, time_left):
        self.time_left = time_left
        self.best_move = (-1, -1) # declaration, default move to return 
        try:
            return self.minimax(game, self.search_depth)
        except SearchTimeout:  # Handle any actions required after timeout as needed
            # print("Search Time is up!")
            return self.best_move

    def checktimer(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.
        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        """
        moves = game.get_legal_moves()
        if not moves:
            return (-1, -1)  
        alpha = float("-inf")
        self.best_move = moves[0]
        for m in moves:
            self.checktimer()
            new_game = game.forecast_move(m)
            score0 = self.min_play(new_game,depth-1)
            if score0 > alpha:
                alpha = score0
                self.best_move = m
                #print("alpha:",alpha, ",score0:", score0, ", move:",m)
        return self.best_move

    def max_play(self,game,depth):
        if depth == 0:
            return self.score(game,self)
        moves = game.get_legal_moves()
        alpha = float("-inf")
        for m in moves:
            self.checktimer()
            new_game = game.forecast_move(m)
            score0 = self.min_play(new_game,depth-1)
            if score0 > alpha:
                alpha = score0
        return alpha        

    def min_play(self,game,depth):
        if depth == 0:
            return self.score(game,self)
        moves = game.get_legal_moves()
        beta = float("inf")
        for m in moves:
            self.checktimer()
            new_game = game.forecast_move(m)
            score0 = self.max_play(new_game,depth-1)
            if score0 < beta:
                beta = score0
        return beta   

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def checktimer(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.
        """
        self.time_left = time_left
        best_move = (-1, -1)

        # depth = self.search_depth
        depth = 1
        try:
            while (True):
                move = self.alphabeta(game, depth)
                if move != (-1, -1):
                    best_move = move
                #print("depth=",depth, " best move:", best_move)
                #if depth == 4: return best_move
                depth += 1
                if self.time_left() < self.TIMER_THRESHOLD:
                    return best_move

        except SearchTimeout:  # Handle any actions required after timeout as needed
            #print("Search Time is up!")
            return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        moves = game.get_legal_moves()
        moves.sort()
        #print(moves)
        if not moves:
            return (-1, -1)  
        
        best_move = moves[0]
        for m in moves:
            self.checktimer()
            new_game = game.forecast_move(m)
            score0 = self.min_play(new_game,depth-1,alpha,beta)
            #print("after min_play:",alpha,score0)
            if score0 > alpha:
                alpha = score0
                best_move = m
            #print("alpha:",alpha,",score0:", score0, ", move:",m)
        return best_move

    def max_play(self,game,depth, alpha, beta):
        #print("maxplay,", alpha,beta)
        if depth == 0:
            return self.score(game,self)
        moves = game.get_legal_moves()
        moves.sort()
        for m in moves:
            self.checktimer()
            new_game = game.forecast_move(m)
            score0 = self.min_play(new_game,depth-1,alpha,beta)
            if score0 > alpha:
                alpha = score0
                if alpha >= beta:
                    #print("max prune")
                    break
        return alpha       

    def min_play(self,game,depth,alpha,beta):
        #print("minplay", alpha,beta)
        if depth == 0:
            return self.score(game,self)
        moves = game.get_legal_moves()
        moves.sort()
        #print("  min level: moves ", moves)
        for m in moves:
            self.checktimer()
            new_game = game.forecast_move(m)
            score0 = self.max_play(new_game,depth-1,alpha,beta)
            #print("  min level: alpha/beta:",alpha, beta,",score0:", score0,", move:",m)
            if score0 < beta:
                beta = score0
                if beta <= alpha:
                    #print("min prune")
                    break
        return beta  
