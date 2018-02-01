"""
MyBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State, util
import random


class Bot:

    MAX_DEPTH = 1;

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        """
        Function that gets called every turn. This is where to implement the strategies.
        Be sure to make a legal move. Illegal moves, like giving an index of a card you
        don't own or proposing an illegal mariage, will lose you the game.
       	TODO: add some more explanation
        :param State state: An object representing the gamestate. This includes a link to
            the states of all the cards, the trick and the points.
        :return: A tuple of integers or a tuple of an integer and None,
            indicating a move; the first indicates the card played in the trick, the second a
            potential spouse.
        """

        # check which player I am so we can use this further up in our computions
        player = state.whose_turn()

        # All legal moves
        moves = state.moves()

        # set default move to random chosen move
        chosenMove = random.choice(moves)

        # holds the highest found score till some point, initialized with minus infinit
        # because we only want scores greater than -inf
        highestScore = float('-inf')
        allScores = []

        # maximum depth we want to let the recursion get to
        depth = self.MAX_DEPTH

        state = state.make_assumption() if state.get_phase() == 1 else state

        # check for all possible moves what their corresponding scores
        # will be following our heuristic
        
        for move in moves:
            
            nextState = state.next(move)
            score = self.computePossibleScoreRecursive(nextState, depth, player)
            allScores.append(score)

            if highestScore < score:
                highestScore = score
                chosenMove = move

        # return the move which leads to the highest 
        # score following from our heuristic evaluation
        return chosenMove


    def computePossibleScoreRecursive(self, state, depth, player):

        if state.finished():
            winner, points = state.winner()
            # print(winner, points, state.get_points(player), depth)
            if winner == player:
                return points
            else:
                return -points

        if depth == 0 or state.finished():
            return self.heuristic(state, player)

        depth = depth - 1

        newState = state.clone()
        moves = newState.moves()

        highestScore = 0
        chosenMove = None

        for move in moves:
            score = self.heuristic(newState, player) + self.computePossibleScoreRecursive(newState.next(move), depth, player)
            if score > highestScore:
                highestScore = score
                chosenMove = move

        return score


    #1 Your score divided by the total amount of earned points
    def heuristic(self, state, player):
        return util.ratio_points(state, player)

    # #2 Your score divided by opponents score
    # def heuristic(self, state, player):
    #     your = state.get_points(player)
    #     if player == 1:
    #         opponent = state.get_points(2)
    #     else:
    #         opponent = state.get_points(1)
    #     if opponent > 0 :
    #         return your / float(opponent)
    #     return your

    # #3 goal score minus your score
    # def heuristic(self, state, player):
    #     your = state.get_points(player)
    #     goal = 66
    #     return goal - float(your)

    # #4 goal score  opponents score
    # def heuristic(self, state, player):
    #     if player == 1:
    #         opponent = state.get_points(2)
    #     else:
    #         opponent = state.get_points(1)
    #     goal = 66
    #     return goal - float(opponent)



