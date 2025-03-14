from enum import Enum

class Quadrante_1(Enum):
    CIMA = slice(None,3,None)
    DIREITA = slice(2,15,6)
    BAIXO = slice(12,15,None)
    ESQUERDA = slice(None,13,6)
    DIAGONAL_DIREITA = slice(None,15,7)
    DIAGONAL_ESQUERDA = slice(2,13,5)
    CENTRO_VERTICAL = slice(1,14,6)
    CENTRO_HORIZINTAL = slice(6,9,None)

class Quadrante_2(Enum):
    CIMA = slice(3,6,None)
    DIREITA = slice(5,18,6)
    BAIXO = slice(15,18,None)
    ESQUERDA = slice(3,16,6)
    DIAGONAL_DIREITA = slice(3,18,7)
    DIAGONAL_ESQUERDA = slice(5,16,5)
    CENTRO_VERTICAL = slice(4,17,6)
    CENTRO_HORIZINTAL = slice(9,11,None)

class Quadrante_3(Enum):
    CIMA = slice(18,21,None)
    DIREITA = slice(20,33,6)
    BAIXO = slice(30,33,None)
    ESQUERDA = slice(18,31,6)
    DIAGONAL_DIREITA = slice(18,33,7)
    DIAGONAL_ESQUERDA = slice(20,31,5)
    CENTRO_VERTICAL = slice(19,32,6)
    CENTRO_HORIZINTAL = slice(24,26,None)

class Quadrante_4(Enum):
    CIMA = slice(21,24,None)
    DIREITA = slice(23,None,6)
    BAIXO = slice(33,None,None)
    ESQUERDA = slice(21,34,6)
    DIAGONAL_DIREITA = slice(25,None,7)
    DIAGONAL_ESQUERDA = slice(23,34,5)
    CENTRO_VERTICAL = slice(22,35,6)
    CENTRO_HORIZINTAL = slice(27,29,None)