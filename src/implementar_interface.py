import tabela_excel as tbe
import interface
import calculos

def receber_tabela(janela):
    atual = None
    for input in janela.inputs:
        if input.nome == "arq":
            atual = input

    tab = tbe.Tabela(atual.input)
    tab.ler()
    return tab


def receber_ponto(janela):
    atual = None
    for input in janela.inputs:
        if input.nome == "ponto":
            atual = input

    return int(atual.input)


def receber_conteudo(**kwargs):
    janela = kwargs["janela"]
    func = kwargs["func"]
    ponto = receber_ponto(janela)
    tab = receber_tabela(janela)
    conteudo = ""
    objeto = func(tab, ponto)
    try:
        valor = str(round(objeto.resultado, 6))
    
    except TypeError:
        valor = "None"
        erro = "None"

    conteudo += "f({}) = ".format(ponto) + valor + "\n"
    try:
        erro = str(round(objeto.erro, 6))
        conteudo += "erro = " + erro+ "\n"
        
    except:
        pass

    atualizar_conteudo(janela, conteudo)


def atualizar_conteudo(janela, conteudo):
    atual = None
    for texto in janela.textos:
        if texto.nome == "resul":
            atual = texto

    atual.conteudo = conteudo


def plotar_tabela(**kwargs):
    janela = kwargs["janela"]
    tab = receber_tabela(janela)
    calculos.plotar_grafico(tab)


def plotar_func(**kwargs):
    janela = kwargs["janela"]
    func_ini = kwargs["func"]
    tab = receber_tabela(janela)
    ponto = receber_ponto(janela)
    objeto = func_ini(tab, ponto)
    calculos.plotar_func(objeto, tab)


def plotar_tudo(**kwargs):
    janela = kwargs["janela"]
    funcs_ini = kwargs["funcs"]
    tab = receber_tabela(janela)
    ponto = receber_ponto(janela)
    objetos = []
    for func_ini in funcs_ini:
        objetos.append(func_ini(tab, ponto))

    calculos.plotar_tudo(objetos, tab)


def setarbots(janela: interface.Janela):
    """ideia de função para criar e adicionar botoes"""
    bot_plotar = interface.Botao(10, 90, 0, 0, "plotar tabela", "plotar", 30, [120, 120, 120], plotar_tabela, {"janela": janela})
    bot_interpol = interface.Botao(10, 170, 0, 0, "interpolação", "interpol", 30, [120, 120, 120], receber_conteudo, {"janela": janela, "func": calculos.interpol})
    bot_plotar_poli = interface.Botao(300, 170, 0, 0, "plotar poli", "plotar_poli", 30, [120, 120, 120], plotar_func, {"janela": janela, "func": calculos.interpol})
    bot_linear = interface.Botao(10, 210, 0, 0, "regressão linear", "linear", 30, [120, 120, 120], receber_conteudo, {"janela": janela, "func": calculos.linear})
    bot_plotar_reta = interface.Botao(300, 210, 0, 0, "plotar reta", "plotar_reta", 30, [120, 120, 120], plotar_func, {"janela": janela, "func": calculos.linear})
    bot_plotar_tudo = interface.Botao(10, 250, 0, 0, "plotar tudo", "plotar_tudo", 30, [120, 120, 120], plotar_tudo, {"janela": janela, "funcs": [calculos.linear, calculos.interpol]})
    janela.addBotões([bot_interpol, bot_plotar_poli, bot_linear, bot_plotar_reta, bot_plotar, bot_plotar_tudo])


def setartextos(janela: interface.Janela):
    text_arq = interface.Texto(10, 10, 30, "arquivo:", "arquivo")
    text_ponto = interface.Texto(10, 50, 30, "ponto:", "ponto")
    text_calc = interface.Texto(10, 130, 30, "calculos:", "calc")
    text_resul = interface.Texto(10, 290, 30, "", "resul")
    janela.addTextos([text_arq, text_ponto, text_calc, text_resul])


def setarinputs(janela: interface.Janela):
    inpu_arq = interface.Inp(160, 10, 20, 30, "exemplo_raiz.xlsx", "arq")
    inpu_ponto = interface.Inp(160, 50, 20, 30, "24", "ponto")
    janela.addInputs([inpu_arq, inpu_ponto])


def main():
    """cria um objeto Janela, organiza os botoes, textos e inputs.
    Apos isso seta os valores iniciais"""
    janela = interface.Janela(1000, 700, "menu")
    setarbots(janela)
    setartextos(janela)
    setarinputs(janela)
    janela.iniciar()
    return janela


if __name__ == "__main__":
    main()
