import pygame
import random
import sys

# --- CONSTANTES ---
LARGURA, ALTURA = 600, 600
DIMENSAO = 10
TAMANHO_QUAD = LARGURA // DIMENSAO
CORES = {
    "MAR": (10, 30, 60),
    "BORDA": (20, 50, 100),
    "ERRO": (15, 15, 30),
    "TEXTO": (255, 255, 255)
}

class Tabuleiro:
    """Gerencia a lógica da matriz e posicionamento de itens."""
    def __init__(self):
        self.grade = [[0 for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]
        self.bombas = self._sortear_posicoes(3, [])
        self.navios = self._sortear_posicoes(10, self.bombas)
        self.acertos = 0

    def _sortear_posicoes(self, qtd, proibidas):
        posicoes = []
        while len(posicoes) < qtd:
            p = (random.randint(0, 9), random.randint(0, 9))
            if p not in posicoes and p not in proibidas:
                posicoes.append(p)
        return posicoes

class Visual:
    """Gerencia o carregamento de mídia e desenhos na tela."""
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.SysFont("Impact", 42)
        # Nomes de arquivos atualizados conforme seu pedido
        self.img_navio = self._carregar("NavioDeGuerra.png")
        self.img_bomba = self._carregar("bomba-28023.jpg")

    def _carregar(self, nome):
        try:
            img = pygame.image.load(nome).convert_alpha()
            return pygame.transform.scale(img, (TAMANHO_QUAD - 4, TAMANHO_QUAD - 4))
        except Exception as e:
            print(f"Aviso: Não foi possível carregar {nome}. Erro: {e}")
            return None

    def desenhar_msg(self, texto, cor):
        surf = self.fonte.render(texto, True, cor)
        x = (LARGURA - surf.get_width()) // 2
        y = (ALTURA - surf.get_height()) // 2
        self.tela.blit(surf, (x, y))

class MotorJogo:
    """Classe principal que integra Lógica (Tabuleiro) e Visual."""
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Batalha Naval OO - Tema 2")
        
        self.logica = Tabuleiro()
        self.visual = Visual(self.tela)
        self.estado = "JOGANDO"

    def processar_clique(self, pos):
        if self.estado != "JOGANDO": return
        
        c, l = pos[0] // TAMANHO_QUAD, pos[1] // TAMANHO_QUAD
        
        if (l, c) in self.logica.bombas:
            self.logica.grade[l][c] = "B"
            self.estado = "DERROTA"
        elif (l, c) in self.logica.navios:
            if self.logica.grade[l][c] != "N":
                self.logica.grade[l][c] = "N"
                self.logica.acertos += 1
                if self.logica.acertos == 10:
                    self.estado = "VITORIA"
        else:
            self.logica.grade[l][c] = "E"

    def atualizar_tela(self):
        self.tela.fill((0, 0, 0))
        for l in range(DIMENSAO):
            for c in range(DIMENSAO):
                rect = pygame.Rect(c*TAMANHO_QUAD, l*TAMANHO_QUAD, TAMANHO_QUAD, TAMANHO_QUAD)
                pygame.draw.rect(self.tela, CORES["MAR"], rect)
                pygame.draw.rect(self.tela, CORES["BORDA"], rect, 1)

                celula = self.logica.grade[l][c]
                if celula == "E":
                    pygame.draw.rect(self.tela, CORES["ERRO"], rect)
                elif celula == "N":
                    if self.visual.img_navio: self.tela.blit(self.visual.img_navio, (rect.x+2, rect.y+2))
                    else: pygame.draw.circle(self.tela, (0, 255, 0), rect.center, 15)
                elif celula == "B":
                    if self.visual.img_bomba: self.tela.blit(self.visual.img_bomba, (rect.x+2, rect.y+2))
                    else: pygame.draw.circle(self.tela, (255, 0, 0), rect.center, 15)

        if self.estado == "DERROTA":
            self.visual.desenhar_msg("EXPLOSÃO! NAVIO AFUNDADO", (255, 50, 50))
        elif self.estado == "VITORIA":
            self.visual.desenhar_msg("VITÓRIA! NAVIOS ENCONTRADOS", (50, 255, 50))

        pygame.display.flip()

    def iniciar(self):
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.processar_clique(pygame.mouse.get_pos())
            
            self.atualizar_tela()

if __name__ == "__main__":
    jogo = MotorJogo()
    jogo.iniciar()