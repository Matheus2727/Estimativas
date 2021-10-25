import pandas as pd

class Regressão_Linear:
    def __init__(self, tabela):
        self.tabela = tabela.tabela.copy()
        self.nome_x = tabela.nome_x
        self.nome_y = tabela.nome_y
        self.tabelas_uteis = None
        self.lista_x = self.tabela[self.nome_x]
        self.lista_y = self.tabela[self.nome_y]
        self.somas = None
        self.a0 = None
        self.a1 = None
        self.func = None
        self.resultado = None

    def gerar_tabelas_uteis(self):
        tabelas_uteis = {}
        tabelas_uteis["x"] = self.lista_x
        tabelas_uteis["y"] = self.lista_y
        quadrados = []
        mult = []
        for i, x in enumerate(self.lista_x):
            quadrados.append(x**2)
            mult.append(self.lista_y[i]*x)
        
        tabelas_uteis["quadrados"] = pd.Series(quadrados)
        tabelas_uteis["mult"] = pd.Series(mult)
        self.tabelas_uteis = pd.DataFrame(tabelas_uteis)
    
    def gerar_somas(self):
        somas = {}
        tamanho = len(self.tabelas_uteis[self.nome_x])
        somas["i"] = tamanho
        for key in self.tabelas_uteis:
            tab = self.tabelas_uteis[key]
            somas[key] = [tab.sum()]
        
        self.somas = pd.DataFrame(somas)
    
    def gerar_sistema(self):
        linhas = {0: [self.somas["i"][0], self.somas["x"][0], self.somas["y"][0]],
        1: [self.somas["x"][0], self.somas["quadrados"][0], self.somas["mult"][0]]}
        matriz = pd.DataFrame(linhas)
        i = 0
        pivo = matriz[i][i]
        alvo = matriz[i + 1][i]
        constante = -alvo/pivo
        for i2, _ in enumerate(matriz[0]):
            matriz[i + 1][i2] += matriz[i][i2]*constante
        
        self.a1 = matriz[1][2]/matriz[1][1]
        self.a0 = (matriz[0][2] - self.a1*matriz[0][1])/matriz[0][0]
    
    def gerar_func(self):
        self.func = lambda x: self.a0 + self.a1*x
    
    def preparar(self):
        self.gerar_tabelas_uteis()
        self.gerar_somas()
        self.gerar_sistema()
        self.gerar_func()
    
    def resolver(self, x_alvo:float):
        self.resultado = self.func(x_alvo)
