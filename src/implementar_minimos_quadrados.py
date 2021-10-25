import minimos_quadrados as miq
# implementa a classe Regressão_Linear do arquivo minimos_quadrados

def main(tabela, alvo):
    """recebe um x alvo e retorna um objeto da classe 
    Regressão_Linear com o resultado calculado"""
    rel = miq.Regressão_Linear(tabela)
    rel.preparar()
    rel.resolver(alvo)
    return rel
