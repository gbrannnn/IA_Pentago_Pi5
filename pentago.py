from quadrantes import Quadrante_1 as q1, Quadrante_2 as q2, Quadrante_3 as q3, Quadrante_4 as q4
from no import No

class Pentago:
    def __init__(self):
        self.estado_inicial = ["-", "-", "-", "-", "-", "-",
                               "-", "-", "-", "-", "-", "-",
                               "-", "-", "-", "-", "-", "-",
                               "-", "-", "-", "-", "-", "-",
                               "-", "-", "-", "-", "-", "-",
                               "-", "-", "-", "-", "-", "-",]
        

    def imprimir(self, no):
        estado = no.estado
        return "|" + estado[0] + "|" + estado[1] + "|" + estado[2] + "|" + estado[3] + "|" + estado[4] + "|" + estado[5
                ] + "|" + "\n"+ "|" + estado[6] + "|" + estado[7] + "|" + estado[8] + "|" + estado[9] + "|" + estado[10] + "|" + estado[11
                ] + "|" + "\n" + "|" + estado[12] + "|" + estado[13] + "|" + estado[14] + "|" + estado[15] + "|" + estado[16] + "|" + estado[17
                ] + "|" + "\n" + "|" + estado[18] + "|" + estado[19] + "|" + estado[20] + "|" + estado[21] + "|" + estado[22] + "|" + estado[23
                ] + "|" + "\n" + "|" + estado[24] + "|" + estado[25] + "|" + estado[26] + "|" + estado[27] + "|" + estado[28] + "|" + estado[29
                ] + "|" + "\n" + "|" + estado[30] + "|" + estado[31] + "|" + estado[32] + "|" + estado[33] + "|" + estado[34] + "|" + estado[35] + "|"                                                                                                                                                                                                                                                                                                                                       
    
    def iniciar(self):
        no_inicial = No(self.estado_inicial)
        return no_inicial

    def jogadaValida(self, no, jogada):
        return no.estado[jogada["index"]] == "-"

    #funcção socessora
    def aplicarJogada(self, no_pai, jogada):
        estado_novo = no_pai.estado.copy()

        estado_novo[jogada["index"]] = jogada["corPeca"]
        
        no_novo = No(estado_novo, no_pai, jogada)

        print(self.imprimir(no_novo))

        if jogada["direcao"] == "d":
            estado_novo = self.girarDireita(estado_novo, jogada["quadrante"])
        elif jogada["direcao"] == "e":
            estado_novo = self.girarEsquerda(estado_novo, jogada["quadrante"])

        no_novo.estado = estado_novo

        return no_novo

    def girarDireita(self, estado, quadrante):
        estado_novo = estado.copy()
        try:
            q = self.selecionarQuadrante(quadrante)
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
            q = self.selecionarQuadrante(quadrante)
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
    
    def selecionarQuadrante(self, quadrante):
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

