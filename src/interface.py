import pygame

pygame.init()
pygame.font.init()


class Janela:
    """padroniza o comportamento de uma janela, a interface"""
    def __init__(self, w: int, h: int, nome: str):
        """recebe a largura, altura e o nome da janela"""
        self.w = w
        self.h = h
        self.nome = nome
        self.botoes = [] # lista de botões da janela
        self.textos = [] # lista de textos da janela
        self.inputs = [] # lista de inputs de texto da janela
        self.inpu = None

    def iniciar(self):
        """inicia a janela, atribui o titulo, dimensoes e fonte"""
        self.disp = pygame.display
        self.disp.set_caption(self.nome)
        self.screen = self.disp.set_mode((self.w, self.h))
        self.fonte = pygame.font.SysFont('arial', 25)

    def addBotões(self, bots: list):
        """adiciona os botões de uma lista a janela"""
        for bot in bots:
            self.botoes.append(bot)
    
    def substBotão(self, bot):
        """substitui um botão se possivel, se não existir previamente adiciona um novo"""
        for i, b in enumerate(self.botoes):
            if b.nome == bot.nome:
                self.botoes[i] = bot
            
            else:
                self.addBotões([bot])

    def addTextos(self, textos: list):
        """adiciona os textos de uma lista a janela"""
        for texto in textos:
            self.textos.append(texto)

    def substTexto(self, texto):
        """substitui ou adiciona um texto a janela"""
        for i, t in enumerate(self.textos):
            if t.nome == texto.nome:
                self.textos[i] = texto
            
            else:
                self.addTextos([texto])

    def addInputs(self, inputs: list):
        """adiciona os inputs de texto de uma lista a janela"""
        for inpu in inputs:
            self.inputs.append(inpu)

    def click(self, pos):
        """recebe uma posição do mouse (onde houve um click) e procura o primeiro
        botão e input que compreendem essa posição em sua area para ativar um evento"""
        for bot in self.botoes: # checa os botões
            limite_x = (pos[0] >= bot.campo_min[0]
                        and pos[0] <= bot.campo_max[0])
            limite_y = (pos[1] >= bot.campo_min[1]
                        and pos[1] <= bot.campo_max[1])
            if limite_x and limite_y: # se o botão for localizado seu evento é ativado e o loop é quebrado
                bot.click()
                break

        for inpu in self.inputs:
            limite_x = (pos[0] >= inpu.campo_min[0]
                        and pos[0] <= inpu.campo_max[0])
            limite_y = (pos[1] >= inpu.campo_min[1]
                        and pos[1] <= inpu.campo_max[1])
            if limite_x and limite_y: # se o input for localizado ele é escolhido como input ativo da janela
                self.inpu = inpu
                break

        else: # se um input não for escolhido o input ativo é desselecionado
            self.inpu = None

    def atualizar_janela(self):
        """gera um novo frame para a janela e a atualiza"""
        self.screen.fill((200, 200, 200)) # cor de fundo
        for texto in self.textos: # printa na interface texto por texto
            conteudo = texto.printar()
            for frase, posx, posy in conteudo:
                self.screen.blit(frase, (posx, posy))

        for bot in self.botoes: # printa na interface botao por botao
            pygame.draw.rect(self.screen, bot.cor, [
                             bot.x, bot.y, bot.w, bot.h])
            texto = bot.fonte.render(bot.conteudo, False, (10, 10, 10))
            self.screen.blit(texto, (bot.x + 5, bot.y))

        for inpu in self.inputs: # printa na interface input por input
            for i in range(inpu.maximo):
                letra = ""
                if i < len(inpu.amostra):
                    letra = inpu.amostra[i]

                inpu.gerar_amostra()
                pygame.draw.rect(self.screen, inpu.cor, [
                                 inpu.x + inpu.w * i, inpu.y, inpu.w, inpu.h])
                texto = inpu.fonte.render(letra, False, (10, 10, 10))
                self.screen.blit(texto, (inpu.x + inpu.w * i, inpu.y))

        if self.inpu is not None: # desenha o cursor do input selecionado se houver algum
            for i, letra in enumerate(self.inpu.input):
                local_escolhido = self.inpu.x + 5 + \
                    self.inpu.fonte.size(
                        self.inpu.amostra[:self.inpu.cursor])[0]
                local_escolhido = self.inpu.x + self.inpu.w * self.inpu.cursor - 1
                pygame.draw.rect(self.screen, [10, 10, 10], [
                                 local_escolhido, self.inpu.y, 1, self.inpu.h - 5])

        pygame.display.flip()

    def main_loop(self):
        """o loop principal da janela, onde a atualização da tela é chamada e
        eventos são lidos"""
        run = True
        while run:
            self.atualizar_janela()
            for event in pygame.event.get(): # filtragem de eventos
                if event.type == pygame.QUIT: # fechar a janela
                    run = False

                elif event.type == pygame.MOUSEBUTTONUP: # click
                    pos = pygame.mouse.get_pos()
                    self.click(pos)

                elif event.type == pygame.KEYDOWN: # envio de caracteres ao input selecionado
                    numeros = "0123456789"
                    letras_min = "abcdefghijklmnopqrstuvwxyz"
                    letras_mai = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    especiais = "+-=*/,.()"
                    opções = numeros + letras_min + letras_mai + especiais # caracteres possiveis
                    if self.inpu is not None:
                        indice = self.inpu.cursor + self.inpu.indice_am # posição do cursor relativa a todo o seu conteudo

                    else:
                        indice = 0

                    if event.unicode in opções and event.unicode != "": # adicionando uma letra ao input
                        if self.inpu is not None:
                            self.inpu.input = self.inpu.input[:indice] + \
                                event.unicode + self.inpu.input[indice:]
                            self.inpu.cursor += 1

                    elif str(event.key) == "32": # adicionando 'espaço' ao input
                        if self.inpu is not None:
                            self.inpu.input = self.inpu.input[:indice] + \
                                " " + self.inpu.input[indice:]
                            self.inpu.cursor = min(
                                self.inpu.cursor + 1, len(self.inpu.amostra))

                    elif str(event.key) == "8": # usando 'backspace'
                        if self.inpu is not None:
                            fatia_ante = self.inpu.input[:indice - 1]
                            fatia_pos = self.inpu.input[indice:]
                            self.inpu.input = fatia_ante + fatia_pos
                            self.inpu.cursor = max(0, self.inpu.cursor - 1)

                    elif str(event.key) == "1073741904": # seta para esquerda
                        if self.inpu is not None:
                            self.inpu.cursor = self.inpu.cursor - 1
                            self.inpu.gerar_amostra()

                    elif str(event.key) == "1073741903": # seta para direita
                        if self.inpu is not None:
                            self.inpu.cursor = self.inpu.cursor + 1
                            self.inpu.gerar_amostra()

                    elif str(event.key) == "13":
                        pass


