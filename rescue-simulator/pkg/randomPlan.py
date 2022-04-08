from audioop import tostereo
from random import randint
from state import State

class RandomPlan:
    def __init__(self, maxRows, maxColumns, goal, initialState, name = "none", mesh = "square"):
        """
        Define as variaveis necessárias para a utilização do random plan por um unico agente.
        """
        self.walls = []
        self.visitedPos = []
        self.chosenDir = []
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.initialState = initialState
        self.currentState = initialState
        self.goalPos = goal
        self.actions = []

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
    
    def updateCurrentState(self, state):
         self.currentState = state

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
            if ((toState.row, toState.col)) not in self.agent.knownWalls:
                print("knownwalls: ", self.agent.knownWalls)

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
        # ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]

        # if parede = adiciona a um vetor de paredes
        # if visitado = evitar

        ## posição inicial pra saber o que começar fazendo
        result = self.selectNextPosition(possibilities[0])
        if self.isPossibleToMove(result[1]) == 1:
            self.chosenDir.append(possibilities[0])
            return result

        if self.isPossibleToMove(result[1]) != 1:
            for pos in possibilities:
                result = self.selectNextPosition(pos)
                if self.isPossibleToMove(result[1]) == 1:
                    self.chosenDir.append(pos)
                    return result

        ## se não puder ir em nenhuma direção: provavelmente travou
        ## andar para trás
        for backwards_dir in reversed(self.chosenDir):
            result = self.selectNextPosition(backwards_possibilities[backwards_dir])
            if self.isPossibleToMove(result[1]) == -1:
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
    
     


        
       
        
        
