import pygame
import random

# Inicializar Pygame
pygame.init()

# Obter as dimensões de fundo
size = (800, 600)

# Criar a tela
tela = pygame.display.set_mode(size)
pygame.display.set_caption("Bat, o abacate") # Adiciona o título na janela

# Carregar a imagem de fundo
fundo_jogo1 = pygame.image.load('jogo1.png')
fundo_jogo2 = pygame.image.load('jogo2.png')
fundo_inicial = pygame.image.load('fundo.jpeg')

# Redimensionar as imagens para caber na tela
fundo_jogo1 = pygame.transform.scale(fundo_jogo1, size)
fundo_jogo2 = pygame.transform.scale(fundo_jogo2, size)
fundo_inicial = pygame.transform.scale(fundo_inicial, size)

# Definir algumas constantes
COR_FUNDO = (255, 255, 255)
TAMANHO_FONTE = 18
COR_FONTE = (255, 108, 151)
COR_BOTAO = (119, 255, 108)
FONTE_BOTAO = 'Titan_One/TitanOne-Regular.ttf'
PADDING_BOTAO = 10
ESPACAMENTO_BOTAO = 10
TITULO_JOGO = "Bat, o abacate na guerra pela saúde"  # Título do jogo
n = 0

# Criar a fonte
fonte = pygame.font.Font(FONTE_BOTAO, TAMANHO_FONTE)
fonte_titulo = pygame.font.Font(FONTE_BOTAO, TAMANHO_FONTE + 10)  # Fonte maior para o título

