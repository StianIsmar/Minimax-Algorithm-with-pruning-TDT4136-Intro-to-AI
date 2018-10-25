# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def maximum(self, touple1, touple2): # (14, 'LEFT'), (20,'RIGHT')
        t1 = touple1[0]
        t2 = touple2[0]
        # First touple
        if isinstance(t1, tuple):
            if isinstance(t2, tuple):
                # both tuple
                if touple1[0][0] > touple2[0][0]:
                    return touple1
                else:
                    return touple2
            if touple1[0][0] > touple2[0]:
                return touple1
            else:
                return touple2
        else:
            if isinstance(t2, tuple):
                #print("DETTE CASET VI HAR ______________________________________________________")
                if touple1[0] > touple2[0][0]:
                    return touple1
                else:
                    return touple2
            else:
                if touple1[0] > touple2[0]:
                    return touple1
                else:
                    return touple2

    def minimum(self, touple1, touple2): # (14, 'LEFT'), (20,'RIGHT')
        t1 = touple1[0]
        t2 = touple2[0]
        # First touple
        if isinstance(t1, tuple):
            if isinstance(t2, tuple):
                # both tuple
                if touple1[0][0] < touple2[0][0]:
                    return touple1
                else:
                    return touple2
            if touple1[0][0] < touple2[0]:
                return touple1
            else:
                return touple2
        else:
            if isinstance(t2, tuple):
                if touple1[0] < touple2[0][0]:
                    return touple1
                else:
                    return touple2
            else:
                if touple1[0] < touple2[0]:
                    return touple1
                else:
                    return touple2

    def generatePath(self, playerindex, depth, state, numberOfAgents, action):
        currentLevel = depth
        legalActions = state.getLegalActions(playerindex)
        if state.isWin() or state.isLose() or currentLevel == 0:
            score = scoreEvaluationFunction(state)
            t = (score, action)
            return t
        # ****** Player is pacman, need to max! ******
        if playerindex == 0:
            # print("Pacman is making a decision in this level: {} ..... :".format(depth))
            bestScore = (-999999,'Blank')
            for action in legalActions:
                # ***** Goes on to another state *****
                nextState = state.generateSuccessor(playerindex, action)
                # changing the playerIndex to a min player
                playerIndex = (playerindex + 1)
                t1 = (self.generatePath(playerIndex, currentLevel - 1, nextState, numberOfAgents, action))
                t1 = (t1[0], action)
                # print("PACMAN BEFORE CHOSEN: This is score t1: {}, this is score bestScore: {}".format(t1, bestScore))
                bestScore = self.maximum(bestScore, t1)
                # print("AFTER CHOSEN PACMAN : This is the chosen bestScore: {}".format(bestScore))
            #print("SELECTED CHILD PACMAN: {}".format(bestScore))
            return bestScore
        else:
            # print("The ghost with this id: {} is making a decision in this level: {}...".format(playerindex,depth))
            bestScore = (9999999,'Blank')
            for action in legalActions:
                nextState = state.generateSuccessor(playerindex,action)
                playerIndex = (playerindex + 1) % numberOfAgents
                t1 = (self.generatePath(playerIndex, currentLevel - 1, nextState, numberOfAgents, action))
                t1 = (t1[0], action)
                # print(" GHOST BEFORE CHOSEN: This is score t1: {}, this is score bestScore: {}".format(t1, bestScore))
                bestScore = self.minimum(bestScore, t1)
                # print("CHOSEN AFTER BESTSCORE GHOST: This is the chosen bestScore: {}".format(bestScore))
            # print("SELECTED CHILD GHOST: {}".format(bestScore))
            return bestScore

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        playerIndexes = list(range(gameState.getNumAgents()))
        startState = gameState
        initialDepth = gameState.getNumAgents() * self.depth
        action = 'None'
        chosen = self.generatePath(0, initialDepth, startState, gameState.getNumAgents(), action)
        return chosen[1]
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def maximumPrune(self, touple1, touple2):  # (14, 'LEFT'), (20,'RIGHT')
        t1 = touple1[0]
        t2 = touple2[0]
        # First touple
        if isinstance(t1, tuple):
            if isinstance(t2, tuple):
                # both tuple
                if touple1[0][0] > touple2[0][0]:
                    return touple1
                else:
                    return touple2
            if touple1[0][0] > touple2[0]:
                return touple1
            else:
                return touple2
        else:
            if isinstance(t2, tuple):
                # print("DETTE CASET VI HAR ______________________________________________________")
                if touple1[0] > touple2[0][0]:
                    return touple1
                else:
                    return touple2
            else:
                if touple1[0] > touple2[0]:
                    return touple1
                else:
                    return touple2

    def minimumPrune(self, touple1, touple2):  # (14, 'LEFT'), (20,'RIGHT')
        t1 = touple1[0]
        t2 = touple2[0]
        # First touple
        if isinstance(t1, tuple):
            if isinstance(t2, tuple):
                # both tuple
                if touple1[0][0] < touple2[0][0]:
                    return touple1
                else:
                    return touple2
            if touple1[0][0] < touple2[0]:
                return touple1
            else:
                return touple2
        else:
            if isinstance(t2, tuple):
                if touple1[0] < touple2[0][0]:
                    return touple1
                else:
                    return touple2
            else:
                if touple1[0] < touple2[0]:
                    return touple1
                else:
                    return touple2

    def generatePathAlphaBeta(self, playerindex, depth, state, numberOfAgents, action, alpha, beta):
        currentLevel = depth
        legalActions = state.getLegalActions(playerindex)
        if state.isWin() or state.isLose() or currentLevel == 0:
            score = scoreEvaluationFunction(state)
            t = (score, action)
            return t
        # ****** Player is pacman, need to max! ******
        if playerindex == 0:
            # print("Pacman is making a decision in this level: {} ..... :".format(depth))
            bestScore = (-999999, 'Blank')
            for action in legalActions:
                # ***** Goes on to another state *****
                nextState = state.generateSuccessor(playerindex, action)
                # changing the playerIndex to a min player
                playerIndex = (playerindex + 1)
                t1 = (self.generatePathAlphaBeta(playerIndex, currentLevel - 1, nextState, numberOfAgents, action, alpha, beta))
                t1 = (t1[0], action)
                # print("PACMAN BEFORE CHOSEN: This is score t1: {}, this is score bestScore: {}".format(t1, bestScore))
                bestScore = self.maximumPrune(bestScore, t1)
                alpha = self.maximumPrune(alpha, bestScore)
                if beta < alpha:
                    break
                # print("AFTER CHOSEN PACMAN : This is the chosen bestScore: {}".format(bestScore))
            # print("SELECTED CHILD PACMAN: {}".format(bestScore))
            return bestScore
        else:
            # print("The ghost with this id: {} is making a decision in this level: {}...".format(playerindex,depth))
            bestScore = (9999999, 'Blank')
            for action in legalActions:
                nextState = state.generateSuccessor(playerindex, action)
                playerIndex = (playerindex + 1) % numberOfAgents
                t1 = (self.generatePathAlphaBeta(playerIndex, currentLevel - 1, nextState, numberOfAgents, action, alpha, beta))
                t1 = (t1[0], action)
                # print(" GHOST BEFORE CHOSEN: This is score t1: {}, this is score bestScore: {}".format(t1, bestScore))
                bestScore = self.minimumPrune(bestScore, t1)
                beta = self.minimumPrune(beta,bestScore)
                if beta < alpha:
                    break
                # print("CHOSEN AFTER BESTSCORE GHOST: This is the chosen bestScore: {}".format(bestScore))
            # print("SELECTED CHILD GHOST: {}".format(bestScore))
            return bestScore
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        playerIndexes = list(range(gameState.getNumAgents()))
        startState = gameState
        initialDepth = gameState.getNumAgents() * self.depth
        action = 'None'
        alpha = (-888888, 'blank')
        beta = (888888,'blank')
        chosen = self.generatePathAlphaBeta(0, initialDepth, startState, gameState.getNumAgents(), action, alpha, beta)
        return chosen[1]
        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

