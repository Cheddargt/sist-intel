from view import View 
from block import Block
from agentv import AgentV

class Model:
    """Model é o modelo do ambiente. Implementa um ambiente na forma de um labirinto com paredes, agentes e vítimas.
    """
    def __init__(self, rows, columns):
        
        """Construtor de modelo do ambiente físico (labirinto)
        @param rows: número de linhas do labirinto
        @param columns: número de colunas do labirinto
        """
        self.rows = rows
        self.columns = columns
    
        self.view = View(self)
        self.blocks = [[Block(x, y) for x in range(columns)] for y in range(rows)]
        self.agent = None
        self.victim = []
        
    def checkValidCoord(self, x, y):
        """Verifica se uma coordenada é válida
        @param x: coordenada x
        @param y: coordenada y
        """
        return x >= 0 and x < self.rows and y >= 0 and y < self.columns

    def setAgent(self, x,y):
        self.agent = AgentV(x, y)

    def setVictim(self, x, y):
        if self.checkValidCoord(x, y):
            self.blocks[x][y].setCategory("victim")
        else:
            print("Erro: coordenada inválida")

    def setWall(self, x, y):
        if self.checkValidCoord(x, y):
            self.blocks[x][y].setCategory("wall")
        else:
            print("Erro: coordenada inválida")

    def generateMap(self, filename):
        """Gera um mapa de labirinto a partir de um arquivo
        @param filename: nome do arquivo
        """
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines: 
            line = line.split()
            print(line)

            for coord in line[1:]:
                coord = coord.split(',')
                x = int(coord[0])
                y = int(coord[1])

                if line[0] == 'Agente':
                    self.setAgent(x, y)
                elif line[0] == 'Parede':
                    self.setWall(x, y)
                elif line[0] == 'Vitima':
                    self.setVictim(x, y)
                else:
                    print("Erro: linha inválida. ", line)
                    return False
        return True
    ## Desenha o labirinto na tela
    def draw(self):
        self.view.draw()