class Botao:
    """padroniza o comportamento de cada botão"""
    def __init__(self, x: int, y: int, w: int, h: int, conteudo: str,
                 nome: str, tamanho: int, cor: list, func, inputs: dict = {}):
        """recebe a posição do botão, suas dimensoes, seu conteudo a ser mostrado,
        seu nome a ser usado no programa, o tamanho da sua fonte, sua cor, um objeto
        'function' e os inputs (kwargs) de sua função"""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.conteudo = conteudo
        self.nome = nome
        self.tamanho = tamanho
        self.cor = cor
        self.func = func
        self.inputs = inputs
        self.fonte = pygame.font.Font(pygame.font.get_default_font(), tamanho)
        self.formatar()
        self.campo_min = [self.x, self.y] # area a ser considerada pelo click
        self.campo_max = [self.x + self.w, self.y + self.h]

    def formatar(self):
        """formata o botão para caber o texto, se as dimensoes foram zero"""
        if self.h == 0:
            self.h = self.fonte.size(self.conteudo)[1]

        if self.w == 0:
            self.w = self.fonte.size(self.conteudo)[0] + 10

    def click(self):
        """chama a função do botão com seus inputs"""
        self.func(**self.inputs)


class Texto:
    """padroniza o comportamento de cada texto"""
    def __init__(self, x: int, y: int, tamanho: int, conteudo: str, nome: str):
        """recebe a posição, tamanho da fonte, o conteudo do texto e o nome a ser
        usado internamente"""
        self.x = x
        self.y = y
        self.tamanho = tamanho
        self.conteudo = conteudo
        self.nome = nome
        self.fonte = pygame.font.Font(pygame.font.get_default_font(), tamanho)

    def printar(self):
        """formata o texto em uma lista de linhas e a retorna para ser printada na tela"""
        lista = []
        y = self.y
        for texto in self.conteudo.split("\n"):
            textsurface = self.fonte.render(texto, False, (10, 10, 10))
            lista.append([textsurface, self.x, y])
            y += self.tamanho

        return lista


class Inp:
    """padroniza o comportamento de cada input de texto"""
    def __init__(self, x: int, y: int, maximo: int, tamanho: int,
                 input: str = "", nome: str = ""):
        """recebe a posição, o maximo de caracteres viziveis, o tamanho da fonte,
        o conteudo default e o nome a ser usado internamente"""
        self.tamanho = tamanho
        self.fonte = pygame.font.Font(
            pygame.font.get_default_font(), self.tamanho)
        self.x = x
        self.y = y
        self.maximo = maximo
        self.w = self.fonte.size("w")[0] + 1
        self.h = self.fonte.size("w")[1]
        self.cor = [245, 245, 245]
        self.input = input
        self.nome = nome
        self.cursor = 0 # posição do cursor
        self.indice_am = 0 # indice referente a primeira letra a mostra em relação ao conteudo inteiro
        self.amostra = self.input # a pequena amostra a qual ficara a mostra
        self.campo_min = [self.x, self.y] # area a ser considerada pelo click
        self.campo_max = [self.x + self.w * self.maximo, self.y + self.h]

    def gerar_amostra(self):
        """gerar nova amostra de texto para acomodar uma mudança nos caracteres ou
        na posição do cursor"""
        self.amostra = self.input[self.indice_am:]
        if self.cursor < 0 and self.indice_am > 0: # se o cursor estiver fora da amostra para a esquerda
            self.indice_am += -1
            maximo = min(self.indice_am + self.maximo,
                         len(self.input) - self.indice_am)
            self.amostra = self.input[self.indice_am:maximo]
            self.cursor += 1

        elif self.cursor > self.maximo: # se o cursor estiver fora da amostra para a direita
            self.cursor += -1
            final = self.indice_am + self.maximo
            if final <= len(self.input):
                self.indice_am += 1
                self.amostra = self.input[self.indice_am:final]

        if len(self.amostra) > self.maximo: # se a amostra for maior do que a parmitida
            if self.cursor < self.maximo:
                self.amostra = self.amostra[:-1]

            elif self.cursor == self.maximo:
                self.amostra = self.amostra[1:]
