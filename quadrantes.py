from enum import Enum

class Quadrante_1(Enum):
    DOMINIO = [0,1,2,6,7,8,12,13,14]
    CIMA = slice(None,3,None)
    DIREITA = slice(2,15,6)
    BAIXO = slice(12,15,None)
    ESQUERDA = slice(None,13,6)
    DIAGONAL_DIREITA = slice(None,15,7)
    #DIAGONAL_ESQUERDA = slice(2,13,5)
    CENTRO_VERTICAL = slice(1,14,6)
    CENTRO_HORIZINTAL = slice(6,9,None)

class Quadrante_2(Enum):
    DOMINIO = [3,4,5,9,10,11,15,16,17]
    CIMA = slice(3,6,None)
    DIREITA = slice(5,18,6)
    BAIXO = slice(15,18,None)
    ESQUERDA = slice(3,16,6)
    #DIAGONAL_DIREITA = slice(3,18,7)
    DIAGONAL_ESQUERDA = slice(5,16,5)
    CENTRO_VERTICAL = slice(4,17,6)
    CENTRO_HORIZINTAL = slice(9,12,None)

class Quadrante_3(Enum):
    DOMINIO = [18,19,20,24,25,26,30,31,32]
    CIMA = slice(18,21,None)
    DIREITA = slice(20,33,6)
    BAIXO = slice(30,33,None)
    ESQUERDA = slice(18,31,6)
    #DIAGONAL_DIREITA = slice(18,33,7)
    DIAGONAL_ESQUERDA = slice(20,31,5)
    CENTRO_VERTICAL = slice(19,32,6)
    CENTRO_HORIZINTAL = slice(24,27,None)

class Quadrante_4(Enum):
    DOMINIO = [21,22,23,27,28,29,33,34,35]
    CIMA = slice(21,24,None)
    DIREITA = slice(23,None,6)
    BAIXO = slice(33,None,None)
    ESQUERDA = slice(21,34,6)
    DIAGONAL_DIREITA = slice(21,None,7)
    #DIAGONAL_ESQUERDA = slice(23,34,5)
    CENTRO_VERTICAL = slice(22,35,6)
    CENTRO_HORIZINTAL = slice(27,30,None)