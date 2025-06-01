from partida import Partida
from agente import Agente
from qlearning import Qlearning
import copy
import time

class Main:
    def jogar_pentago_contra_agente():
        partida = Partida()
        
        (humano, agente) = partida.inicializarJogadores()

        partida.jogador_turno = humano

        agente_qlearning = Agente(partida)
        if not agente_qlearning.carregar_modelo("agente_pentago.pkl"):
            print("Modelo não encontrado. Execute o treinamento primeiro.")
            return
        
        print("Treinando agente Q-learning...")
        qlearning = Qlearning(agente_qlearning)
        Q, politica = qlearning.calcular_tabela_q(estado_inicial=0, n_passos=50000)
        print("Treinamento concluído!")

        # print("\nImprimindo Valores por estado:")
        # print(agente_qlearning.imprimir_q(Q))
        # print("\nImprimindo Polítca ótima por estado:")
        # print(agente_qlearning.imprimir_politica(politica))

        confirmacao_de_instrucoes = partida.instrucoes()

        if confirmacao_de_instrucoes == "n": 
            raise Exception("Não está de acordo com as intruções")
        
        print("Partida iniciada")

        rodada_atual = 1
        while True:
            if partida.jogador_turno is humano:
                jogada_humano = humano.jogar()
                
                partida.no_anterior = partida.no_jogadas.pop()
                
                estado_anterior = partida.no_anterior.estado_apos_giro if rodada_atual != 1 else partida.no_anterior.estado_antes_giro
                
                if not partida.pentago.jogadaValida(estado_anterior, jogada_humano):
                    print("Index selecionado não pode receber um valor!!!")
                    partida.no_jogadas.append(partida.no_anterior)
                    continue

                partida = partida.jogar(jogada_humano)
                print(partida.historico)
                no = partida.pentago.no
        
                partida.no_jogadas.append(no)
        
                if rodada_atual >= 9:
                    if partida.venceu() or partida.empate():
                        partida.finalizarPartida(no, partida.no_anterior, jogada_humano)
                        break
                
            elif partida.jogador_turno is agente:
                # print("\nVez do agente\n")
                
                # partida.no_anterior = partida.no_jogadas.pop()
                
                # jogada_agente = agente.jogar(copy.deepcopy(partida))

                # partida = partida.jogar(jogada_agente)

                print("\nVez do agente Q-learning\n")
                
                partida.no_anterior = partida.no_jogadas.pop()
                
                # Usar Q-learning para escolher a jogada
                jogada_agente = agente_qlearning.escolher_jogada_qlearning(partida, agente_qlearning, politica)

                partida = partida.jogar(jogada_agente)

                no = partida.pentago.no

                partida.no_jogadas.append(no)

                if rodada_atual >= 9:
                    if partida.venceu() or partida.empate():
                        partida.finalizarPartida(no, partida.no_anterior, jogada_agente)
                        break     

            print()
            print(partida.pentago.imprimir(no.estado_apos_giro))
            rodada_atual += 1
        
        agente_qlearning.salvar_modelo("agente_pentago.pkl")

        print(partida.historico.pop())
        return
    

Main.jogar_pentago_contra_agente()