# Criar os botões
largura_botao = fundo_inicial.get_width() // 2  # Reduzir a largura do botão pela metade
altura_botao = TAMANHO_FONTE + 2 * PADDING_BOTAO
botao_iniciar = pygame.Rect(
    (size[0] // 2 - largura_botao // 2, size[1] // 2 - altura_botao - ESPACAMENTO_BOTAO, largura_botao, altura_botao))  
botao_regras = pygame.Rect(
    (size[0] // 2 - largura_botao // 2, size[1] // 2 + ESPACAMENTO_BOTAO, largura_botao, altura_botao))

# Defina o novo tamanho
novo_tamanho = (100, 100)

# Carregar e redimensionar imagens do personagem
imagens_abacate = {
    'direita': pygame.transform.scale(pygame.image.load('Bat o abacate/bat_direita.png'), novo_tamanho),
    'esquerda': pygame.transform.scale(pygame.image.load('Bat o abacate/bat_esquerda.png'), novo_tamanho),
    'inicio': pygame.transform.scale(pygame.image.load('Bat o abacate/bat.png'), novo_tamanho),
    'pulo': pygame.transform.scale(pygame.image.load('Bat o abacate/bat_pulo.png'), novo_tamanho)
}

# Crie um dicionário para rastrear se uma tecla está pressionada
teclas_pressionadas = {
    'UP': False,
    'DOWN': False,
    'LEFT': False,
    'RIGHT': False
}

# Definir a posição inicial do bat
posicao_bat = [size[0] // 2, size[1] // 2]

# Definir a velocidade de movimento do bat
velocidade_bat = 2

# Definir o tamanho dos elementos
tamanho_elemento = (40, 40)
# Carregar e redimensionar elementos
try:
    elementos_wins = {
        'leandro': pygame.transform.scale(pygame.image.load('wins/morango.png'), tamanho_elemento),
        'pera': pygame.transform.scale(pygame.image.load('wins/pera.png'), tamanho_elemento),
        'laranja': pygame.transform.scale(pygame.image.load('wins/laranja.png'), tamanho_elemento),    
        'cenoura': pygame.transform.scale(pygame.image.load('wins/cenoura.png'), tamanho_elemento),
        'brocolis': pygame.transform.scale(pygame.image.load('wins/brocolis.png'), tamanho_elemento),
        'batata' : pygame.transform.scale(pygame.image.load('wins/batata.png'), tamanho_elemento)
    }

    elementos_eca = {
        'donut': pygame.transform.scale(pygame.image.load('eca/donut.png'), tamanho_elemento),
        'pizza': pygame.transform.scale(pygame.image.load('eca/pizza.png'), tamanho_elemento),
        'chocolate': pygame.transform.scale(pygame.image.load('eca/chocolate.png'), tamanho_elemento),
        'batata_frita': pygame.transform.scale(pygame.image.load('eca/batata-frita.png'), tamanho_elemento)
    }
except Exception as e:
    print(f"Erro ao carregar imagens: {e}")

# Carregar e redimensionar imagens do vilão
imagens_burgo = {
    'burgo': pygame.transform.scale(pygame.image.load('Burgo o hamburgo/burgo.png'), novo_tamanho),
    'ripburgo': pygame.transform.scale(pygame.image.load('Burgo o hamburgo/burgo.png'), novo_tamanho)
}

# Armazena num vetor a Velocidade de movimentacao dos elementos
velocidade_queda = 3

# Variável para armazenar os elementos e a posição dos elementos
elementos = []
posicoes_elementos = []

# Definir variáveis do jogo
pontos = 0
vidas = 3
niveis = 3
nivel_atual = 1 
jogo_iniciado = False  # Adicionado para controlar se o jogo foi iniciado ou não

# Definir as velocidades de Burgo para cada nível
velocidades_burgo = {
    1: 2,  # Velocidade no nível 1
    2: 4,  # Velocidade no nível 2
    3: 6   # Velocidade no nível 3
}

# Definir a posição inicial de Burgo
posicao_burgo = [0, 0]  # Começa no canto superior esquerdo

# Função para atualizar a posição de Burgo e verificar a transição de nível
def atualizar_burgo(nivel_atual, posicao_burgo, velocidades_burgo):
    posicao_burgo[0] += velocidades_burgo[nivel_atual]
    # Se Burgo saiu da tela, reinicie sua posição
    if posicao_burgo[0] > size[0]:
        posicao_burgo[0] = 0

# Função para verificar a vitória e avançar de nível
def verificar_vitoria(posicao_bat, nivel_atual):
    global ganhou_nivel
    if posicao_bat[1] <= 0:  # Se Bat alcançou o topo da tela
        ganhou_nivel = True
        nivel_atual += 1
        return True
    return False

# Função para iniciar o próximo nível
def iniciar_proximo_nivel(nivel_atual):
    if nivel_atual > niveis:
        mostrar_tela_vitoria()
        return True
    else:
        atualizar_burgo(nivel_atual, posicao_burgo, velocidades_burgo)
        return False

# Função para mostrar a tela de vitória
def mostrar_tela_vitoria():
    # Carregar e exibir a imagem de vitória
    tela_vitoria = pygame.image.load('gamewin.jpeg')
    tela_vitoria = pygame.transform.scale(tela_vitoria, size)
    tela.blit(tela_vitoria, (0, 0))
    pygame.display.flip()
    pygame.time.wait(5000)  # Esperar por 5 segundos antes de fechar o jogo


# Função para desenhar o contador de pontos e vidas
def desenhar_contadores(tela, pontos, vidas):
    fonte_pontos = pygame.font.Font(None, 36)
    texto_pontos = fonte_pontos.render(f'Pontos: {pontos}', True, (0, 0, 0))
    tela.blit(texto_pontos, (10, 10))

    fonte_vidas = pygame.font.Font(None, 36)
    texto_vidas = fonte_vidas.render(f'Vidas: {vidas}', True, (0, 0, 0))
    tela.blit(texto_vidas, (size[0] - 110, 10))

# Função para criar um novo elemento em uma posição aleatória na parte superior da tela
def criar_elemento():
    print("Criando elemento...")
    # Criar uma lista com todos os elementos
    todos_elementos = list(elementos_wins.values()) + list(elementos_eca.values())
    # Escolher um elemento aleatoriamente
    elemento = random.choice(todos_elementos)
    # Adicionar o elemento à lista de elementos
    elementos.append(elemento)
    # Criar uma posição aleatória na parte superior da tela para o elemento
    posicao = [random.randint(0, size[0] - novo_tamanho[0]), 0]
    # Adicionar a posição à lista de posições dos elementos
    posicoes_elementos.append(posicao)

# Função para atualizar as posições dos elementos
def atualizar_elementos():
    global pontos, vidas, criar
    # Criar cópias das listas
    elementos_copia = elementos[:]
    posicoes_elementos_copia = posicoes_elementos[:]
    for i in range(len(elementos_copia) - 1, -1, -1):  # Iterar de trás para frente
        # Atualizar a posição y do elemento para fazê-lo cair
        posicoes_elementos[i][1] += velocidade_queda
        # Se o elemento saiu da tela, removê-lo
        if posicoes_elementos[i][1] > size[1]:
            del elementos[i]
            del posicoes_elementos[i]
            # Criar um novo elemento para substituir o antigo
            criar = True
        # Se o personagem encostar no elemento, o elemento é reiniciado
        elif (posicao_bat[1] + novo_tamanho[1] >= posicoes_elementos[i][1] - novo_tamanho[1] and posicao_bat[1] - novo_tamanho[1] <= posicoes_elementos[i][1] + novo_tamanho[1]) and (posicao_bat[0] + novo_tamanho[0] >= posicoes_elementos[i][0] - novo_tamanho[0] and posicao_bat[0] - novo_tamanho[0] <= posicoes_elementos[i][0] + novo_tamanho[0]):
            if elementos_copia[i] in elementos_wins.values():
                pontos += 1
                if pontos % 5 == 0:
                    vidas += 1
                    pontos = 0  # Zerar pontuação
                    pygame.mixer.music.load('som/catch.mp3')
                    pygame.mixer.music.play(0)
            else:
                vidas -= 1
            del elementos[i]
            del posicoes_elementos[i]
            criar = True

# Função para desenhar os elementos na tela
def desenhar_elementos(tela):
    for i in range(len(elementos)):
        tela.blit(elementos[i], posicoes_elementos[i])

# Adicionar uma variável para rastrear o tempo desde a última vez que um elemento foi criado
tempo_ultimo_elemento = pygame.time.get_ticks()

# Definir a posição inicial de Burgo
posicao_burgo = [0, 0]  # Começa no canto superior esquerdo

# Definir a velocidade de movimento de Burgo
velocidade_burgo_nivel2 = 3
velocidade_burgo_nivel3 = 5  # Mais rápido no nível 3

# Carregar e redimensionar imagens do vilão
imagens_burgo = {
    'burgo': pygame.transform.scale(pygame.image.load('Burgo o hamburgo/burgo.png'), novo_tamanho),
    'ripburgo': pygame.transform.scale(pygame.image.load('Burgo o hamburgo/burgo.png'), novo_tamanho)
}

def nivel(n):
    global posicao_burgo
    # Atualizar a posição de Burgo
    if n == 2:
        posicao_burgo[0] += velocidade_burgo_nivel2
        # Se Burgo saiu da tela, reinicie sua posição
        if posicao_burgo[0] > size[0]:
            posicao_burgo[0] = 0
        # Se Bat está no canto superior da tela
        if posicao_bat[1] <= 0:
            # Mudar a sprite de Burgo para ripburgo
            tela.blit(imagens_burgo['ripburgo'], posicao_burgo)
            pygame.display.flip()
            pygame.time.wait(3000)  # Esperar por 3 segundos
            # Exibir a tela de vitória
            tela_vitoria = pygame.image.load('gamewin.jpeg')
            tela_vitoria = pygame.transform.scale(tela_vitoria, size)
            tela.blit(tela_vitoria, (0, 0))
        else:
            # Desenhar Burgo na tela
            tela.blit(imagens_burgo['burgo'], posicao_burgo)


def nivel3():
    global posicao_burgo
    # Atualizar a posição de Burgo
    if n == 3:
        posicao_burgo[0] += velocidade_burgo_nivel3
        # Se Burgo saiu da tela, reinicie sua posição
        if posicao_burgo[0] > size[0]:
            posicao_burgo[0] = 0
        # Se Bat está no canto superior da tela
        if posicao_bat[1] <= 0:
            # Mudar a sprite de Burgo para ripburgo
            tela.blit(imagens_burgo['ripburgo'], posicao_burgo)
            pygame.display.flip()
            pygame.time.wait(3000)  # Esperar por 3 segundos
            # Exibir a tela de vitória
            tela_vitoria = pygame.image.load('gamewin.jpeg')
            tela_vitoria = pygame.transform.scale(tela_vitoria, size)
            tela.blit(tela_vitoria, (0, 0))
        else:
            # Desenhar Burgo na tela
            tela.blit(imagens_burgo['burgo'], posicao_burgo)

ganhou_nivel = False

# Loop principal do jogo
executando = True
while executando:
    # Tratar eventos
    n = 1
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_iniciar.collidepoint(evento.pos):
                jogo_iniciado = True
                criar_elemento() #cria novo elemento
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                teclas_pressionadas['UP'] = True
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                teclas_pressionadas['DOWN'] = True
            elif evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                teclas_pressionadas['LEFT'] = True
            elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                teclas_pressionadas['RIGHT'] = True
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                teclas_pressionadas['UP'] = False
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                teclas_pressionadas['DOWN'] = False
            elif evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                teclas_pressionadas['LEFT'] = False
            elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                teclas_pressionadas['RIGHT'] = False
    # Chamar a função nivel com o nível atual
    if jogo_iniciado:  # Certifique-se de que o jogo foi iniciado
        nivel(nivel_atual)

    # Atualizar a posição de Burgo e verificar a transição de nível
    if jogo_iniciado:
        atualizar_burgo(nivel_atual, posicao_burgo, velocidades_burgo)

        # Verificar se o jogador ganhou e avançar para o próximo nível
        if verificar_vitoria(posicao_bat, nivel_atual):
            # Iniciar o próximo nível ou mostrar a tela de vitória
            if iniciar_proximo_nivel(nivel_atual):
                break  # Sai do loop se todos os níveis foram concluído

    # Verificar se passou tempo suficiente desde a última vez que um elemento foi criado
    if pygame.time.get_ticks() - tempo_ultimo_elemento > 2000:  # 2000 milissegundos = 2 segundos
        criar_elemento()
        tempo_ultimo_elemento = pygame.time.get_ticks()

    # Atualizar e desenhar elementos
    atualizar_elementos()
    desenhar_elementos(tela)
    
    # Verificar se o jogador ganhou
    if posicao_bat[1] <= 0:  # Se a posição y do jogador é 0 ou menor
        # Carregar e exibir a imagem de vitória
        tela_vitoria = pygame.image.load('gamewin.jpeg')
        tela_vitoria = pygame.transform.scale(tela_vitoria, size)
        tela.blit(tela_vitoria, (0, 0))
        ganhou_nivel = True
        n += 1

        # Exibir a mensagem de vitória
        fonte_vitoria = pygame.font.Font(None, 50)
        texto_vitoria = fonte_vitoria.render('Você passou para o próximo nível!', True, (0, 0, 0))
        tela.blit(texto_vitoria, (size[0] / 2 - texto_vitoria.get_width() / 2, size[1] / 2 - texto_vitoria.get_height() / 2))

        pygame.display.flip()
        pygame.time.wait(500)  # Esperar por 5 segundos antes de ir para o próximo nível

    # Adiciona o código para iniciar o próximo nível
    if ganhou_nivel:
        if nivel_atual == 2:
            nivel(n)
        elif nivel_atual == 3:
            nivel(n)
        ganhou_nivel = False

    # Verificar se o jogo acabou
    if vidas <= 0:
        # Carregar e exibir a tela de Game Over
        tela_game_over = pygame.image.load('gameover.jpeg') 
        tela_game_over = pygame.transform.scale(tela_game_over, size)
        tela.blit(tela_game_over, (0, 0))
        pygame.display.flip()
        pygame.time.wait(5000)  # Esperar por 5 segundos antes de fechar o jogo
        executando = False  # Sair do loop do jogo

    # Fora do loop de eventos, atualize a posição do personagem com base nas teclas pressionadas
    if teclas_pressionadas['UP'] and posicao_bat[1] - velocidade_bat >= 0:
        posicao_bat[1] -= velocidade_bat
    if teclas_pressionadas['DOWN'] and posicao_bat[1] + velocidade_bat <= size[1] - novo_tamanho[1]:
        posicao_bat[1] += velocidade_bat
    if teclas_pressionadas['LEFT'] and posicao_bat[0] - velocidade_bat >= 0:
        posicao_bat[0] -= velocidade_bat
    if teclas_pressionadas['RIGHT'] and posicao_bat[0] + velocidade_bat <= size[0] - novo_tamanho[0]:
        posicao_bat[0] += velocidade_bat

    # Preencher a tela com a cor de fundo
    tela.fill(COR_FUNDO)

    # Desenhar o fundo
    if jogo_iniciado:
        if fundo_inicial == fundo_jogo1:
            tela.blit(fundo_jogo1, (0, 0))
        else:
            tela.blit(fundo_jogo2, (0, 0))
        # Atualizar e desenhar elementos
        atualizar_elementos()
        desenhar_elementos(tela)
        # Desenhar o jogador (bat) no centro da tela
        if teclas_pressionadas['UP']:
            tela.blit(imagens_abacate['pulo'], (posicao_bat[0], posicao_bat[1]))
        elif teclas_pressionadas['LEFT']:
            tela.blit(imagens_abacate['esquerda'], (posicao_bat[0], posicao_bat[1]))
        elif teclas_pressionadas['RIGHT']:
            tela.blit(imagens_abacate['direita'], (posicao_bat[0], posicao_bat[1]))
        else:
            tela.blit(imagens_abacate['inicio'], (posicao_bat[0], posicao_bat[1]))

    else:
        tela.blit(fundo_inicial, (0, 0))
        # Desenhar os botões
        pygame.draw.rect(tela, COR_BOTAO, botao_iniciar)
        pygame.draw.rect(tela, COR_BOTAO, botao_regras)

        # Desenhar o texto dos botões
        superficie_texto = fonte.render("START", True, COR_FONTE)
        posicao_texto = superficie_texto.get_rect(center=botao_iniciar.center)
        tela.blit(superficie_texto, posicao_texto)

        superficie_texto = fonte.render("INSTRUÇÕES", True, COR_FONTE)
        posicao_texto = superficie_texto.get_rect(center=botao_regras.center)
        tela.blit(superficie_texto, posicao_texto)

        # Desenhar o título do jogo na tela
        superficie_titulo = fonte_titulo.render(TITULO_JOGO, True, COR_FONTE)
        posicao_titulo = superficie_titulo.get_rect(center=(size[0] // 2, size[1] // 10))
        tela.blit(superficie_titulo, posicao_titulo)

    # Atualizar a tela
    pygame.display.flip()

    # Desenhar contadores de pontos e vidas
    desenhar_contadores(tela, pontos, vidas)

    # Atualizar a tela
    pygame.display.flip()

# Encerrar Pygame
pygame.quit()
