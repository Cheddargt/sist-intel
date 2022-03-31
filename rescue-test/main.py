from asyncio.windows_events import INFINITE
import sys
import os
import time
import numpy as np

## 3 = parede
## 4 = parede visitada
## 1 = vítima
## 2 = vítima visitada
## 0 = não visitado
## -1 = visitado

possibilities = ["S", "L", "N", "O", "SE", "NE", "SO", "NO"]
movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1),
                    "NE" : (-1, 1),
                    "NO" : (-1, -1),
                    "SE" : (1, 1),
                    "SO" : (1, -1)}

def getConfig():
    arq = open(os.path.join("config_data","config.txt"),"r")
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

    return configDict

def getAmbiente():
    arq = open(os.path.join("config_data","ambiente.txt"),"r")
    ambienteDict = {} 
    for line in arq:
        ## O formato de cada linha é:var=valor
        ## As variáveis são 
        ##  maxLin, maxCol que definem o tamanho do labirinto
        ## Tv e Ts: tempo limite para vasculhar e tempo para salvar
        ## Bv e Bs: bateria inicial disponível ao agente vasculhador e ao socorrista
        ## Ks :capacidade de carregar suprimentos em número de pacotes (somente para o ag. socorrista)

        values = line.split(" ")

        coords = []

        for i in range(1, len(values)):
            if "\n" in values[i]:
                values[i] = values[i].replace("\n", "")   
            coords.append(values[i]);

        ambienteDict[values[0]] = coords

    return ambienteDict

def printMap(map, agent_pos, ag_vasc_visited):
    print("----------------- mapa atual -----------------")
    for line in map:
        print("     ",line)
    print("--------------- end mapa atual ---------------")
    print("agent_pos: ", agent_pos)
    print("ag_vasc_visited: ", ag_vasc_visited)
    print("----------------------------------------------")
    
    # time.sleep(1)

# def calcularRetorno(agent_init_pos, agent_pos, ag_vasc_visited, bateria_vasc, caminho_retorno, hora_de_voltar):
#     """Retorna uma lista [] em que [0] é uma bool que informa se é hora de voltar\n
#         e [1] é o caminho de volta\n
#         true = volta"""

#     ## objetivo é a posição inicial do agente, do começo do programa
#     goal = agent_init_pos
#     current_test_pos = agent_pos
#     bateria_pra_voltar = 0
#     caminho_temp = [];

#     pos_n = [agent_pos[0] + movePos["N"][0], agent_pos[1] + movePos["N"][1]]
#     pos_o = [agent_pos[0] + movePos["O"][0], agent_pos[1] + movePos["O"][1]]
#     pos_l = [agent_pos[0] + movePos["L"][0], agent_pos[1] + movePos["L"][1]]
#     pos_s = [agent_pos[0] + movePos["S"][0], agent_pos[1] + movePos["S"][1]]
#     pos_ne = [agent_pos[0] + movePos["NE"][0], agent_pos[1] + movePos["NE"][1]]
#     pos_no = [agent_pos[0] + movePos["NO"][0], agent_pos[1] + movePos["NO"][1]]
#     pos_se = [agent_pos[0] + movePos["SE"][0], agent_pos[1] + movePos["SE"][1]]
#     pos_so = [agent_pos[0] + movePos["SO"][0], agent_pos[1] + movePos["SO"][1]]

#     menorCusto = INFINITE

#     caminho_temp.append(agent_pos)

#     ## enquanto a última posição do vetor não for o objetivo (não encontrou o caminho)
#     while caminho_temp[len(caminho_temp)-1] != goal and bateria_pra_voltar+2 < bateria_vasc: 
#         for pos in reversed(ag_vasc_visited):
#             if (pos != agent_pos):
#                 caminho_temp.append(pos)
#                 bateria_pra_voltar += 1
        
#     if (bateria_pra_voltar+2 >= bateria_vasc): 
#         hora_de_voltar = True

#     caminho_retorno = caminho_temp

#     return hora_de_voltar


