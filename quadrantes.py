from enum import Enum

class Quadrante_1(Enum):
    CIMA = slice(None,3,None)
    DIREITA = slice(2,15,6)
    BAIXO = slice(12,15,None)
    ESQUERDA = slice(None,13,6)

class Quadrante_2(Enum):
    CIMA = slice(3,6,None)
    DIREITA = slice(5,18,6)
    BAIXO = slice(15,18,None)
    ESQUERDA = slice(3,16,6)

class Quadrante_3(Enum):
    CIMA = slice(18,21,None)
    DIREITA = slice(20,33,6)
    BAIXO = slice(30,33,None)
    ESQUERDA = slice(18,31,6)

class Quadrante_4(Enum):
    CIMA = slice(21,24,None)
    DIREITA = slice(23,None,6)
    BAIXO = slice(33,None,None)
    ESQUERDA = slice(21,34,6)
