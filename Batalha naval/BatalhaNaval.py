import pygame
import random
import sys

# Configurações de Tela
LARGURA, ALTURA = 600, 600
DIMENSAO = 10
TAMANHO_QUADRADO = LARGURA // DIMENSAO

# Cores
AZUL_ESCURO = (10, 30, 60)
COR_BORDA = (20, 50, 100)
COR_ERRO = (15, 15, 30)
COR_MENSAGEM = (255, 255, 255)

class BatalhaNavalFinal:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Batalha Naval: Missão de Busca")
        self.fonte = pygame.font.SysFont("Impact", 45)
        
        # Carregamento de imagens
        self.img_navio = self.carregar_img("NavioDeGuerra.png")
        self.img_bomba = self.carregar_img("bomba-28023.jpg")

        self.tabuleiro = [[0 for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]
        self.navios_encontrados = 0
        self.estado_jogo = "JOGANDO" # JOGANDO, VITORIA, DERROTA

        # Sorteio de Bombas e Navios
        self.pos_bombas = self.sortear_posicoes(3, [])
        self.pos_navios = self.sortear_posicoes(10, self.pos_bombas)

    def sortear_posicoes(self, quantidade, proibidas):
        lista = []
        while len(lista) < quantidade:
            p = (random.randint(0, 9), random.randint(0, 9))
            if p not in lista and p not in proibidas:
                lista.append(p)
        return lista

    def carregar_img(self, nome):
        try:
            img = pygame.image.load(nome).convert_alpha()
            return pygame.transform.scale(img, (TAMANHO_QUADRADO - 4, TAMANHO_QUADRADO - 4))
        except: return None

    def desenhar(self):
        self.tela.fill((0, 0, 0))
        for l in range(DIMENSAO):
            for c in range(DIMENSAO):
                rect = pygame.Rect(c*TAMANHO_QUADRADO, l*TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO)
                
                # Fundo Padrão
                pygame.draw.rect(self.tela, AZUL_ESCURO, rect)
                pygame.draw.rect(self.tela, COR_BORDA, rect, 1)

                # Revelar conteúdo
                if self.tabuleiro[l][c] == "E":
                    pygame.draw.rect(self.tela, COR_ERRO, rect)
                elif self.tabuleiro[l][c] == "N":
                    if self.img_navio: self.tela.blit(self.img_navio, (rect.x+2, rect.y+2))
                    else: pygame.draw.circle(self.tela, (0, 255, 0), rect.center, 15)
                elif self.tabuleiro[l][c] == "B":
                    if self.img_bomba: self.tela.blit(self.img_bomba, (rect.x+2, rect.y+2))
                    else: pygame.draw.circle(self.tela, (255, 0, 0), rect.center, 15)

        # Mensagens de Fim de Jogo
        if self.estado_jogo != "JOGANDO":
            txt = "EXPLOSÃO! NAVIO AFUNDADO" if self.estado_jogo == "DERROTA" else "VITÓRIA! NAVIOS ENCONTRADOS"
            cor = (255, 50, 50) if self.estado_jogo == "DERROTA" else (50, 255, 50)
            superficie = self.fonte.render(txt, True, cor)
            # Centralizar mensagem
            pos_x = (LARGURA - superficie.get_width()) // 2
            pos_y = (ALTURA - superficie.get_height()) // 2
            self.tela.blit(superficie, (pos_x, pos_y))

    def rodar(self):
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if ev.type == pygame.MOUSEBUTTONDOWN and self.estado_jogo == "JOGANDO":
                    x, y = pygame.mouse.get_pos()
                    c, l = x // TAMANHO_QUADRADO, y // TAMANHO_QUADRADO

                    if (l, c) in self.pos_bombas:
                        self.tabuleiro[l][c] = "B"
                        self.estado_jogo = "DERROTA"
                    elif (l, c) in self.pos_navios:
                        if self.tabuleiro[l][c] != "N":
                            self.tabuleiro[l][c] = "N"
                            self.navios_encontrados += 1
                            if self.navios_encontrados == 10:
                                self.estado_jogo = "VITORIA"
                    else:
                        self.tabuleiro[l][c] = "E"

            self.desenhar()
            pygame.display.flip()

if __name__ == "__main__":
    BatalhaNavalFinal().rodar()