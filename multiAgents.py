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

    def replace_at_index1(tup, ix, val):
        lst = list(tup)
        lst[ix] = val
        return tuple(lst)

    def generatePath(self, playerindex, depth, state, numberOfAgents, prevState, action):
        print("  ")
        print(" ***** GENERATE PATH CALLED ****** ")
        print("  ")
        print(action, "THIS IS THE ACTION THAT WAS CALLED")
        currentLevel = depth # Begynner som 4
        legalActions = state.getLegalActions(playerindex) # ['Left', 'Center', 'Right']
        #print("LegalActions: {} for playerindex: {} in level: {}".format(legalActions,playerindex,depth))
        # **** Terminal node- Base case:
        #print("Legal action TRUE/FALSE? : {}".format(not legalActions))
#
        if state.isWin() or state.isLose() or currentLevel == 0:
            #score = self.evaluationFunction(prevState)
            score = scoreEvaluationFunction(state)
            t = (score, action)
            return t
           # print("this is the score from the basecase:  {} ".format(score))

            #return score  # Retruning the score of that terminal node

        # ******* Non-terminal node: Generate successors! *****
        # tuppel(score, action)

        # ****** Player is pacman, need to max! ******
        if playerindex == 0:
            # print("Pacman is making a decision in this level: {} ..... :".format(depth))
            bestScore = (-999999,'Blank')
            prevState = state #This is the state we are looking at actions from!
            for action in legalActions:
                # ***** Goes on to another state *****
                nextState = state.generateSuccessor(playerindex, action)
                # changing the playerIndex to a min player
                playerIndex = (playerindex + 1)
                #print (playerIndex, "DETTE ER PLAYERINDEX FRA MAX")

                t1 = (self.generatePath(playerIndex, currentLevel - 1, nextState, numberOfAgents, prevState, action))
                # This returns a value!
                print("PACMAN BEFORE CHOSEN: This is score t1: {}, this is score bestScore: {}".format(t1, bestScore))

                #bestScore = (bestScore[0], action)
                bestScore = self.maximum(bestScore, t1)

                print(bestScore, "Dette er best score!*************************")
                #print(bestScore[1], "Dette er bestScore[1")


                print("AFTER CHOSEN PACMAN : This is the chosen bestScore: {}".format(bestScore))
                # bestScore = (-999, 'Blank), t1 = (200,'Left')
                # Hvordan returnerer man den handlingen som horer til den beste verdien?
            # Send the highest value up in the tree:
            #print("SELECTED CHILD PACMAN: {}".format(bestScore))
            return bestScore
        else:
            # print("The ghost with this id: {} is making a decision in this level: {}...".format(playerindex,depth))
            bestScore = (9999999,'Blank')
            prevState = state
            for action in legalActions:
                nextState = state.generateSuccessor(playerindex,action)
                playerIndex = (playerindex + 1) % numberOfAgents
                #print (playerIndex, "DETTE ER PLAYERINDEX")
                print(action, currentLevel, "this is the action")
                t1 = (self.generatePath(playerIndex, currentLevel - 1, nextState, numberOfAgents, prevState, action))
                print(" GHOST BEFORE CHOSEN: This is score t1: {}, this is score bestScore: {}".format(t1, bestScore))
                bestScore = self.minimum(bestScore, t1)
                print("CHOSEN AFTER BESTSCORE GHOST: This is the chosen bestScore: {}".format(bestScore))
            print("SELECTED CHILD GHOST: {}".format(bestScore))
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
        #print(gameState.getLegalActions(0), "These are the legal actions!")
        # print "dintekst", gameState.getNumAgents()
        initialDepth = gameState.getNumAgents() * self.depth
        action = 'None'
        chosen = self.generatePath(0, initialDepth, startState, gameState.getNumAgents(), startState, action)
        #print (chosen[1], "Dette er svaret som returneres!")
        return chosen[1]
        #print("This is the final chosen touple: {}".format(chosen[1]))
        # print(chosen[1])
        # util.raiseNotDefined()



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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