def tentarMover(agent_pos, agent_init_pos, mov_dir, map, bateria_vasc, 
ag_vasc_walls, ag_vasc_vict, ag_vasc_visited, caminho_retorno, hora_de_voltar):
    new_pos = [agent_pos[0] + movePos[mov_dir][0], agent_pos[1] + movePos[mov_dir][1]]
    x, y = new_pos[0], new_pos[1]

    ## fora do mapa
    if (x < 0 or y < 0):
        return 
    if (x >= len(map)):
        return
    if (y >= len(map[0])):
        return 
    
    ## se encontrar uma parede
    if (map[x][y] == 3):
        # gasta 1 de bateria
        # gasta 1 de tempo
        # parede visitada
        map[x][y] = 4 
        ag_vasc_walls.append([x, y])

        # printMap(map, agent_pos, ag_vasc_visited)
        # não se move
        return 
    
    if (map[x][y] == 0):
        # gasta 1 de bateria
        # gasta 1 de tempo
        map[x][y] = -1 # posição visitada

        # if (calcularRetorno(agent_init_pos, agent_pos, 
        # ag_vasc_visited, bateria_vasc, caminho_retorno, hora_de_voltar)):
        #     return
        
        print ("variável: ", "agent_pos", "//", "valor: ", agent_pos, "//", "tipo: ", type(agent_pos))
        agent_pos = [x, y]
        print ("variável: ", "agent_pos", "//", "valor: ", agent_pos, "//", "tipo: ", type(agent_pos))
        ag_vasc_visited.append(agent_pos)

        printMap(map, agent_pos, ag_vasc_visited)

        tentarMover(agent_pos, agent_init_pos, "S", map, bateria_vasc, ag_vasc_walls, ag_vasc_vict, ag_vasc_visited, caminho_retorno, hora_de_voltar)
        tentarMover(agent_pos, agent_init_pos, "L", map, bateria_vasc, ag_vasc_walls, ag_vasc_vict, ag_vasc_visited, caminho_retorno, hora_de_voltar)
        tentarMover(agent_pos, agent_init_pos, "N", map, bateria_vasc, ag_vasc_walls, ag_vasc_vict, ag_vasc_visited, caminho_retorno, hora_de_voltar)
        tentarMover(agent_pos, agent_init_pos, "O", map, bateria_vasc, ag_vasc_walls, ag_vasc_vict, ag_vasc_visited, caminho_retorno, hora_de_voltar)

    ## encontrou uma vítima
    if (map[x][y] == 1):
        ag_vasc_vict.append([x, y])
        # gasta 1 de bateria
        # gasta 1 de tempo
        # scaneia gastando tempo e bateria
        map[x][y] = 2 # posição visitada

        # if (calcularRetorno(agent_init_pos, agent_pos, 
        #     ag_vasc_visited, bateria_vasc, caminho_retorno)):
        #     return
        
        print ("variável: ", "agent_pos", "//", "valor: ", agent_pos, "//", "tipo: ", type(agent_pos))
        agent_pos = [x, y]
        print ("variável: ", "agent_pos", "//", "valor: ", agent_pos, "//", "tipo: ", type(agent_pos))

        ag_vasc_visited.append(agent_pos)

        printMap(map, agent_pos, ag_vasc_visited)

        tentarMover(agent_pos, agent_init_pos, "S", map, bateria_vasc, ag_vasc_walls, ag_vasc_vict, ag_vasc_visited, caminho_retorno, hora_de_voltar)
        tentarMover(agent_pos, agent_init_pos, "L", map, bateria_vasc, ag_vasc_walls, ag_vasc_vict, ag_vasc_visited, caminho_retorno, hora_de_voltar)
        tentarMover(agent_pos, agent_init_pos, "N", map, bateria_vasc, ag_vasc_walls, ag_vasc_vict, ag_vasc_visited, caminho_retorno, hora_de_voltar)
        tentarMover(agent_pos, agent_init_pos, "O", map, bateria_vasc, ag_vasc_walls, ag_vasc_vict, ag_vasc_visited, caminho_retorno, hora_de_voltar)

    # gasta 1 de bateria
    # gasta 1 de tempo

    printMap(map, agent_pos, ag_vasc_visited)

    return

    ## se o movimento for na diagonal
    ## if (0,0) (1,1)
    ## y2-y1 x2-x1
    # if (map[x][y] == 2):
    #     # gasta 1 de bateria
    #     # gasta 1 de tempo
    #     map[x][y] = 3 # parede visitada
    #     ag_vasc_walls.append(map[x], map[y])

    #     # não se move
    #     return False
    

