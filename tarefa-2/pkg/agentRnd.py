## AGENTE RANDOM
### @Author: Luan Klein e Tacla (UTFPR)
### Agente que fixa um objetivo aleatório e anda aleatoriamente pelo labirinto até encontrá-lo.
### Executa raciocíni on-line: percebe --> [delibera] --> executa ação --> percebe --> ...
import sys
import os
import time

## Importa Classes necessarias para o funcionamento
from model import Model
from problem import Problem
from state import State
from random import randint

## Importa o algoritmo para o plano
from randomPlan import RandomPlan

##Importa o Planner
sys.path.append(os.path.join("pkg", "planner"))
from planner import Planner


## Classe que define o Agente
class AgentRnd:

    def __init__(self, model, configDict):
        """ 
        Construtor do agente random
        @param model referencia o ambiente onde o agente estah situado
        """

        self.model = model

        self.visited = []

        self.knownWalls = []

        self.foundVictims = []

        self.agentKnowledge = {}

        ## Obtem o tempo que tem para executar
        self.tv = configDict["Tv"]
        self.initialTime = configDict["Tv"]
        print("Tempo disponivel: ", self.tv)

        ## Pega o tipo de mesh, que está no model (influência na movimentação)
        self.mesh = self.model.mesh

        ## Cria a instância do problema na mente do agente (sao suas crencas)
        self.prob = Problem()
        self.prob.createMaze(model.rows, model.columns, model.maze)

        # O agente le sua posica no ambiente por meio do sensor
        initial = self.positionSensor()
        self.prob.defInitialState(initial.row, initial.col)
        print("*** Estado inicial do agente: ", self.prob.initialState)

        # Define o estado atual do agente = estado inicial
        self.currentState = self.prob.initialState

        # Define o estado objetivo:
        # definimos um estado objetivo aleatorio
        # self.prob.defGoalState(randint(0,model.rows-1), randint(0,model.columns-1))

        # definimos um estado objetivo que veio do arquivo ambiente.txt
        self.prob.defGoalState(model.maze.board.posGoal[0],
                               model.maze.board.posGoal[1])
        print("*** Objetivo do agente: ", self.prob.goalState)
        print("*** Total de vitimas existentes no ambiente: ",
              self.model.getNumberOfVictims())
        """
        DEFINE OS PLANOS DE EXECUÇÃO DO AGENTE
        """

        ## Custo da solução
        self.costAll = 0

        ## Cria a instancia do plano para se movimentar aleatoriamente no labirinto (sem nenhuma acao)
        self.plan = RandomPlan(model.rows, model.columns, self.prob.goalState,
                               initial, "goal", self.mesh)

        ## adicionar crencas sobre o estado do ambiente ao plano - neste exemplo, o agente faz uma copia do que existe no ambiente.
        ## Em situacoes de exploracao, o agente deve aprender em tempo de execucao onde estao as paredes
        self.plan.setWalls(model.maze.walls)

        ## Adiciona o(s) planos a biblioteca de planos do agente
        self.libPlan = [self.plan]

        ## inicializa acao do ciclo anterior com o estado esperado
        self.previousAction = "nop"  ## nenhuma (no operation)
        self.expectedState = self.currentState

    def getKnowledge(self):
        self.agentKnowledge = {
            'visited': self.visited,
            'knownWalls': self.knownWalls,
            'foundVictims': self.foundVictims
        }
        return self.agentKnowledge

    ## Metodo que define a deliberacao do agente
    def deliberate(self):
        print(f"libplan: ", self.libPlan)

        ## Verifica se há algum plano a ser executado
        if len(self.libPlan) == 0:
            return -1  ## fim da execucao do agente, acabaram os planos

        self.plan = self.libPlan[0]

        print("\n*** Inicio do ciclo raciocinio ***")
        print("Pos agente no amb.: ", self.positionSensor())

        ## Redefine o estado atual do agente de acordo com o resultado da execução da ação do ciclo anterior
        self.currentState = self.positionSensor()
        self.plan.updateCurrentState(
            self.currentState)  # atualiza o current state no plano
        print("Ag cre que esta em: ", self.currentState)

        ## Verifica se a execução do acao do ciclo anterior funcionou ou nao
        if not (self.currentState == self.expectedState):
            print("---> erro na execucao da acao ", self.previousAction,
                  ": esperava estar em ", self.expectedState,
                  ", mas estou em ", self.currentState)

        ## Funcionou ou nao, vou somar o custo da acao com o total
        self.costAll += self.prob.getActionCost(self.previousAction)
        print("Custo até o momento (com a ação escolhida):", self.costAll)

        ## consome o tempo gasto
        self.tv -= self.prob.getActionCost(self.previousAction)
        print("Tempo disponivel: ", self.tv)

        # passar o tempo remanescente para o plano decidir o que fazer
        self.plan.setRemainingTime(self.tv)

        ## TAREFA 1
        # if self.tv < self.initialTime and self.currentState.row == 0 and self.currentState.col == 0:
        #     print("!!! Voltou pra base !!!")
        #     print("Vítimas encontradas: ", self.foundVictims)
        #     print("Quantidade vítimas encontradas: ", len(self.foundVictims))
        #     print("Tempo de vasculhamento: ", self.initialTime - self.tv)

        #     del self.libPlan[0]  ## retira plano da biblioteca
        #     return -1
        # elif self.tv == 0 and self.currentState.row != 0 and self.currentState.col != 0:
        #     print("!!! Ag não conseguiu voltar pra base !!!")
        #     del self.libPlan[0]  ## retira plano da biblioteca
        #     return -1

        ## TAREFA 2
        if self.tv == 0:
            print("!!! Ag não conseguiu voltar pra base !!!")
            del self.libPlan[0]  ## retira plano da biblioteca
            return -1

        # ## Verifica se atingiu o estado objetivo
        # ## Poderia ser outra condição, como atingiu o custo máximo de operação
        # if self.prob.goalTest(self.currentState):
        #     print("!!! Objetivo atingido !!!")
        #     del self.libPlan[0]  ## retira plano da biblioteca

        ## Verifica se tem vitima na posicao atual
        victimId = self.victimPresenceSensor()

        if victimId == 42:
            print('warning')

        if victimId > 0:
            sinaisVitais = self.victimVitalSignalsSensor(victimId)[0]
            difAcesso = self.victimDiffOfAcessSensor(victimId)[0]
            print("vitima encontrada em ", self.currentState, " id: ",
                  victimId, " sinais vitais: ", sinaisVitais)
            print("vitima encontrada em ", self.currentState, " id: ",
                  victimId, " dif de acesso: ", difAcesso)

            vict = {
                "pos": (self.currentState.row, self.currentState.col),
                ##utilizando apenas o último elemento
                "sinVitais": sinaisVitais[-1],
                "difAcesso": difAcesso[-1]
            }

            if vict not in self.foundVictims:
                self.foundVictims.append(vict)

        ## Define a proxima acao a ser executada
        ## currentAction eh uma tupla na forma: <direcao>, <state>
        result = self.plan.chooseAction()
        print("Ag deliberou pela acao: ", result[0],
              " o estado resultado esperado é: ", result[1])

        ## Executa esse acao, atraves do metodo executeGo
        self.executeGo(result[0])
        self.previousAction = result[0]
        self.expectedState = result[1]

        time.sleep(0.01)

        return 1

    ## Metodo que executa as acoes
    def executeGo(self, action):
        """Atuador: solicita ao agente físico para executar a acao.
        @param direction: Direcao da acao do agente {"N", "S", ...}
        @return 1 caso movimentacao tenha sido executada corretamente """

        ## Passa a acao para o modelo
        result = self.model.go(action)

        ## added by zeni
        self.visited = self.model.visitedPos

        ## added by zeni
        ## não tá dando pra passar pra cá?
        self.knownWalls = self.model.knownWalls
        if len(self.knownWalls) > 0:
            print("walls: ", self.knownWalls)
            ## adicionar crencas sobre o estado do ambiente ao plano - apenas paredes conhecidas
            self.plan.setKnownWalls(self.knownWalls)

        self.plan.setVisitedPos(self.visited)

        self.plan.setLastPos((self.currentState.row, self.currentState.col))

        # print(f"Ag visitou: {self.visited}")

        ## Se o resultado for True, significa que a acao foi completada com sucesso, e ja pode ser removida do plano
        ## if (result[1]): ## atingiu objetivo ## TACLA 20220311
        ##    del self.plan[0]
        ##    self.actionDo((2,1), True)

    ## Metodo que pega a posicao real do agente no ambiente
    def positionSensor(self):
        """Simula um sensor que realiza a leitura do posição atual no ambiente.
        @return instancia da classe Estado que representa a posição atual do agente no labirinto."""
        pos = self.model.agentPos
        return State(pos[0], pos[1])

    def victimPresenceSensor(self):
        """Simula um sensor que realiza a deteccao de presenca de vitima na posicao onde o agente se encontra no ambiente
           @return retorna o id da vítima"""
        return self.model.isThereVictim()

    def victimVitalSignalsSensor(self, victimId):
        """Simula um sensor que realiza a leitura dos sinais da vitima 
        @param o id da vítima
        @return a lista de sinais vitais (ou uma lista vazia se não tem vítima com o id)"""
        return self.model.getVictimVitalSignals(victimId)

    def victimDiffOfAcessSensor(self, victimId):
        """Simula um sensor que realiza a leitura dos dados relativos à dificuldade de acesso a vítima
        @param o id da vítima
        @return a lista dos dados de dificuldade (ou uma lista vazia se não tem vítima com o id)"""
        return self.model.getDifficultyOfAcess(victimId)

    ## Metodo que atualiza a biblioteca de planos, de acordo com o estado atual do agente
    def updateLibPlan(self):
        for i in self.libPlan:
            i.updateCurrentState(self.currentState)

    def actionDo(self, posAction, action=True):
        self.model.do(posAction, action)
