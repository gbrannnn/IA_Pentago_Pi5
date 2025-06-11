from pentago import Pentago
from no import No

from jogador import JogadorHumano, JogadorAgente, JogadorAgenteQlearning
from jogo import Jogo

import random

class Partida(Jogo):
    def __init__(self):
        self.no_jogadas = []
        self.historico = []
        self.pentago = Pentago(["-"]*36)
        #teste de caso
        # self.pentago = Pentago(["W", "W", "-", "W", "W", "W"] +
        #                        ["-", "-", "-", "-", "-", "-"] + 
        #                        ["-", "-", "-", "-", "-", "-"] +
        #                        ["-", "-", "-", "-", "-", "-"] +
        #                        ["-", "-", "-", "-", "-", "-"] +
        #                        ["-", "-", "-", "-", "-", "-"])
        no_inicial = self.pentago.iniciar()
        self.no_jogadas.append(no_inicial)        
        print(self.pentago.imprimir(no_inicial.estado_antes_giro))
        self.jogador_turno = None
        self.jogador_ganhador = None
    
    def inicializarJogadores(self, treino=False):
        if treino:
            (jogador1, jogador2) = (JogadorAgenteQlearning("B"), JogadorAgente("W"))
        else:
            (jogador1, jogador2) = (JogadorHumano("W"), JogadorAgenteQlearning("B"))
            
        jogador1.define_proximo_turno(jogador2)
        jogador2.define_proximo_turno(jogador1)
        
        self.jogadores = (jogador1, jogador2)

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
        for i in range(len(estado)*4):
            jogada["index"] = random.choice(list(range(36)))
            jogada["quadrante"] = random.choice(["q1", "q2", "q3", "q4"]) 
            jogada["direcao"] = random.choice(["d", "e"])
            if self.pentago.jogadaValida(estado, jogada):
                jogadas.append(jogada.copy())

        return jogadas

    
    def jogar(self, jogada):
        no_novo = self.pentago.posicionarPeca(self.no_anterior, jogada)

        no_novo.estado_apos_giro = self.pentago.executarGiro(no_novo.estado_antes_giro, jogada)

        self.pentago = Pentago(no_novo.estado_apos_giro, no_novo)
        
        self.historico.append(jogada)
        
        self.jogador_turno = self.trocarTurno()

        # print()
        # print(self.pentago.imprimir(no_novo.estado_apos_giro))

        return self
    
    def trocarTurno(self):
        humano, agente = self.jogadores
        if self.jogador_turno is humano:
            return agente
        elif self.jogador_turno is agente:
            return humano
        else:
            # Fallback - nunca deveria chegar aqui
            raise Exception(f"Jogador turno inválido: {self.jogador_turno}")

    def calcular_utilidade(self, jogador):
        estado = self.pentago.estado

        quantidades_de_pecas = self.pentago.verificarSequenciaPecas2(estado)

        maior_sequencia = max(quantidades_de_pecas[jogador.identificador])

        pontos = 0

        if jogador.min_max == "max":
            pontos += 10 ** maior_sequencia
        elif jogador.min_max == "min":
            pontos -= 10 ** maior_sequencia

        return pontos
    
    def turno(self):
        return self.jogador_turno

    def venceu(self):
        if len(self.historico) <= 0:
            return False

        estado = self.pentago.estado

        quantidades_de_pecas = self.pentago.verificarSequenciaPecas2(estado)
                                                                    
        valor_sequecia_vencedor = 5
        if any(valor >= valor_sequecia_vencedor for valor in quantidades_de_pecas["B"]):
            print("Jogador com a peca B venceu!!!")
            self.jogador_ganhador = "B"
            return True
        elif any(valor >= valor_sequecia_vencedor for valor in quantidades_de_pecas["W"]):
            print("Jogador com a peca W venceu!!!")
            self.jogador_ganhador = "W"
            return True

        return False

    def empate(self):
        if len(self.historico) <= 0:
            return False
        estado = self.pentago.estado
        
        quantidades_de_pecas = self.pentago.verificarSequenciaPecas2(estado)

        valor_sequecia_vencedor = 5
        if (any(valor >= valor_sequecia_vencedor for valor in quantidades_de_pecas["B"]) and any(valor >= valor_sequecia_vencedor for valor in quantidades_de_pecas["W"])) or "-" not in estado:
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