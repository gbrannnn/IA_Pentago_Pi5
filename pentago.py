from quadrantes import Quadrante_1 as q1, Quadrante_2 as q2, Quadrante_3 as q3, Quadrante_4 as q4
from no import No

from jogo import Jogo, Jogador

class Pentago(Jogo):
    def __init__(self):
        self.estado_inicial = ["-"] * 36
        
    def imprimir(self, estado):
        return "|" + estado[0] + "|" + estado[1] + "|" + estado[2] + "|" + estado[3] + "|" + estado[4] + "|" + estado[5
                ] + "|" + "\n"+ "|" + estado[6] + "|" + estado[7] + "|" + estado[8] + "|" + estado[9] + "|" + estado[10] + "|" + estado[11
                ] + "|" + "\n" + "|" + estado[12] + "|" + estado[13] + "|" + estado[14] + "|" + estado[15] + "|" + estado[16] + "|" + estado[17
                ] + "|" + "\n" + "|" + estado[18] + "|" + estado[19] + "|" + estado[20] + "|" + estado[21] + "|" + estado[22] + "|" + estado[23
                ] + "|" + "\n" + "|" + estado[24] + "|" + estado[25] + "|" + estado[26] + "|" + estado[27] + "|" + estado[28] + "|" + estado[29
                ] + "|" + "\n" + "|" + estado[30] + "|" + estado[31] + "|" + estado[32] + "|" + estado[33] + "|" + estado[34] + "|" + estado[35] + "|"                                                                                                                                                                                                                                                                                                                                       
    
    def iniciar(self):
        no_inicial = No(self.estado_inicial)
        return no_inicial

    def jogos_validos(self, estado, jogada):
        return estado[jogada["index"]] == "-"

    def venceu(self, venceu):
        return venceu
    
    def empate(self, empate):
        return empate

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

    def verificarSequenciaPecas(self, estado, index, quadrante_giro=None):
        quadrante = self.verificarQudranteJogada(index)
        print(quadrante.__name__)

        if quadrante_giro == None:
            coordenadas_quadrante = self.pegarDoQuadranteCoordenadasAprtirDoIndex(estado, quadrante, index)
        else:
            coordenadas_quadrante = self.pegarCoordenadasQuadrante(quadrante) 

        valores_cada_coordenda = self.concatenarCoordenadasQuadrante(estado, quadrante, coordenadas_quadrante)
        
        outrasDiagonais = 4
        indexInicioOutraDiagonais = [1, 4, 6, 11]
        indexFinalOutraDiagonais = [29, 24, 34, 31]
        for i in range(outrasDiagonais):
            step = 7 if i % 2 == 0 else 5
            valores_cada_coordenda.append(estado[slice(indexInicioOutraDiagonais[i], indexFinalOutraDiagonais[i] + 1, step)])

        if quadrante_giro != None:
            diagonal_principal_direita = estado[slice(0,None,7)]
            diagonal_principal_esquerda = estado[slice(5,31,5)]
            valores_cada_coordenda.append(diagonal_principal_direita)
            valores_cada_coordenda.append(diagonal_principal_esquerda)
    
        print(valores_cada_coordenda)
        
        quantidades_de_pecas_B = []
        quantidades_de_pecas_W = []
        for valor in valores_cada_coordenda:
            countador_B_adjacente = 0
            countador_W_adjacente = 0
            for i in range(len(valor) - 1):
                if valor[i] == valor[i+1] and valor[i] == "B":
                    countador_B_adjacente += 1
                elif valor[i] == valor[i+1] and valor[i] == "W":
                    countador_W_adjacente += 1
            quantidades_de_pecas_B.append(countador_B_adjacente)
            quantidades_de_pecas_W.append(countador_W_adjacente)

        quantidades_de_pecas = {"B": quantidades_de_pecas_B, "W": quantidades_de_pecas_W}

        print(quantidades_de_pecas)
        return quantidades_de_pecas
    
    def pegarDoQuadranteCoordenadasAprtirDoIndex(self, estado, quadrante, index):
        coordenadas_quadrante = []
        for q in quadrante :
            if q.name == "DOMINIO":
                continue

            r = self.sliceParaRange(q.value.start, q.value.stop, q.value.step, estado)
            if index in r:
                coordenadas_quadrante.append(q.name)
        return coordenadas_quadrante

    def pegarCoordenadasQuadrante(self, quadrante):
        coordenadas_quadrante = []
        for q in quadrante :
            if q.name == "DOMINIO":
                continue
            coordenadas_quadrante.append(q.name)
        return coordenadas_quadrante

    def concatenarCoordenadasQuadrante(self, estado, quadrante, coordenadas_qudrante):
        match quadrante.__name__:
            case "Quadrante_1":
                quadrante_vizinho_1 = q2          
                quadrante_vizinho_2 = q3
                quadrante_vizinho_3 = q4
            case "Quadrante_2":
                quadrante_vizinho_1 = q1
                quadrante_vizinho_2 = q4
                quadrante_vizinho_3 = q3
            case "Quadrante_3":
                quadrante_vizinho_1 = q4
                quadrante_vizinho_2 = q1
                quadrante_vizinho_3 = q2
            case "Quadrante_4":
                quadrante_vizinho_1 = q3
                quadrante_vizinho_2 = q2
                quadrante_vizinho_3 = q1

        valores_cada_coordenda = []
        for coordenada in coordenadas_qudrante:
            print(coordenada)
            if coordenada in ("CIMA", "CENTRO_HORIZONTAL", "BAIXO"):
                arr = self.inverterArray(estado, quadrante, coordenada)
                valores_cada_coordenda.append(arr + estado[quadrante_vizinho_1[coordenada].value])
            elif coordenada in ("ESQUERDA", "CENTRO_VERTICAL", "DIREITA"):
                arr = self.inverterArray(estado, quadrante, coordenada)
                valores_cada_coordenda.append(arr + estado[quadrante_vizinho_2[coordenada].value])
            elif coordenada in quadrante.__members__ and (coordenada in ("DIAGONAL_DIREITA", "DIAGONAL_ESQUERDA")):
                arr = self.inverterArray(estado, quadrante, coordenada)
                valores_cada_coordenda.append(arr + estado[quadrante_vizinho_3[coordenada].value])
        
        return valores_cada_coordenda

    def inverterArray(self, estado, quadrante, coordenada):
        arr = estado[quadrante[coordenada].value]
        if quadrante.__name__ == "Quadrante_1" :
            arr = estado[quadrante[coordenada].value]
        elif quadrante.__name__ == "Quadrante_2" and coordenada in ("CIMA", "CENTRO_HORIZONTAL", "BAIXO"):
            arr = estado[quadrante[coordenada].value]
            arr.reverse()
        elif quadrante.__name__ == "Quadrante_3" and coordenada in ("ESQUERDA", "CENTRO_VERTICAL", "DIREITA", "DIAGONAL_ESQUERDA"):
            arr = estado[quadrante[coordenada].value]
            arr.reverse()
        elif quadrante.__name__ == "Quadrante_4":
            arr = estado[quadrante[coordenada].value]
            arr.reverse()
        
        return arr

    def sliceParaRange(self, start, stop, step, lista):
        start = 0 if start is None else start
        stop = len(lista) if stop is None else stop
        step = 1 if step is None else step
        return range(start, stop, step)
        
    def verificarQudranteJogada(self, index):
        if index in q1.DOMINIO.value:
            q = q1
        elif index in q2.DOMINIO.value:
            q = q2
        elif index in q3.DOMINIO.value:
            q = q3
        elif index in q4.DOMINIO.value:
            q = q4
        
        return q