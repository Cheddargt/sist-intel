import sys
import os
import time

## Importa as classes que serao usadas
sys.path.append(os.path.join("pkg"))
from model import Model
from agentRnd import AgentRnd
from agentRescue import AgentRescue


## Metodo utilizado para permitir que o usuario construa o labirindo clicando em cima
def buildMaze(model):
    model.drawToBuild()
    step = model.getStep()
    while step == "build":
        model.drawToBuild()
        step = model.getStep()
    ## Atualiza o labirinto
    model.updateMaze()


def main():
    # Lê arquivo config.txt
    arq = open(os.path.join("config_data", "config.txt"), "r")
    configDict = {}
    for line in arq:
        ## O formato de cada linha é:var=valor
        ## As variáveis são
        ##  maxLin, maxCol que definem o tamanho do labirinto
        ## Tv e Ts: tempo limite para vasculhar e tempo para salvar
        ## Bv e Bs: bateria inicial disponível ao agente vasculhador e ao socorrista
        ## Ks :capacidade de carregar suprimentos em número de pacotes (somente para o ag. socorrista)

        values = line.split("=")
        configDict[values[0]] = int(values[1])

    print("dicionario config: ", configDict)

    # Cria o ambiente (modelo) = Labirinto com suas paredes
    mesh = "square"

    ## nome do arquivo de configuracao do ambiente - deve estar na pasta <proj>/config_data
    loadMaze = "ambiente"

    model = Model(configDict["maxLin"], configDict["maxCol"], mesh, loadMaze)
    buildMaze(model)

    model.maze.board.posAgent
    model.maze.board.posGoal
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    model.setAgentPos(model.maze.board.posAgent[0],
                      model.maze.board.posAgent[1])
    model.setGoalPos(model.maze.board.posGoal[0], model.maze.board.posGoal[1])
    model.draw()

    # Cria um agente vasculhador
    agent_vsc = AgentRnd(model, configDict)

    ###################### FOR DEBUG MODE ################################

    ## Ciclo de raciocínio do agente
    agent_vsc.deliberate()
    # added by zeni
    model.draw()
    time.sleep(0.01)
    while agent_vsc.deliberate() != -1:
        model.draw()
        time.sleep(0.01) # para dar tempo de visualizar as movimentacoes do agente no labirinto

    model.draw()

    agentVascKnowledge = agent_vsc.getKnowledge()

    # if len(agentVascKnowledge["foundVictims"]) == 0:
    #     print ("nenhuma vítima detectada")

    ####################### END DEBUG MODE #############################

    ####################### AGENTRSC DEBUG MODE ########################

    # agentVascKnowledge = {
    #     'visited': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
    #                 (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0),
    #                 (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0),
    #                 (20, 0), (21, 0), (22, 0), (23, 0), (24, 0), (24, 1),
    #                 (24, 2), (24, 3), (24, 4), (24, 5), (24, 6)],
    #     'knownWalls': [],
    #     'foundVictims': [(7, 0)]
    # }

    ####################### END DEBUG MODE #############################

    # Cria um agente salvador
    
    agent_rsc = AgentRescue(model, configDict, agentVascKnowledge)
    print('conhecimento do agt vasc: ', agentVascKnowledge)

    while agent_rsc.deliberate() != -1:
        model.draw()
        time.sleep(
            0.01
        )  # para dar tempo de visualizar as movimentacoes do agente no labirinto

    model.draw()

    # vetor de vítimas
    # vetor de paredes
    # vetor de posições
    # agent = AgentSvr()


if __name__ == '__main__':
    main()
