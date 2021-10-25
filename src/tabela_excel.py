import pandas as pd

class Tabela:
    # prepara um base de dados do excel para ser usada por outros arquivos
    def __init__(self, nome:str):
        """recebe o nome de uma arquivo excel na pasta 'dados'"""
        self.nome = nome
        self.tabela = None
        self.nome_x = None
        self.nome_y = None
    
    def ler(self):
        """le os dados do arquivo, os armazena e prepara labels
        para serem usados por outros programas"""
        self.tabela=pd.read_excel("dados/"+self.nome)
        self.nome_x = self.tabela.columns[0]
        self.nome_y = self.tabela.columns[1]