def explorarMapa(agent_init_pos, map, ag_vasc_visited, 
    bateria_vasc, ag_vasc_walls, ag_vasc_vict):


    ## "visita" a posição inicial do agente
    map[agent_init_pos[0]] [agent_init_pos[1]] = -1

    ## inicializa posição atual do agente com a posição inicial
    agent_pos = agent_init_pos
    # print ("variável: ", "agent_pos", "//", "valor: ", agent_pos, "//", "tipo: ", type(agent_pos))

    ## adiciona posição visitada a um vetor de posições visitadas  
    ag_vasc_visited.append(agent_init_pos)

    caminho_retorno = []
    hora_de_voltar = False

    ## verifica se possui bateria pra voltar + 2 (pra escanear uma vítima)
    tentarMover(agent_pos, agent_init_pos, "S", map, bateria_vasc, ag_vasc_walls, 
        ag_vasc_vict, ag_vasc_visited, caminho_retorno, hora_de_voltar)

    # print ("variável: ", "caminho_retorno", "//", "valor: ", caminho_retorno, "//", "tipo: ", type(caminho_retorno))
    print ("variável: ", "caminho_retorno", "//", "valor: ", caminho_retorno, "//", "tipo: ", type(caminho_retorno))

    # ## retorna pra base pelo melhor caminho
    # for pos in caminho_retorno:
    #     # print ("variável: ", "pos", "//", "valor: ", pos, "//", "tipo: ", type(pos))
    #     map[pos[0]][pos[1]] = -2
    #     bateria_vasc -= 1
    #     print ("variável: ", "agent_pos", "//", "valor: ", agent_pos, "//", "tipo: ", type(agent_pos))
    #     # agent_pos = pos
    #     print ("variável: ", "agent_pos", "//", "valor: ", agent_pos, "//", "tipo: ", type(agent_pos))

    return

def euc_dist (a, b):
    print("a: ", a, "b: ", b)
    return (np.sqrt((b[1]-a[1])*(b[1]-a[1]) + ((b[0]-a[0])*(b[0]-a[0]))))

def criarPlanoResgate(map, ag_vasc_vict, ag_vasc_visited, ag_init_pos,
         ag_vasc_walls, plano_resgate):

    ## encontrar a vítima mais próxima

    ## inicializa o caminho inicial atual
    current_pos = ag_init_pos

    ## copia vetor de vítimas para dar pop toda vez que visitar uma
    all_victims = ag_vasc_vict


    while (len(all_victims) > 0):

        ## inicializa vítima mais próxima supondo uma
        closest_victim = all_victims[0]

        ## inicializa melhor direção
        best_dir = []

        ## inicializa custo até a vítima mais próxima
        closest_euc_dist = INFINITE

        ## inicializa caminho parcial
        caminho_parcial = []

        ## encontra vítima mais próxima
        for vict in ag_vasc_vict:
            ## calcula distância euclidiana pra achar a vítima mais próxima
            dist = euc_dist(ag_init_pos, vict)
            if (dist < closest_euc_dist):
                closest_euc_dist = dist
                closest_victim = vict
        
        while (current_pos != closest_victim):
            ## possíveis direções
            pos_s = [current_pos[0] + movePos["S"][0], current_pos[1] + movePos["S"][1]]
            pos_l = [current_pos[0] + movePos["L"][0], current_pos[1] + movePos["L"][1]]
            pos_o = [current_pos[0] + movePos["O"][0], current_pos[1] + movePos["O"][1]]
            pos_n = [current_pos[0] + movePos["N"][0], current_pos[1] + movePos["N"][1]]

            ## assume que essa é a melhor direção
            if (pos_s[0] < len(map[0])):
                # and pos_s not in (ag_vasc_walls)
                # and pos_s in ag_vasc_visited):
                best_dir = pos_s

            ## encontra passo de menor custo até ela
            ## verifica se não sai do mapa
            ## verifica se não é parede
            ## verifica se foi mapeado pelo agente vasculhador
            if (euc_dist(pos_l, closest_victim) < euc_dist(best_dir, closest_victim)
                and pos_l[1] < len(map)):
                # and pos_l not in (ag_vasc_walls)
                # and pos_l in ag_vasc_visited):
                best_dir = pos_l

            elif (euc_dist(pos_o, closest_victim) < euc_dist(best_dir, closest_victim) 
                and pos_o[1] >= 0):
                # and pos_o not in (ag_vasc_walls)
                # and pos_o in ag_vasc_visited):
                best_dir = pos_o

            elif (euc_dist(pos_n, closest_victim) < euc_dist(best_dir, closest_victim)
                and pos_n[1] >= 0):
                # and pos_n not in (ag_vasc_walls)
                # and pos_n in ag_vasc_visited):
                best_dir = pos_n
            
            current_pos = best_dir
            caminho_parcial.append(current_pos)

        
        current_pos = closest_victim
        all_victims.remove(closest_victim)

        for pos in caminho_parcial:
            plano_resgate.append(pos)

