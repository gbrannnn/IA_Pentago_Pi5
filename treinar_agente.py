from partida import Partida
from agente import Agente
from qlearning import Qlearning
import copy
import time

class TreinarAgente:
    def treinar_agente_qlearning():
        partida = Partida()
        (agente_q, agente_minimax) = partida.inicializarJogadores(treino=True)
        
        partida.jogador_turno = agente_minimax
        
        agente_qlearning = Agente(partida)

        if not agente_qlearning.carregar_modelo("agente_pentago.pkl"):
            print("Modelo não encontrado. Execute o treinamento primeiro.")
            return
        
        print("Treinando agente Q-learning...")
        qlearning = Qlearning(agente_qlearning)
        Q, politica = qlearning.calcular_tabela_q(estado_inicial=0, n_passos=50000)

        # print("\nImprimindo Valores por estado:")
        # print(agente_qlearning.imprimir_q(Q))
        # print("\nImprimindo Polítca ótima por estado:")
        # print(agente_qlearning.imprimir_politica(politica))
        
        print("Partida de treinamento iniciada")

        rodada_atual = 1
        while True:
            if partida.jogador_turno is agente_q:
                print("\nVez do agente Q-learning\n")
                
                if len(partida.no_jogadas) > 0:
                    partida.no_anterior = partida.no_jogadas[-1]
                
                # Usar Q-learning para escolher a jogada
                jogada_agente = agente_qlearning.escolher_jogada_qlearning(partida, agente_qlearning, politica)

                partida = partida.jogar(jogada_agente)

                no = partida.pentago.no

                partida.no_jogadas.append(no)

                if rodada_atual >= 9:
                    if partida.venceu() or partida.empate():
                        partida.finalizarPartida(no, partida.no_anterior, jogada_agente)
                        break
                
                time.sleep(2)
            elif partida.jogador_turno is agente_minimax:
                print("\nVez do agente_minimax\n")
                
                if len(partida.no_jogadas) > 0:
                    partida.no_anterior = partida.no_jogadas[-1] 
                
                jogada_agente_minimax = agente_minimax.jogar(copy.deepcopy(partida))

                partida = partida.jogar(jogada_agente_minimax)                

                no = partida.pentago.no

                partida.no_jogadas.append(no)

                if rodada_atual >= 9:
                    if partida.venceu() or partida.empate():
                        partida.finalizarPartida(no, partida.no_anterior, jogada_agente_minimax)
                        break     

                time.sleep(2)
            
            print()
            print(partida.pentago.imprimir(no.estado_apos_giro))
            rodada_atual += 1
        
        agente_qlearning.salvar_modelo("agente_pentago.pkl")

        print(partida.historico.pop())
        return


for i in range(1):
    TreinarAgente.treinar_agente_qlearning()