from audioop import tostereo
from random import randint
import numpy as np

from matplotlib.style import available
from urllib3 import ProxyManager
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

    def mutateSolution(self, solution, remainingTime):

        newSolution = solution.copy()

        possiblity = 0.01 # possibilidade de 4% de ocorrer

        for vict in newSolution:
            if randint(0, 100)/100 <= possiblity:
                if vict["gene"] == 0: vict["gene"] = 1
                if vict["gene"] == 1: vict["gene"] = 0

        # #TODO: alterar pra realizar o fitness
        # solution['fitness'] = self.fitnessFunction(solution['solution'], remainingTime)

        return solution

    def singlePointCrossover (self, parentA, parentB):

        firstChild = parentA.copy()
        firstChild.pop('fitness', None)
        firstChild.pop('fitnessNormalizado', None)

        secondChild = parentB.copy()
        secondChild.pop('fitness', None)
        secondChild.pop('fitnessNormalizado', None)

        crossoverPoint = randint (0, len(firstChild['solution'])-1)

        left_A = firstChild['solution'][:crossoverPoint] # guarda o pedaço de vetor parentA de crossoverPoint até o final
        right_A = firstChild['solution'][crossoverPoint:] # guarda o pedaço de vetor parentA de crossoverPoint até o final
        left_B = secondChild['solution'][:crossoverPoint] # guarda o pedaço de vetor parentB de crossoverPoint até o final
        right_B = secondChild['solution'][crossoverPoint:] # guarda o pedaço de vetor parentB de crossoverPoint até o final

        firstChild['solution'] = left_A + right_A
        secondChild['solution'] = left_B + right_B

        return [firstChild, secondChild]

    def createSolutionArray (self, victArray):
        
        for vict in victArray:
            vict['gene'] = 0

        return victArray
        
    def createFirstGeneration (self, victArray, NUM_SOLUCOES, remainingTime):

        emptyArray = {}
        emptyArray['solution'] = victArray.copy()

        # probabilidade de ser solução ou não -- apenas para inicialização!!
        solutProbability = 0.3

        firstGen = []


        for i in range(NUM_SOLUCOES):
            emptyArray = {}
            emptyArray['solution'] = victArray.copy()
            for vict in emptyArray['solution']:
                if randint(0, 100)/100 <= solutProbability:
                    vict['gene'] = 1
                else:   
                    vict['gene'] = 0
            emptyArray['fitness'] = self.fitnessFunction(emptyArray['solution'], remainingTime)
            firstGen.append(emptyArray)

        return firstGen

    def fitnessFunction (self, solution, remainingTime):

        gravidadeAcumulada = 0;
        tempoAcumulado = 0;

        for vict in solution:
            if vict['gene'] == 1:
                gravidadeAcumulada += vict['sinVitais']
                tempoAcumulado += vict['difAcesso']

        if tempoAcumulado > remainingTime:
            gravidadeAcumulada = 0;

        return gravidadeAcumulada

    def elitismSelection (self, geracao):

        # inicializar com soluções quaisquer
        bestSolution = {}
        bestSolution['fitness'] = 0
        secondBestSolution = {}
        secondBestSolution['fitness'] = 0


        # find best solution
        for solution in geracao:
            if solution['fitness'] > bestSolution['fitness']:
                bestSolution = solution 

        # find second best solution
        for solution in geracao:
            if solution['fitness'] > secondBestSolution['fitness'] and solution != bestSolution:
                secondBestSolution = solution

        return [bestSolution, secondBestSolution]

    def rwheelSelection (self, currentGeracao, remainingTime):

        currentGen = currentGeracao.copy()

        fitnessAcumulado = 0

        for solution in currentGen:
            fitnessAcumulado += solution['fitness']


        for solution in currentGen:
            if solution['fitness'] != 0:
                solution['fitnessNormalizado'] = solution['fitness']/fitnessAcumulado
            else:
                solution['fitnessNormalizado'] = 0
        
        selectedParents = []

        while len(selectedParents) < 2:
            selectedChance = randint(0, 100)/100
            fitnessNormalizadoAcumulado = 0
            for solution in currentGen:
                if solution['fitnessNormalizado'] >= selectedChance and solution not in selectedParents:
                    selectedParents.append(solution)
                    break
                fitnessNormalizadoAcumulado += solution['fitnessNormalizado']

        resultingChildren = self.singlePointCrossover(selectedParents[0], selectedParents[1])

        resultingChildren[0]['fitness'] = self.fitnessFunction(resultingChildren[0]['solution'], remainingTime)
        resultingChildren[1]['fitness'] = self.fitnessFunction(selectedParents[0]['solution'], remainingTime)

        return resultingChildren

    def createRescuePlan(self):
        agPosition = (self.initialState.row, self.initialState.col)
        basePos = (self.initialState.row, self.initialState.col)
        remainingTime = self.remainingTime
        NUM_GERACOES = 10 # número de gerações
        NUM_SOLUCOES = 10 # número de soluções por geração - vetor de vítimas
        primeiraGeracao = []
        currentGeracao = []
        proximaGeracao = []

        ## inicializa um vetor de soluções neutro (todas as vítimas possuem gene = 0)
        primeiraGeracao = self.createFirstGeneration(self.foundVictims, NUM_SOLUCOES, remainingTime)
        currentGeracao = primeiraGeracao

        ## imprimir geração
        print("GEN # 1: gAcumulado = ", end=""),



        for solution in primeiraGeracao:
            if solution['fitness'] != 0:
                print(str(round(solution['fitness'], 2)), " ", end="")

        print("GEN # 1: tGasto = ", end=""),

        for solution in primeiraGeracao:
            tempoacumulado = 0
            for vict in solution['solution']:
                if vict['gene'] == 1:
                    tempoacumulado += vict['difAcesso']
            print(tempoacumulado, " ", end="")
        
        print("")
        print(" ------------- ")
        
        for i in range(NUM_GERACOES-1):     # -1 pra considerar a primeira geração já criada
                # carrega os 2 melhores pra próxima geração
                elitismCarryOver = self.elitismSelection(currentGeracao)
                proximaGeracao = elitismCarryOver

                while len(proximaGeracao) < NUM_SOLUCOES:

                    filhos = self.rwheelSelection(currentGeracao, remainingTime)
                    proximaGeracao += filhos

                ## realizar mutação

                # for solution in proximaGeracao:
                #     solution['solution'] = self.mutateSolution(solution['solution'], remainingTime)
                    

                # TODO: realizar fitness pós mutação
                
                ## imprimir geração
                print("GEN #", i+2 ,": gAcumulado = ", end=""),

                for solution in proximaGeracao:
                    if solution['fitness'] != 0:
                        print(str(round(solution['fitness'], 2)), " ", end="")

                print("")

                print("tGasto = ", end=""),

                for solution in primeiraGeracao:
                    tempoacumulado = 0
                    for vict in solution['solution']:
                        if vict['gene'] == 1:
                            tempoacumulado += vict['difAcesso']
                    print(tempoacumulado, " ", end="")
                
                print("")
                print(" ------------- ")

                currentGeracao = proximaGeracao
                proximaGeracao = []

                # proxima geracao
                print("")

        best_fitness = currentGeracao[0]['fitness']
        best_solution = currentGeracao[0]

        for solution in currentGeracao:
            if solution['fitness'] > best_fitness:
                best_fitness = solution['fitness']
                best_solution = solution

        VictSalvas = 0 #Vs
        ts = 0  #ts
        victTotal = len(self.foundVictims) #V
        gravidadeAcumulada = 0 #G
        VictSalvasPorTempo = 0


        for vict in best_solution['solution']:
            if vict['gene'] == 1:
                VictSalvas += 1
                ts += vict['difAcesso']
                gravidadeAcumulada += vict['sinVitais']

        if (ts != 0):
            VictSalvasPorTempo = VictSalvas/ts #S

        print("Vs = ", VictSalvas)
        print("ts = ", ts)
        print("V = ", victTotal)
        print("G = ", gravidadeAcumulada)
        print("S = ", VictSalvasPorTempo)
        print("")

        # inicializa primeira geração
        # for i in NUM_SOLUCOES:


       
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
    
     


        
       
        
        
