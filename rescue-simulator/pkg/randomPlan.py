from audioop import tostereo
from random import randint
import numpy as np

from matplotlib.style import available
from state import State

def euc_dist (a, b):
    return (np.sqrt((b[1]-a[1])*(b[1]-a[1]) + ((b[0]-a[0])*(b[0]-a[0]))))

class RandomPlan:
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
        self.returningPath = []
        self.remainingTime = 999999999
        self.lastPos = []

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

    def setVisitedPos(self, visited):
        self.visitedPos = visited

    def setLastPos(self, pos):
        self.lastPos = pos
    
    def updateCurrentState(self, state):
         self.currentState = state

    ## isso aqui não pode ser em agente, tem que ser no plano de retorno
    def calculateWayBack(self):
        available_path = self.visitedPos.copy()
        wayBackCost = 0

        best_path = []

        pos_aux = (self.currentState.row, self.currentState.col)
        ag_pos = (self.currentState.row, self.currentState.col)

        ## voltar pra base
        goal = (self.initialState.row, self.initialState.col)

        if (self.currentState.col == 21) and (self.currentState.row == 23):
            print("teste")
            
        if (self.currentState.row, self.currentState.col) != (0,0):

            while goal not in best_path:
                best_choice = ()
                smallest_dist = 99999999

                for pos in reversed(available_path):

                    # inicializar
                    if pos != pos_aux:

                        validPos = False

                        # cima baixo or direita ou esq
                        delta_x = abs(pos_aux[0] - pos[0])
                        delta_y = abs(pos_aux[1] - pos[1])

                        if delta_x == 1 and delta_y == 0:
                            validPos = True
                        elif delta_x == 0 and delta_y == 1:
                            # dir ou esq
                            validPos = True

                        dist = euc_dist(pos, goal)
                        if validPos and dist <= smallest_dist and pos != ag_pos and pos not in self.returningPath:
                            smallest_dist = dist
                            best_choice = pos

                # pos_aux = próximo "passo" do agente
                if best_choice != ():
                    pos_aux = best_choice
                    best_path.append(best_choice) 
                    wayBackCost+=1
                    available_path.remove(best_choice)
                        
        return [wayBackCost, best_path]

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

        possibilities = ["O", "S", "L", "N", "SE", "SO"]  
        backwards_possibilities = { "O" : "L",
                                    "S" : "N",
                                    "L" : "O",
                                    "N" : "S",
                                    "SE" : "NO",
                                    "SO" : "NE",
                                    "NE" : "SO",
                                    "NO" : "SE"}

        # ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]

        # if parede = adiciona a um vetor de paredes
        # if visitado = evitar

        # TODO: mover pra uma função tipo "goHome"
        backwardsMovePos = {
                (-1, 0) : "N",
                (1, 0) : "S",
                (0, 1) : "L", 
                (0, -1) : "O"}

        # TODO: consertar erro que tá fazendo o arquivo morrer

        if (self.currentState.row == 0 and self.currentState.col == 6):
            print("warning") 

        if self.lastPos == (self.currentState.row, self.currentState.col):
           self.chosenDir.remove(self.chosenDir[0])

        if len(self.returningPath) > 0:
            ## preciso disso
            next_dir = (self.returningPath[0][0] - self.currentState.row, self.returningPath[0][1] - self.currentState.col)
            ## preciso disso
            nextPos = backwardsMovePos[next_dir]
            ## preciso disso
            state = State(self.currentState.row + self.returningPath[0][0], self.currentState.col + self.returningPath[0][1])
            ## preciso disso
            self.returningPath.remove(self.returningPath[0])
            return [nextPos, state]

        # if (self.remainingTime < self.calculateWayBack()[0]+2):
        #     # if (self.currentState == self.initialState):
        #         # return [(-1, -1), self.currentState]
        #     print("hora de voltar -- sem tempo pra escanear!")
        #     self.returningPath = self.calculateWayBack()[1]
        #     next_dir = (self.returningPath[0][0] - self.currentState.row, self.returningPath[0][1] - self.currentState.col)
        #     nextPos = backwardsMovePos[next_dir]
        #     state = State(self.currentState.row + self.returningPath[0][0], self.currentState.col + self.returningPath[0][1])
        #     self.returningPath.remove(self.returningPath[0])
        #     return [nextPos, state]
            
        
        ## posição inicial pra saber o que começar fazendo
        result = self.selectNextPosition(possibilities[0])
        if self.isPossibleToMove(result[1]) == 1:
            self.chosenDir.insert(0, possibilities[0])
            return result

        if self.isPossibleToMove(result[1]) != 1:
            for pos in possibilities:
                result = self.selectNextPosition(pos)
                if self.isPossibleToMove(result[1]) == 1:
                    # if self.lastPos == (self.currentState.row, self.currentState.col):
                    #     self.chosenDir.remove(self.chosenDir[0])
                    self.chosenDir.insert(0, pos)
                    return result
                

        ## se não puder ir em nenhuma direção: provavelmente travou
        ## andar para trás
        for backwards_dir in self.chosenDir:
            result = self.selectNextPosition(backwards_possibilities[backwards_dir])
            if self.isPossibleToMove(result[1]) == -1:
                # remove a direção escolhida da lista de direções, começando pelo fim (pra remover a última)
                self.chosenDir.remove(backwards_dir)
                return result
        ## gastar uma energia
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
    
     


        
       
        
        
