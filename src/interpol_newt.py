import pandas as pd

class Interpolação:
    # aplica o metodo de interpolação de Newton para gerar um polinomio 
    # que passa pelos pontos de uma tabela afim de encontrar a imagem para
    # um determinado x dentro do intervalo dessa tabela e seu erro
    def __init__(self, tabela):
        """recebe uma tabela (elemento Tabela), um x alvo e o numero de
        pontos reservados para o calculo da estimativa do erro.
        se a tabela tiver p pontos, por exemplo, serao usados (p - erro)
        pontos para o resultado e (erro) pontos para o calculo do erro"""
        self.tabela = tabela.tabela.copy()
        self.nome_x = tabela.nome_x
        self.nome_y = tabela.nome_y
        self.ordens = None
        self.lista_x = self.tabela[self.nome_x]
        self.x_uteis = None
        self.resultado = None
        self.erro = None

    def gerar_ordens(self):
        """preenche uma lista com data frames, o data frame de indice i
        representa o vetor de ordem i da tabela"""
        self.ordens = []
        self.ordens.append(self.tabela[self.nome_y]) # a ordem zero representa o vetor de imagens
        for o in range(1, len(self.ordens[0])): # n pontos acarreta n-1 ordens, a primeira ja esta preenchida
            nova_ordem = []
            ord_ant = self.ordens[o - 1]
            for i in range(o): # preenche com None os indices que não podem ser calculados
                nova_ordem.append(None)

            for i in range(o, len(self.ordens[0])): # aplica a formula para cada indice possivel da ordem atual
                nova_ordem.append((ord_ant[i] - ord_ant[i - 1])/(self.lista_x[i] - self.lista_x[(i-o)]))

            self.ordens.append(pd.Series(nova_ordem))
    
    def checar(self, x_alvo):
        if x_alvo < self.lista_x.iloc[-1] and x_alvo > self.lista_x.iloc[0]:
            return True
        
        else:
            return False

    def determinar_x_uteis(self, x_alvo, erro):
        """determina quais pontos são uteis para a determinação do
        polinomio (de acordo com a ordem maxima)"""
        ordem_max = len(self.tabela) - erro - 1
        ordens = len(self.ordens)
        indice = ordens - 1
        for i, x in enumerate(self.lista_x):
            if x >= x_alvo: # localiza o primeiro ponto onde o valor de x é maior que o alvo
                indice = i
                break
        
        nova_lista0 = self.lista_x[:indice] # divide fatias do vetor de valores x nesse indice (o alvo esta entre elas)
        nova_lista1 = self.lista_x[indice:]
        teste_len = lambda nl0, nl1: len(nl0) + len(nl1) > ordem_max + 1 # testa se o numero de x uteis esta ideal para a ordem maxima
        # retira objetos da fatia de maior tamanho ate q estejam com o mesmo tamanho ou o tamanho total estaja ideal
        while len(nova_lista0) > len(nova_lista1) and teste_len(nova_lista0, nova_lista1):
            nova_lista0 = nova_lista0[1:]

        while len(nova_lista0) < len(nova_lista1) and teste_len(nova_lista0, nova_lista1):
            nova_lista1 = nova_lista1[:-1]
        
        while teste_len(nova_lista0, nova_lista1): # se o tamanho não estiver ideal corta os valores mais afastados do alvo de cada fatia
            candidato0 = nova_lista0.iloc[0]
            candidato1 = nova_lista1.iloc[-1]
            dif0 = abs(candidato0 - x_alvo)
            dif1 = abs(candidato1 - x_alvo)
            if dif0 <= dif1:
                nova_lista1 = nova_lista1[:-1]
            
            else:
                nova_lista0 = nova_lista0[1:]

        self.x_uteis = pd.concat([nova_lista0, nova_lista1])
        self.dist = self.x_uteis.index.start # quantos pontos foram ignorados do inicio da lista de pontos
    
    def gerar_poli(self, x_alvo):
        """gera o polinomio de newton para um x alvo. retorna os
        fatores para o calculo do erro"""
        # o polinomio se da por p(x) = a0 + a1*w0(x) + a2*w1(x) +...
        # onde w0(x) = (x - x0), w1(x) = (x - x0)*(x - x1)
        # e os 'a' estão relacionados a tabela de ordens
        subs = [] # subtrações da formula (x - xi)
        for x in self.x_uteis:
            subs.append(x_alvo - x)
        
        fatores = [] # fatores da formula (w em um indice i)
        for s in subs:
            float_temp = 1
            if fatores != []:
                float_temp = fatores[-1]

            fatores.append(s * float_temp)
        
        parcelas = [] # parcelas da formula (partes sendo somadas)
        parcelas.append(self.ordens[0][self.dist])
        for i, f in enumerate(fatores[:-1]):
            parcelas.append(f * self.ordens[i + 1][i + 1 + self.dist])
        
        resultado = 0 # soma cada parcela e obtem o resultado
        for p in parcelas:
            resultado += p
        
        self.resultado = resultado
        self.fatores = fatores
        return resultado
    
    def gerar_erro(self, erro):
        """recebe a ordem maxima a ser trabalhada"""
        # aplica a formula para a estimativa do erro do metodo
        ordem_max = len(self.tabela) - erro - 1
        if len(self.tabela) - 1 > ordem_max: #checa se o erro pode ser estimado
            self.erro = abs(self.fatores[-1]*self.ordens[ordem_max + 1].abs().max())
    
    def preparar(self):
        """prepara o objeto de forma generica para a tabela dada"""
        self.gerar_ordens()

    def resolver(self, x_alvo:float, erro:int):
        """prepara o objeto de forma especifica para os dados e 
        calcula os resultados. recebe um x e um numero de pontos
        a serem reservados para o calculo do erro"""
        if self.checar(x_alvo):
            self.determinar_x_uteis(x_alvo, erro)
            self.gerar_poli(x_alvo)
            self.gerar_erro(erro)
        
        else:
            pass
