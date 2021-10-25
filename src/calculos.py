import implementar_interpol_newt as iin
import implementar_minimos_quadrados as imq
import implementar_grafico as igr
import matplotlib.pyplot as plt
import grafico

def plotar_grafico(tab):
    x = tab.tabela[tab.nome_x]
    y = tab.tabela[tab.nome_y]
    _, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel='x', ylabel='y', title='grafico')
    ax.grid()
    plt.show()

def plotar_func(objeto, tab):
    try:
        func = objeto.gerar_poli
    
    except:
        func = objeto.func

    try:
        inter = [objeto.x_uteis.iloc[0], objeto.x_uteis.iloc[-1]]

    except:
        inter = [tab.tabela[tab.nome_x].iloc[0], tab.tabela[tab.nome_x].iloc[-1]]

    grafico = igr.main(func, inter)
    grafico.plotar()

def plotar_tudo(objetos, tab):
    x0 = tab.tabela[tab.nome_x]
    y0 = tab.tabela[tab.nome_y]
    _, ax = plt.subplots()
    ax.plot(x0, y0, label="tabela")

    for objeto in objetos:
        try:
            la = "interpol"
            func = objeto.gerar_poli
        
        except:
            la = "linear"
            func = objeto.func

        try:
            inter = [objeto.x_uteis.iloc[0], objeto.x_uteis.iloc[-1]]

        except:
            inter = [tab.tabela[tab.nome_x].iloc[0], tab.tabela[tab.nome_x].iloc[-1]]

        listas = grafico.Grafico(func, 1000, inter).gerar_listas()
        ax.plot(listas[0], listas[1], label=la)

    ax.set(xlabel='x', ylabel='y', title='grafico')
    ax.grid()
    plt.legend()
    plt.show()

def interpol(tab, ponto):
    inter = iin.main(tab, ponto, 1)
    return inter

def linear(tab, ponto):
    min_quad = imq.main(tab, ponto)
    return min_quad
