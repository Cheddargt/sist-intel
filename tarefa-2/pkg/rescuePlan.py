from audioop import tostereo
from random import randint
import numpy as np

from matplotlib.style import available
from state import State

def euc_dist (a, b):
    return (np.sqrt((b[1]-a[1])*(b[1]-a[1]) + ((b[0]-a[0])*(b[0]-a[0]))))

class RescuePlan:
    def __init__(self, maxRows, maxColumns, goal, initialState, name = "none", mesh = "square"):
        """
        Define as variaveis necessárias para a utilização do random plan por um unico agente.
        """
        self.walls = []
        self.knownWalls = []
        self.visitedPos = [(initialState.row, initialState.col)]
        self.chosenDir = []
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.initialState = initialState
        self.currentState = initialState
        self.goalPos = goal
        self.actions = []
        self.agentPath = []
        self.remainingTime = 999999999

        #availablePath
        self.availablePath = []

        #knownWalls
        self.knownWalls = []

        #foundVictims
        self.foundVictims = []
        self.savedVictims = []


    def setWalls(self, walls):
        row = 0
        col = 0
        for i in walls:
            col = 0
            for j in i:
                if j == 1:
                    self.walls.append((row, col))
                col += 1
            row += 1

    def setKnownWalls(self, kn_walls):
        # deveria: fazer append
        # estou: substituindo tudo
        self.knownWalls = kn_walls

    def setRemainingTime(self, time):
        self.remainingTime = time

    def setKnowledge(self, knowledge):
        self.availablePath = knowledge["visited"]
        self.knownWalls = knowledge["knownWalls"]
        self.foundVictims = knowledge["foundVictims"]
    
    def updateCurrentState(self, state):
         self.currentState = state

    def mutateSolution(self, solution):

        possiblity = 0.04

        for vict in solution:
            if randint(0, 100)/100 <= possiblity:
                if vict["gene"] == 0: vict["gene"] = 1
                if vict["gene"] == 1: vict["gene"] = 0

        return solution

    def createRescuePlan(self):
        ## inicializa na posição inicial, NÃO atualiza em tempo real (offline)
        agPosition = (self.initialState.row, self.initialState.col)
        ## posição da base
        basePos = (self.initialState.row, self.initialState.col)
        ## vitima mais proxima, distancia à vitima mais proxima, custo à vitima mais próxima
        # inicializa com uma vítima qualquer
        closestVict = self.foundVictims[0]
        closestVictDist = 9999999999
        closestVictCost = 9999999999
        ## melhor caminho atual
        currentBestPath = []
        ## tempo disponível
        remaniningTime = self.remainingTime

        closestVict = self.foundVictims[0]

        ## define vítima mais próxima/de menor custo
        for vict in self.foundVictims:
            victPos = vict['pos']
            victAccTime = vict["difAcesso"]
            victSinVital = vict["sinVitais"]
            ## calcula distância atual do agente até a vítima
            dist = euc_dist(agPosition, vict_pos)

            if victCost < closestVictCost and self.remainingTime > closestVictCost + returnCost:
                closestVict = vict_pos 
                closestVictDist = dist
                closestVictCost = victCost
        
            # ## calcula a melhor rota e o custo até essa vítima
            # victCost = self.calculatePathToGoal(agPosition, closestVict)[0]
            victPath = self.calculatePathToGoal(agPosition, closestVict)[1]

            ## atualiza posição do agente para a da vítima escolhida
            agPosition = closestVict

            ## remove a vítima da lista de self.foundVictims
            self.savedVictims.append(closestVict)
            self.foundVictims.remove(closestVict)
            self.agentPath+=victPath

        backToBase = self.calculatePathToGoal(agPosition, basePos)[1]
        self.agentPath+=backToBase
        print(self.agentPath)

    def isPossibleToMove(self, toState):
        """Verifica se eh possivel ir da posicao atual para o estado (lin, col) considerando 
        a posicao das paredes do labirinto e movimentos na diagonal
        @param toState: instancia da classe State - um par (lin, col) - que aqui indica a posicao futura 
        @return: True quando é possivel ir do estado atual para o estado futuro """

        ## vai para fora do labirinto
        if (toState.col < 0 or toState.row < 0):
            return 0

        ## vai para fora do labirinto
        if (toState.col >= self.maxColumns or toState.row >= self.maxRows):
            return 0

        ## vai para uma posição que já foi
        if (toState.row, toState.col) in self.visitedPos:
            return -1
      
        # ## vai para cima de uma parede
        # ## aqui é que descobre uma parede nova
        if (toState.row, toState.col) in self.walls:
            # TODO: como que eu acesso knownWalls (linha 34 de agentRnd) aqui? Passo por parâmetro?
            ## preciso saber pra não perder energia tentando ir para paredes que o agente já conhece
            # R: uma função chamada setKnownWalls chamada na linha 180 de agentRnd
            if ((toState.row, toState.col)) in self.knownWalls:
                return 0

        # vai na diagonal? Caso sim, nao pode ter paredes acima & dir. ou acima & esq. ou abaixo & dir. ou abaixo & esq.
        delta_row = toState.row - self.currentState.row
        delta_col = toState.col - self.currentState.col

        ## o movimento eh na diagonal
        ## só pode realizar movimento na diagonal com base em knownWals, ou seja, já tendo visitado aquelas duas posições
        ## e verificando knownWalls para verificar se já colidiu com paredes ali.
        ##
        ##  só seria útil no retorno (porque no vasculhamento seria inútil)
        # if (delta_row !=0 and delta_col != 0):
        #     if (self.currentState.row + delta_row, self.currentState.col) in self.walls and (self.currentState.row, self.currentState.col + delta_col) in self.walls:
        #         return False
        
        self.visitedPos.append((toState.row, toState.col))
        return 1

    def selectNextPosition(self, dir):
         """ Sorteia uma direcao e calcula a posicao futura do agente 
         @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """
         movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1),
                    "NE" : (-1, 1),
                    "NO" : (-1, -1),
                    "SE" : (1, 1),
                    "SO" : (1, -1)}

         state = State(self.currentState.row + movePos[dir][0], self.currentState.col + movePos[dir][1])
         return dir, state

    def chooseAction(self):
        """ Escolhe o proximo movimento de forma aleatoria. 
        Eh a acao que vai ser executada pelo agente. 
        @return: tupla contendo a acao (direcao) e uma instância da classe State que representa a posição esperada após a execução
        """

        possibilities = ["O", "S", "L", "N"]  
        backwards_possibilities = { "O" : "L",
                                    "S" : "N",
                                    "L" : "O",
                                    "N" : "S"}

        # TODO: mover pra uma função tipo "goHome"
        backwardsMovePos = {
                (-1, 0) : "N",
                (1, 0) : "S",
                (0, 1) : "L", 
                (0, -1) : "O"}

         

        if len(self.agentPath) > 0:

            ## preciso disso
            next_dir = (self.agentPath[0][0] - self.currentState.row, self.agentPath[0][1] - self.currentState.col)
            ## preciso disso
            nextPos = backwardsMovePos[next_dir]
            ## preciso disso
            state = State(self.currentState.row + self.agentPath[0][0], self.currentState.col + self.agentPath[0][1])
            ## preciso disso
            self.agentPath.remove(self.agentPath[0])
            return [nextPos, state]

        if len(self.foundVictims) == 0:
            print ("vítimas salvas: ", len(self.savedVictims))
            return [-1, -1]
            
        ## tentar de novo

        # ## enquanto for possível se mover
        # if not self.isPossibleToMove(result[1]):
        #     result = self.selectNextPosition("SE")
        #     ## enquanto for possível se mover
        #     if not self.isPossibleToMove(result[1]):
        #         result = self.selectNextPosition("L")
        #         ## enquanto for possível se mover
        #         if not self.isPossibleToMove(result[1]):
        #             result = self.selectNextPosition("N")
        #             ## enquanto for possível se mover
        #             if not self.isPossibleToMove(result[1]):
        #                 result = self.selectNextPosition("O")

        # return result

    def do(self):
        """
        Método utilizado para o polimorfismo dos planos

        Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
        """
        nextMove = self.move()
        return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))   
    
     


        
       
        
        
