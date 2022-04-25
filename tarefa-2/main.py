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

    ###################### AGENTE VASCULHADOR ################################

    # # Cria um agente vasculhador
    # agent_vsc = AgentRnd(model, configDict)
    # ## Ciclo de raciocínio do agente
    # agent_vsc.deliberate()
    # # added by zeni
    # model.draw()
    # time.sleep(0.01)
    # while agent_vsc.deliberate() != -1:
    #     model.draw()
    #     time.sleep(
    #         0.01
    #     )  # para dar tempo de visualizar as movimentacoes do agente no labirinto

    # model.draw()

    # agentVascKnowledge = agent_vsc.getKnowledge()

    # if len(agentVascKnowledge["foundVictims"]) == 0:
    #     print("nenhuma vítima detectada")

    # print('conhecimento do agt vasc: ', agentVascKnowledge)

    ####################### END AGENTE VASCULHADOR #############################

    ####################### DEBUG TAREFA 2 ########################

    agentVascKnowledge = {
        'visited': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
                    (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0),
                    (13, 1), (13, 2), (13, 3), (12, 3), (12, 2), (12, 1),
                    (11, 1), (11, 2), (11, 3), (11, 4), (11, 5), (12, 5),
                    (13, 5), (14, 5), (15, 5), (15, 4), (15, 3), (15, 2),
                    (15, 1), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0),
                    (19, 1), (19, 2), (19, 3), (18, 1), (17, 1), (17, 2),
                    (17, 3), (17, 4), (17, 5), (18, 5), (19, 5), (19, 6),
                    (19, 7), (19, 8), (18, 6), (17, 6), (17, 7), (17, 8),
                    (16, 8), (16, 7), (16, 6), (16, 5), (16, 4), (16, 3),
                    (16, 2), (16, 1), (15, 6), (15, 7), (15, 8), (15, 9),
                    (16, 9), (16, 10), (17, 10), (17, 11), (17, 12), (18, 12),
                    (19, 12), (19, 11), (19, 10), (19, 13), (19, 14), (19, 15),
                    (19, 16), (19, 17), (19, 18), (19, 19), (18, 16), (18, 15),
                    (18, 14), (18, 13), (17, 13), (17, 14), (17, 15), (17, 16),
                    (17, 17), (16, 17), (16, 16), (16, 15), (16, 14), (16, 13),
                    (16, 12), (16, 11), (15, 11), (15, 10), (14, 10), (14, 9),
                    (14, 8), (14, 7), (14, 6), (13, 6), (13, 7), (13, 8),
                    (13, 9), (13, 10), (13, 11), (14, 11), (13, 12), (13, 13),
                    (13, 14), (14, 14), (13, 15), (13, 16), (14, 16), (15, 16),
                    (15, 17), (15, 18), (16, 18), (15, 19), (14, 19), (14, 18),
                    (14, 17), (13, 17), (13, 18), (13, 19), (12, 19), (12, 18),
                    (12, 17), (12, 16), (12, 15), (12, 14), (12, 13), (12, 12),
                    (12, 11), (12, 10), (12, 9), (12, 8), (12, 7), (12, 6),
                    (11, 6), (11, 7), (11, 8), (11, 9), (11, 10), (10, 9),
                    (10, 8), (10, 7), (10, 6), (10, 5), (10, 4), (10, 3),
                    (10, 2), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7),
                    (9, 8), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3),
                    (8, 2), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
                    (7, 8), (7, 9), (8, 9), (8, 10), (9, 10), (9, 11),
                    (10, 11), (10, 12), (11, 12), (11, 13), (11, 14), (11, 15),
                    (11, 16), (11, 17), (11, 18), (11, 19), (10, 19), (10, 18),
                    (10, 17), (10, 16), (10, 15), (10, 14), (10, 13), (9, 13),
                    (9, 12), (8, 12), (8, 11), (7, 11), (7, 12), (6, 12),
                    (6, 11), (6, 10), (5, 10), (5, 9), (4, 9), (4, 8), (3, 8),
                    (3, 7), (2, 7), (2, 6), (1, 6), (1, 5), (1, 4), (1, 3),
                    (2, 3), (2, 2), (2, 1), (3, 1), (4, 1), (5, 1), (5, 2),
                    (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (6, 7), (6, 8),
                    (4, 6), (4, 5), (4, 4), (4, 3), (4, 2), (3, 2), (3, 3),
                    (3, 4), (3, 5), (2, 4), (0, 3), (0, 2), (0, 1), (0, 4),
                    (0, 5), (0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11),
                    (6, 13), (6, 14), (6, 15), (7, 15), (7, 16), (8, 16),
                    (9, 16), (9, 17), (9, 18), (9, 19), (8, 19), (7, 19),
                    (6, 19), (5, 19), (4, 19), (4, 18), (4, 17), (4, 16),
                    (4, 15), (4, 14), (4, 13), (4, 12), (5, 13), (5, 14),
                    (5, 15), (5, 16), (6, 16), (6, 17), (7, 17), (8, 17),
                    (5, 17), (3, 13), (3, 14), (2, 14), (2, 15), (1, 15),
                    (3, 16), (3, 17), (3, 18), (3, 19), (2, 19), (2, 18),
                    (2, 17), (1, 17), (0, 17), (0, 18), (0, 19), (8, 14)],
        'knownWalls': [(14, 0), (14, 1), (14, 2), (14, 3), (13, 4), (12, 4),
                       (14, 4), (19, 4), (18, 3), (18, 2), (18, 4), (19, 9),
                       (18, 8), (18, 7), (17, 9), (18, 10), (18, 11), (18, 19),
                       (18, 18), (18, 17), (17, 18), (14, 12), (15, 12),
                       (14, 13), (15, 14), (14, 15), (15, 15), (15, 13),
                       (16, 19), (17, 19), (11, 11), (10, 10), (10, 1), (9, 1),
                       (9, 9), (8, 1), (7, 1), (7, 10), (7, 13), (6, 9),
                       (5, 8), (4, 7), (3, 6), (2, 5), (1, 2), (6, 1), (6, 2),
                       (6, 3), (6, 4), (6, 5), (6, 6), (1, 1), (0, 7), (1, 8),
                       (2, 9), (3, 10), (4, 11), (5, 12), (7, 14), (8, 15),
                       (9, 15), (8, 18), (7, 18), (6, 18), (5, 18), (3, 12),
                       (3, 15), (2, 13), (2, 16), (1, 14), (1, 16), (0, 15),
                       (1, 18), (0, 16), (1, 19), (8, 13), (9, 14)],
        'foundVictims': [{
            'pos': (13, 2),
            'sinVitais': 0.03,
            'difAcesso': 13.0
        }, {
            'pos': (11, 1),
            'sinVitais': 0.1,
            'difAcesso': 8.0
        }, {
            'pos': (13, 5),
            'sinVitais': 0.08,
            'difAcesso': 11.0
        }, {
            'pos': (18, 0),
            'sinVitais': 0.44,
            'difAcesso': 31.0
        }, {
            'pos': (16, 7),
            'sinVitais': 0.95,
            'difAcesso': 62.0
        }, {
            'pos': (16, 9),
            'sinVitais': 0.46,
            'difAcesso': 34.0
        }, {
            'pos': (17, 11),
            'sinVitais': 1.0,
            'difAcesso': 63.0
        }, {
            'pos': (18, 15),
            'sinVitais': 1.0,
            'difAcesso': 49.0
        }, {
            'pos': (16, 17),
            'sinVitais': 0.38,
            'difAcesso': 39.0
        }, {
            'pos': (16, 16),
            'sinVitais': 0.26,
            'difAcesso': 16.0
        }, {
            'pos': (16, 14),
            'sinVitais': 0.49,
            'difAcesso': 47.0
        }, {
            'pos': (16, 13),
            'sinVitais': 0.33,
            'difAcesso': 44.0
        }, {
            'pos': (14, 8),
            'sinVitais': 0.49,
            'difAcesso': 54.0
        }, {
            'pos': (14, 7),
            'sinVitais': 0.51,
            'difAcesso': 52.0
        }, {
            'pos': (13, 13),
            'sinVitais': 0.85,
            'difAcesso': 128.0
        }, {
            'pos': (13, 16),
            'sinVitais': 0.36,
            'difAcesso': 18.0
        }, {
            'pos': (14, 19),
            'sinVitais': 0.38,
            'difAcesso': 29.0
        }, {
            'pos': (13, 19),
            'sinVitais': 0.82,
            'difAcesso': 49.0
        }, {
            'pos': (12, 13),
            'sinVitais': 0.08,
            'difAcesso': 8.0
        }, {
            'pos': (12, 10),
            'sinVitais': 0.1,
            'difAcesso': 6.0
        }, {
            'pos': (10, 9),
            'sinVitais': 0.21,
            'difAcesso': 8.0
        }, {
            'pos': (10, 3),
            'sinVitais': 0.08,
            'difAcesso': 18.0
        }, {
            'pos': (8, 4),
            'sinVitais': 0.05,
            'difAcesso': 13.0
        }, {
            'pos': (7, 2),
            'sinVitais': 0.75,
            'difAcesso': 100.0
        }, {
            'pos': (7, 3),
            'sinVitais': 0.7,
            'difAcesso': 105.0
        }, {
            'pos': (7, 7),
            'sinVitais': 0.13,
            'difAcesso': 8.0
        }, {
            'pos': (10, 11),
            'sinVitais': 0.23,
            'difAcesso': 13.0
        }, {
            'pos': (10, 12),
            'sinVitais': 0.08,
            'difAcesso': 18.0
        }, {
            'pos': (11, 16),
            'sinVitais': 0.13,
            'difAcesso': 18.0
        }, {
            'pos': (10, 13),
            'sinVitais': 0.86,
            'difAcesso': 172.0
        }, {
            'pos': (1, 3),
            'sinVitais': 0.21,
            'difAcesso': 6.0
        }, {
            'pos': (5, 3),
            'sinVitais': 0.03,
            'difAcesso': 21.0
        }, {
            'pos': (4, 5),
            'sinVitais': 0.21,
            'difAcesso': 13.0
        }, {
            'pos': (0, 3),
            'sinVitais': 0.03,
            'difAcesso': 8.0
        }, {
            'pos': (0, 5),
            'sinVitais': 0.08,
            'difAcesso': 21.0
        }, {
            'pos': (3, 9),
            'sinVitais': 0.05,
            'difAcesso': 11.0
        }, {
            'pos': (5, 19),
            'sinVitais': 0.15,
            'difAcesso': 16.0
        }, {
            'pos': (4, 15),
            'sinVitais': 0.03,
            'difAcesso': 3.0
        }, {
            'pos': (4, 14),
            'sinVitais': 0.13,
            'difAcesso': 3.0
        }, {
            'pos': (2, 18),
            'sinVitais': 0.64,
            'difAcesso': 86.0
        }]
    }

    ####################### END DEBUG TAREFA 2 #############################

    # Cria um agente salvador

    agent_rsc = AgentRescue(model, configDict, agentVascKnowledge)

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
