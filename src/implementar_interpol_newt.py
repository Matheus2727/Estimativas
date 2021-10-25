import interpol_newt as inn
# implementa a classe Interpolação do arquivo interpol_newt

def main(tabela, alvo:float, erro:int):
    """recebe um x alvo e uma quantidade de pontos a serem reservados para
    o calculo do erro. se o alvo estiver fora do intervalo da tabela não
    gera resultado nem estimativa para o erro. se zero pontos forem 
    reservados para o erro ele não gera estimativa. retorna um objeto
    da classe Interpolação com os resultados calculados"""
    newt = inn.Interpolação(tabela)
    newt.preparar()
    newt.resolver(alvo, erro)
    return newt
