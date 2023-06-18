from constants import LARGURA_TABULEIRO, ALTURA_TABULEIRO, LARGURA_CASA, COMPRIMENTO_LADO

def get_board_house_coordinates(index):
    espaco = (LARGURA_TABULEIRO - LARGURA_CASA) / (COMPRIMENTO_LADO - 1)
    x, y = 0, 0
    if index < COMPRIMENTO_LADO:
        x = index * espaco
        y = 0
    elif index < 2 * COMPRIMENTO_LADO - 1:
        x = LARGURA_TABULEIRO - LARGURA_CASA
        y = (index - COMPRIMENTO_LADO + 1) * espaco
    elif index < 3 * COMPRIMENTO_LADO - 2:
        x = LARGURA_TABULEIRO - LARGURA_CASA - (index - 2 * COMPRIMENTO_LADO + 2) * espaco
        y = ALTURA_TABULEIRO - LARGURA_CASA
    else:
        x = 0
        y = ALTURA_TABULEIRO - LARGURA_CASA - (index - 3 * COMPRIMENTO_LADO + 3) * espaco
    return x, y