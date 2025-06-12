from quadrantes import Quadrante_1 as q1, Quadrante_2 as q2, Quadrante_3 as q3, Quadrante_4 as q4
from no import No


class Pentago():
    def __init__(self, estado, no=None):
        self.estado = estado
        self.no = no

    def imprimir(self, estado):
        return "|" + estado[0] + "|" + estado[1] + "|" + estado[2] + "|" + estado[3] + "|" + estado[4] + "|" + estado[5
                ] + "|" + "\n"+ "|" + estado[6] + "|" + estado[7] + "|" + estado[8] + "|" + estado[9] + "|" + estado[10] + "|" + estado[11
                ] + "|" + "\n" + "|" + estado[12] + "|" + estado[13] + "|" + estado[14] + "|" + estado[15] + "|" + estado[16] + "|" + estado[17
                ] + "|" + "\n" + "|" + estado[18] + "|" + estado[19] + "|" + estado[20] + "|" + estado[21] + "|" + estado[22] + "|" + estado[23
                ] + "|" + "\n" + "|" + estado[24] + "|" + estado[25] + "|" + estado[26] + "|" + estado[27] + "|" + estado[28] + "|" + estado[29
                ] + "|" + "\n" + "|" + estado[30] + "|" + estado[31] + "|" + estado[32] + "|" + estado[33] + "|" + estado[34] + "|" + estado[35] + "|"                                                                                                                                                                                                                                                                                                                                       
    
    def iniciar(self):
        self.no = No(self.estado)
        return self.no

    def jogadaValida(cls, estado, jogada):
        return estado[jogada["index"]] == "-"

    #funcção socessora
    def posicionarPeca(self, no_pai, jogada):
        estado_novo = no_pai.estado_antes_giro.copy() if no_pai.estado_apos_giro == None else no_pai.estado_apos_giro.copy()

        estado_novo[jogada["index"]] = jogada["corPeca"]
        
        print(self.imprimir(estado_novo))
        no_novo = No(estado_novo, no_pai)
        return no_novo
    
    def executarGiro(self, estado_novo, jogada):
        if jogada["direcao"] == "d":
            estado_novo = self.girarDireita(estado_novo, jogada["quadrante"])
        elif jogada["direcao"] == "e":
            estado_novo = self.girarEsquerda(estado_novo, jogada["quadrante"])

        return estado_novo

    def girarDireita(self, estado, quadrante):
        estado_novo = estado.copy()
        try:
            q = self.selecionarQuadranteGiro(quadrante)
        except Exception as erro:
            raise erro

        q_esquerda = estado[q.ESQUERDA.value]
        q_esquerda.reverse()

        q_direita = estado[q.DIREITA.value]
        q_direita.reverse()

        estado_novo[q.CIMA.value] = q_esquerda
        estado_novo[q.DIREITA.value] = estado[q.CIMA.value]
        estado_novo[q.BAIXO.value] = q_direita
        estado_novo[q.ESQUERDA.value] = estado[q.BAIXO.value]
        
        return estado_novo

    def girarEsquerda(self, estado, quadrante):
        estado_novo = estado.copy()

        try:
            q = self.selecionarQuadranteGiro(quadrante)
        except Exception as erro:
            raise erro

        q_cima = estado[q.CIMA.value]
        q_cima.reverse()

        q_baixo = estado[q.BAIXO.value]
        q_baixo.reverse()

        estado_novo[q.CIMA.value] = estado[q.DIREITA.value]
        estado_novo[q.ESQUERDA.value] = q_cima
        estado_novo[q.BAIXO.value] = estado[q.ESQUERDA.value]
        estado_novo[q.DIREITA.value] = q_baixo
        
        return estado_novo
    
    def selecionarQuadranteGiro(self, quadrante):
        q = None
        match quadrante:
            case "q1":
                q = q1
            case "q2":
                q = q2
            case "q3":
                q = q3
            case "q4":
                q = q4
            case default:
                raise Exception("Quadrante não existente")
        return q
    
    def verificarSequenciaPecas2(self, estado):
        estado_copia = estado.copy()

        valor_cada_coordenada = []

        valor_cada_coordenada.append(estado_copia[q1.CIMA.value] + estado_copia[q2.CIMA.value])
        valor_cada_coordenada.append(estado_copia[q1.CENTRO_HORIZONTAL.value] + estado_copia[q2.CENTRO_HORIZONTAL.value])
        valor_cada_coordenada.append(estado_copia[q1.BAIXO.value] + estado_copia[q2.BAIXO.value])

        valor_cada_coordenada.append(estado_copia[q1.DIREITA.value] + estado_copia[q3.DIREITA.value])
        valor_cada_coordenada.append(estado_copia[q1.CENTRO_VERTICAL.value] + estado_copia[q3.CENTRO_VERTICAL.value])
        valor_cada_coordenada.append(estado_copia[q1.ESQUERDA.value] + estado_copia[q3.ESQUERDA.value])

        valor_cada_coordenada.append(estado_copia[q1.DIAGONAL_DIREITA.value] + estado_copia[q4.DIAGONAL_DIREITA.value])

        valor_cada_coordenada.append(estado_copia[q3.CIMA.value] + estado_copia[q4.CIMA.value])
        valor_cada_coordenada.append(estado_copia[q3.CENTRO_HORIZONTAL.value] + estado_copia[q4.CENTRO_HORIZONTAL.value])
        valor_cada_coordenada.append(estado_copia[q3.BAIXO.value] + estado_copia[q4.BAIXO.value])

        valor_cada_coordenada.append(estado_copia[q2.DIREITA.value] + estado_copia[q4.DIREITA.value])
        valor_cada_coordenada.append(estado_copia[q2.CENTRO_VERTICAL.value] + estado_copia[q4.CENTRO_VERTICAL.value])
        valor_cada_coordenada.append(estado_copia[q2.ESQUERDA.value] + estado_copia[q4.ESQUERDA.value])

        valor_cada_coordenada.append(estado_copia[q2.DIAGONAL_ESQUERDA.value] + estado_copia[q3.DIAGONAL_ESQUERDA.value])

        outrasDiagonais = 4
        indexInicioOutraDiagonais = [1, 4, 6, 11]
        indexFinalOutraDiagonais = [29, 24, 34, 31]
        for i in range(outrasDiagonais):
            step = 7 if i % 2 == 0 else 5
            valor_cada_coordenada.append(estado[slice(indexInicioOutraDiagonais[i], indexFinalOutraDiagonais[i] + 1, step)])
            
        return self.contarQuantidadeDePecas(valor_cada_coordenada)


    def contarQuantidadeDePecas(self, valor_cada_coordenada):
        quantidades_de_pecas_B = []
        quantidades_de_pecas_W = []
        for valor in valor_cada_coordenada:
            sequencias_B = []
            sequencias_W = []
            contador_B = 0
            contador_W = 0
            for i in range(len(valor)):
                if valor[i] == "B":
                    contador_B += 1
                    if i == len(valor) - 1:
                        sequencias_B.append(contador_B)
                        contador_B = 0
                elif contador_B > 0:
                    sequencias_B.append(contador_B)
                    contador_B = 0
                
                if valor[i] == "W":
                    contador_W += 1
                    if i == len(valor) - 1:
                        sequencias_W.append(contador_W)
                        contador_W = 0 
                elif contador_W > 0:
                    sequencias_W.append(contador_W)
                    contador_W = 0

            quantidades_de_pecas_B.append(max(sequencias_B) if len(sequencias_B) > 0 else 0)
            quantidades_de_pecas_W.append(max(sequencias_W) if len(sequencias_W) > 0 else 0)

        quantidades_de_pecas = {"B": quantidades_de_pecas_B, "W": quantidades_de_pecas_W}

        return quantidades_de_pecas