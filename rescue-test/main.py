from asyncio.windows_events import INFINITE
import sys
import os
import time

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

def printMap(map):
    print("----------------- mapa atual -----------------")
    for line in map:
        print("     ",line)
    print("--------------- end mapa atual ---------------")

def calcularRetorno(agent_init_pos, agent_pos, ag_vasc_visited):
    """Retorna uma lista [] em que [0] é uma bool que informa se é hora de voltar\n
        e [1] é o caminho de volta\n
        true = volta"""
    
    ## objetivo é a posição inicial do agente, do começo do programa
    goal = agent_init_pos

    caminho = []
    menorCusto = INFINITE
    hora_de_voltar = False

    return caminho, hora_de_voltar

def tentarMover(agent_pos, mov_dir, map, ag_vasc_walls, ag_vasc_vict):

    time.sleep(1)
    printMap(map)
    print("agent_pos: ", agent_pos)
    print("vitimas encontradas: ", ag_vasc_vict)

    
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
        map[x][y] = 4 # parede visitada
        ag_vasc_walls.append([x, y])

        # não se move
        return 
    
    if (map[x][y] == 0):
        # gasta 1 de bateria
        # gasta 1 de tempo
        map[x][y] = -1 # posição visitada
        agent_pos = [x, y]
        tentarMover(agent_pos, "L", map, ag_vasc_walls, ag_vasc_vict)
        tentarMover(agent_pos, "S", map, ag_vasc_walls, ag_vasc_vict)
        tentarMover(agent_pos, "N", map, ag_vasc_walls, ag_vasc_vict)
        tentarMover(agent_pos, "O", map, ag_vasc_walls, ag_vasc_vict)

    ## encontrou uma vítima
    if (map[x][y] == 1):
        ag_vasc_vict.append([x, y])
        # gasta 1 de bateria
        # gasta 1 de tempo
        # scaneia gastando tempo e bateria
        map[x][y] = 2 # posição visitada
        agent_pos = [x, y]
        tentarMover(agent_pos, "S", map, ag_vasc_walls, ag_vasc_vict)
        tentarMover(agent_pos, "L", map, ag_vasc_walls, ag_vasc_vict)
        tentarMover(agent_pos, "O", map, ag_vasc_walls, ag_vasc_vict)
        tentarMover(agent_pos, "N", map, ag_vasc_walls, ag_vasc_vict)


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
    

    

# def dfs(visitados, ag_vasc_visited, pos_atual):
#     if pos_atual not in visitados:
#         print (pos_atual)
#         visitados.add(pos_atual)
#         for neighbour in ag_vasc_visited[pos_atual]:
#             dfs(visitados, ag_vasc_visited, neighbour)



# def dfs(self):
#         """
#         DFS: Busca em profundidade
#             Retorna a próxima coordenada não visitada
#         """
#         for direction in ["NW", "NE", "SW", "SE", "N", "W", "E", "S"]:
#             x, y = self.directionCoord(direction)
#             if self.checkValidCoord(x, y) and not self.visited[y][x]:
#                 self.stack.append((x, y))

#         # Próxima coordenada não visitada da pilha
#         while self.stack:
#             x, y = self.stack.pop(-1)
#             if not self.visited[y][x]:
#                 return x, y
#         return None, None

def explorarMapa(agent_init_pos, map, ag_vasc_visited, 
    bateria_vasc, ag_vasc_walls, ag_vasc_vict):

    agent_pos = [0, 0]

    ## "visita" a posição inicial do agente
    map[agent_init_pos[0]] [agent_init_pos[1]] = -1

    ## inicializa posição atual do agente com a posição inicial
    # agent_pos = (int (agent_init_pos[0]), int (agent_init_pos[1]))
    # print ("variável: ", "agent_pos", "//", "valor: ", agent_pos, "//", "tipo: ", type(agent_pos))

    ## adiciona posição visitada a um vetor de posições visitadas  
    ag_vasc_visited.append(agent_init_pos)

    ## verifica se possui bateria pra voltar + 2 (pra escanear uma vítima)
    ## calcularRetorno 
    while not (calcularRetorno(agent_init_pos, agent_pos, ag_vasc_visited)[0]):
        tentarMover(agent_pos, "S", map, ag_vasc_walls, ag_vasc_vict)
        printMap(map)
        print("agent_pos: ", agent_pos)

        time.sleep(1)
        

    ## retorna pra base pelo melhor caminho

    


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
    
    ## imprime o mapa
    printMap(map)

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
    explorarMapa(agent_init_pos, map, ag_vasc_visited, 
        bateria_vasc, ag_vasc_walls, ag_vasc_vict)

    ## após a exploração do mapa
    ## ag_vasc_visited terá uma ordem de visitação do agente vasculhador
    ag_vasc_visited =   [[0,0], [1,0], [2,0], [3,0], [4,0], 
                        [4,1], [4,2], [4,3], [4,4], [3,4],
                        [2,4], [1,4], [0,4], [1,3], [2,3],
                        [3,3], [3,2], [2,2], [3,1], [1,1]
                        [0,1]]

    ## ag_vasc_walls terá um vetor com as paredes encontradas

    ## ag_vasc_vict terá um vetor com as vítimas encontradas

    ## haverá também um vetor com paredes

    ## haverá também um vetor com vítimas

    ## calcular o melhor caminho

    ## executar

    ## voltar pra base

    printMap(map);
    print("ag_vasc_visited: ", ag_vasc_visited)

    








    

    
        




if __name__ == '__main__':
    main()  