def executarPlanoResgate (map, ag_init_pos, ag_vasc_vict, 
    plano_resgate, pacotes):

    agent_pos = ag_init_pos

    not_visited_vict = ag_vasc_vict

    ## "visita" a posição inicial do agente
    map[ag_init_pos[0]] [ag_init_pos[1]] = 0

    caminho_retorno = []
    hora_de_voltar = False

    ## vai pra próxima posição do plano resgate
    for pos in plano_resgate:
        agent_pos = pos
        map[pos[0]][pos[1]] = 0
        if (pos in ag_vasc_vict):
            not_visited_vict.remove(pos)
            pacotes -= 1

    if (agent_pos == ag_init_pos):
        print("Voltou pra base")
    print(pacotes)
    print("Vítimas salvas: ", len(ag_vasc_vict))
    return


def main():
    ## Inicializa o labirinto
    configDict = getConfig()
    ambienteDict = getAmbiente()
    ag_vasc_visited = []
    ag_vasc_walls = []
    ag_vasc_vict = []

    bateria_vasc = int(configDict["Bv"])
    ## print ("variável: ", "bateria_vasc", "//", "valor: ", bateria_vasc, "//", "tipo: ", type(bateria_vasc))

    ## imprime as configurações
    print("dicionario config: ", configDict)

    ## cria o mapa
    map = [[0 for col in range(configDict["maxLin"])] for row in range(configDict["maxCol"])]

    print("dicionario ambiente: ", ambienteDict)

    ## posição inicial do agente
    agent_init_pos = ambienteDict["Agente"][0].split(",")
    agent_init_pos[0], agent_init_pos[1] = int(agent_init_pos[0]), int(agent_init_pos[1])
    print("agent_init_pos: ", agent_init_pos)

    ## adiciona as paredes no mapa 
    for i in range(0, len(ambienteDict["Parede"])):
        wall_coord = ambienteDict["Parede"][i].split(",")
        x, y = int(wall_coord[0]), int(wall_coord[1])
        map[x][y] = 3

    ## adiciona as vítimas no mapa 
    for i in range(0, len(ambienteDict["Vitima"])):
        vict_coord = ambienteDict["Vitima"][i].split(",")
        i, j = int(vict_coord[0]), int(vict_coord[1])
        map[i][j] = 1

    ## alterar o mapa dentro da função altera fora também, é ponteiro
    ## mapa é passado apenas para fins de verificação dentro das regras
    ## dos sensores do agente vasculhador
    explorarMapa(agent_init_pos, map, ag_vasc_visited, 
        bateria_vasc, ag_vasc_walls, ag_vasc_vict)


    ## após a exploração do mapa
    ## ag_vasc_visited terá uma ordem de visitação do agente vasculhador
    
    ## ag_vasc_walls terá um vetor com as paredes encontradas

    ## ag_vasc_vict terá um vetor com as vítimas encontradas

    ## haverá também um vetor com paredes

    ## haverá também um vetor com vítimas

    ## calcular o melhor caminho

    plano_resgate = []

    criarPlanoResgate(map, ag_vasc_vict, ag_vasc_visited, agent_init_pos,
         ag_vasc_walls, plano_resgate)

    pacotes = configDict["Ks"]

    executarPlanoResgate(map, agent_init_pos, ag_vasc_vict, plano_resgate, pacotes)

    ## executar

    ## voltar pra base


    








    

    
        




if __name__ == '__main__':
    main()  