from pentago import Pentago
from no import No

from jogador import JogadorHumano, JogadorAgente
from jogo import Jogo

import random

class Partida(Jogo):
    def __init__(self):
        self.no_jogadas = []
        self.historico = []
        self.pentago = Pentago(["-"]*36)
        no_inicial = self.pentago.iniciar()
        self.no_jogadas.append(no_inicial)        
        print(self.pentago.imprimir(no_inicial.estado_antes_giro))
        self.jogador_turno = None
    
    def inicializarJogadores(self):
        (humano, agente) = (JogadorHumano("B"), JogadorAgente("W"))
        humano.define_proximo_turno(agente)
        agente.define_proximo_turno(humano)
        
        self.jogadores = (humano, agente)

        return self.jogadores
    
    def jogos_validos(self):
        jogada = {
            "corPeca": self.turno().identificador,
            "index": None,
            "quadrante": None,
            "direcao": None
        }

        estado = self.pentago.estado

        jogadas = []
        for i in range(len(estado)):
            jogada["index"] = i
            jogada["quadrante"] = random.choice(["q1", "q2", "q3", "q4"]) 
            jogada["direcao"] = random.choice(["d", "e"])
            if self.pentago.jogadaValida(estado, jogada):
                jogadas.append(jogada.copy())

        return jogadas

    
    def jogar(self, jogada):
        no_novo = self.pentago.posicionarPeca(self.no_anterior, jogada)

        no_novo.estado_apos_giro = self.pentago.executarGiro(no_novo.estado_antes_giro, jogada)

        self.pentago = Pentago(no_novo.estado_apos_giro, no_novo)

        self.jogador_turno = self.trocarTurno()

        return self
    
    def trocarTurno(self):
        if self.jogador_turno is self.jogadores[0]:
            return self.jogadores[1] # agente
        elif self.jogador_turno is self.jogadores[1]:
            return self.jogadores[0] # humano
        
        return

    def calcular_utilidade(self, jogador):
        estado = self.pentago.estado
        jogada = self.historico[-1]

        quantidades_de_pecas = self.pentago.verificarSequenciaPecas(estado, jogada["index"], jogada["quadrante"])

        if quantidades_de_pecas[jogador.identificador] == 2:
            return 0.4 if jogador.min_max == "max" else -0.4
        elif quantidades_de_pecas[jogador.identificador] == 3:
            return 0.6 if jogador.min_max == "max" else -0.6
        elif quantidades_de_pecas[jogador.identificador] == 4:
            return 0.8 if jogador.min_max == "max" else -0.8
        elif quantidades_de_pecas[jogador.identificador] == 5 or self.venceu():
            return 1 if jogador.min_max == "max" else -1

        return 0.2
    
    def turno(self):
        return self.jogador_turno

    def venceu(self):
        estado = self.pentago.estado
        jogada = self.historico[-1]

        quantidades_de_pecas = self.pentago.verificarSequenciaPecas(estado, jogada["index"], jogada["quadrante"])
                                                                    
        valor_sequecia_vencedor = 5
        if any(valor >= valor_sequecia_vencedor for valor in quantidades_de_pecas["B"]):
            print("Jogador com a peca B venceu!!!")
            return True
        elif any(valor >= valor_sequecia_vencedor for valor in quantidades_de_pecas["W"]):
            print("Jogador com a peca W venceu!!!")
            return True

        return False

    def empate(self):
        estado = self.pentago.estado
        jogada = self.historico[-1]
        
        quantidades_de_pecas = self.pentago.verificarSequenciaPecas(estado, jogada["index"], jogada["quadrante"])
        
        valor_sequecia_vencedor = 5
        if any(valor >= valor_sequecia_vencedor for valor in quantidades_de_pecas["B"]) and any(valor >= valor_sequecia_vencedor for valor in quantidades_de_pecas["W"]):
            print("Empate!!! As duas peças possuem 5 em seqência")
            return True

        return False
    
    def finalizarPartida(self, no_novo, no_anterior, jogada):
        no = No(no_novo.estado_antes_giro, no_novo.estado_apos_giro, no_anterior, jogada)
        self.no_jogadas.append(no)
        self.historico.append(jogada)

        print("Partida Finalizado!!")
        return    
    
    
    def instrucoes(self):
        print("Para que possa jogar o Pentago sera necessario realizar um input de duas informações por rodada,\n" \
                "essas que seriam um valor/index de onde ira jogar e o quadrante/qn (sendo n valor do quadrante que irá girar, exemplo q1)," \
                "e para onde irá girar o quadrante (exemplo d/e)"\
                "Sendo eles separados por virgula.")
        
        confirmacao_de_instrucoes = input("De acordo? y/n: ")

        return confirmacao_de_instrucoes