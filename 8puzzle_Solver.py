
import copy

objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Posições dos números no estado objetivo
posGoal = {
    0: (2, 2),
    1: (0, 0),
    2: (0, 1),
    3: (0, 2),
    4: (1, 0),
    5: (1, 1),
    6: (1, 2),
    7: (2, 0),
    8: (2, 1)
}


class Estado:
    
    def __init__(self, estado, pai, g, visitado=False):
        self.configuracao = estado
        self.pai = pai
        self.g = g
        self.encontra_zero()
        self.h = self.calcula_h()
        self.f = self.g + self.h
        self.visitado = visitado
    
    def __eq__(self, other):
        return self.configuracao == other.configuracao
    
    def encontra_zero(self):
        found = False
        for i in range(len(self.configuracao)):
            for j in range(len(self.configuracao[i])):
                if(self.configuracao[i][j] == 0):
                    self.x = i
                    self.y = j
                    found = True
                    break

            if found:
                break
            
    def calcula_h(self):
        h = 0
        h_atual = 0

        for i in range(len(self.configuracao)):
            for j in range(len(self.configuracao[i])):
                h_atual = abs(i - posGoal.get(self.configuracao[i][j])[0]) + abs(j - posGoal.get(self.configuracao[i][j])[1])
                h += h_atual

        return h
    
    def print_estado(self):
        print("-"*9)
        for i in range(len(self.configuracao)):
            for j in range(len(self.configuracao)):
                print(f"|{self.configuracao[i][j]}|", end='')
            print("")
        
        print("-"*9)
        print(f"g = {self.g}")
        print(f"h = {self.h}")
        print(f"f = {self.f}")
    
    def set_visitado(self):
        self.visitado = True


class Node:
    # A arvore é imaginada como uma lista duplamente ligada de outras listas, onde cada nó é uma lista de expansoes de seu nó pai
    # O anterior diz respeito ao nó que gerou o nó presente
    # O próximo diz respeito aos nós que foram gerados à partir do nó presente
    def __init__(self, estados, anterior, proximo):
        self.estados = estados
        self.anterior = anterior
        self.proximo = proximo
    
    def setProximo(self, prox):
        self.proximo = prox
    
    def setEstados(self, estado):
        self.estados = estado


#   Ordenar noh pelo custo
def ordena_ramo(lista):
    l = copy.deepcopy(lista)
    tam = len(l)
    
    if tam <= 1:
        return lista
    
    else:
        pivot = l.pop()
        
    itens_maiores = []
    itens_menores = []
    
    for item in l:
        if item.f < pivot.f:
            itens_maiores.append(item)
        else:
            itens_menores.append(item)
            
    return ordena_ramo(itens_maiores) + [pivot] + ordena_ramo(itens_menores)


# Funcoes para mover o 0
def mover_baixo(estado):
    x, y = estado.x, estado.y
    
    new_config = copy.deepcopy(estado.configuracao)
    
    if (x < 2):
        aux = new_config[x+1][y]
        new_config[x+1][y] = 0
        new_config[x][y] = aux
    
    new_estado = Estado(new_config, estado, estado.g + 1)
    return new_estado

def mover_cima(estado):
    
    x, y = estado.x, estado.y
    new_config = copy.deepcopy(estado.configuracao)
    
    if (x > 0):
        aux = new_config[x-1][y]
        new_config[x-1][y] = 0
        new_config[x][y] = aux
    
    new_estado = Estado(new_config, estado, estado.g + 1)
    return new_estado

def mover_direita(estado):
    x, y = estado.x, estado.y
    new_config = copy.deepcopy(estado.configuracao)
    
    if (y < 2):
        aux = new_config[x][y+1]
        new_config[x][y+1] = 0
        new_config[x][y] = aux
        
    new_estado = Estado(new_config, estado, estado.g + 1)
    return new_estado

def mover_esquerda(estado):
    x, y = estado.x, estado.y
    new_config = copy.deepcopy(estado.configuracao)
    
    if (y > 0):
        aux = new_config[x][y-1]
        new_config[x][y-1] = 0
        new_config[x][y] = aux
        
    new_estado = Estado(new_config, estado, estado.g + 1)
    return new_estado


# Expande os nós da arvore
def expandir(estado, node, raiz):
    
    passo = raiz
    
    expansao = []
    
    e1 = mover_cima(estado)
    
    ja_gerado = False
    if (e1 != estado):
        
        while (passo != None):
            for e in passo.estados:
                if(e == e1):
                    ja_gerado = True
                    passo = None
                    break
                
            if (passo != None):
                passo = passo.proximo
        
        if (not ja_gerado):
            expansao.append(e1)
    
    e2 = mover_baixo(estado)
    
    ja_gerado = False
    passo = raiz
    if (e2 != estado):
        while (passo != None):
            for e in passo.estados:
                if(e == e2):
                    ja_gerado = True
                    passo = None
                    break
            if(passo != None):
                passo = passo.proximo
        
        if (not ja_gerado):
            expansao.append(e2)
    
    e3 = mover_direita(estado)
    
    ja_gerado = False
    passo = raiz
    if (e3 != estado):
        while (passo != None):
            for e in passo.estados:
                if(e == e3):
                    ja_gerado = True
                    passo = None
                    break
            if (passo != None):
                passo = passo.proximo
        
        if (not ja_gerado):
            expansao.append(e3)
    
    e4 = mover_esquerda(estado)
    
    ja_gerado = False
    passo = raiz
    if (e4 != estado):
        while (passo != None):
            for e in passo.estados:
                if(e == e4):
                    ja_gerado = True
                    passo = None
                    break
            if (passo != None):
                passo = passo.proximo
        
        if (not ja_gerado):
            expansao.append(e4)
    
    novo_no = Node(expansao, node, None)
    ordenado = ordena_ramo(novo_no.estados)
    novo_no.setEstados(ordenado)
    
    node.proximo = novo_no

    return novo_no


config_ini = [[1, 8, 2], [0, 4, 3], [7, 6, 5]]

inicio = Estado(config_ini, None, 0, True)

raiz = Node([inicio], None, None)

print("Estado Inicial:")
inicio.print_estado()


passo = raiz
configuracao = []
escolhido = []

# APLICANDO BUSCA A*
print("\nAplicando Busca A*")
while (passo != None and configuracao != objetivo):
    menor_f = None
    
    if (passo == raiz):
        escolhido = copy.deepcopy(passo.estados[0])
        
    prox = expandir(escolhido, passo, raiz)
    
    menor_f = prox.estados[0]
    
    if (raiz.proximo != None):
        passo2 = raiz
        hasMenor = False
        
        while (passo2 != None):
            for e in passo2.estados:
                if ((not e.visitado) and menor_f.f > e.f):
                    menor_f = copy.deepcopy(e)
                    e.visitado = True
                    hasMenor = True
                    break
            if (hasMenor):
                passo2 = None
            else:
                passo2 = passo2.proximo
    
    if (not hasMenor):
        menor_f.visitado = True
    
    configuracao = copy.deepcopy(menor_f.configuracao)
    
    escolhido = copy.deepcopy(menor_f)
    escolhido.print_estado()
    passo = passo.proximo
