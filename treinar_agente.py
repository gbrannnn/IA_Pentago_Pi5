from partida import Partida
from agente import Agente
import copy
import logging

class TreinarAgente:
    def __init__(self, num_episodios=1000, epsilon_dinamico=0.1):
        self.num_episodios = num_episodios
        self.epsilon_dinamico = epsilon_dinamico
        self.vitorias_agente_q = 0
        self.vitorias_agente_minimax = 0
        self.empate = 0
        self.partida_avaliacao = False


    def avaliacao_qlearning(self):
        self.partida_avaliacao = True
        self.num_episodios = 10
        self.epsilon_dinamico = 0.1

        logging.basicConfig(
            filename='meu_log.log',      # Nome do arquivo de saída
            level=logging.INFO,          # Nível mínimo que será registrado
            format='%(asctime)s - %(levelname)s - %(message)s' # Formato do log
        )
        logging.info("---Avaliacao iniciado---")
        logging.info(f"Número de episódios: {self.num_episodios}")

        self.loop_partida()
        
        print()
        logging.info(f"Vitorias do agente Q-learning: {self.vitorias_agente_q}")
        logging.info(f"Vitorias do agente minimax: {self.vitorias_agente_minimax}")
        logging.info(f"Empates: {self.empate}")
        logging.info("---Avaliacao Finalizada---")
        return

    def treinar_agente_qlearning(self):
        self.vitorias_agente_q = 0
        self.vitorias_agente_minimax = 0
        self.empate = 0

        logging.basicConfig(
            filename='meu_log.log',      # Nome do arquivo de saída
            level=logging.INFO,          # Nível mínimo que será registrado
            format='%(asctime)s - %(levelname)s - %(message)s' # Formato do log
        )
        logging.info("---Treinamento iniciado---")
        logging.info(f"Número de episódios: {self.num_episodios}")

        self.loop_partida()
        
        print()
        logging.info(f"Vitorias do agente Q-learning: {self.vitorias_agente_q}")
        logging.info(f"Vitorias do agente minimax: {self.vitorias_agente_minimax}")
        logging.info(f"Empates: {self.empate}")
        logging.info("---Treinamento Finalizado---")
        return

    def loop_partida(self):
        for episodio in range(1, self.num_episodios + 1):
            try:
                partida = Partida()
                (agente_q, agente_minimax) = partida.inicializarJogadores(treino=True)
                
                partida.jogador_turno = agente_minimax
                
                agente_qlearning = Agente(agente_q.identificador ,partida, epsilon=self.epsilon_dinamico)

                # se existir, carrega; senão, continua com Q zerado
                agente_qlearning.carregar_modelo("agente_pentago.pkl")
                print(f"Q: {len(agente_qlearning.Q)}")
                print(f"PI: {len(agente_qlearning.PI)}")

                
                print("Partida de treinamento iniciada")

                rodada_atual = 1
                while True:
                    if partida.jogador_turno is agente_q:
                        print("Vez do agente Q-learning")
                        
                        if len(partida.no_jogadas) > 0:
                            partida.no_anterior = partida.no_jogadas[-1]
                        
                        # Usar Q-learning para escolher a jogada
                        jogada_agente = agente_qlearning.escolher_jogada_qlearning(partida)

                        partida = partida.jogar(jogada_agente)
                        
                        agente_q.partida = partida

                        recompensa = agente_qlearning.R(partida.pentago.estado)
                        agente_qlearning.atualizar_q(partida.pentago.estado, jogada_agente, recompensa)

                        no = partida.pentago.no

                        partida.no_jogadas.append(no)

                        if rodada_atual >= 9:
                            if partida.empate():
                                self.empate += 1
                                partida.finalizarPartida(no, partida.no_anterior, jogada_agente)
                                break
                            elif partida.venceu():
                                self.vitorias_agente_q += 1
                                partida.finalizarPartida(no, partida.no_anterior, jogada_agente)
                                break

                    elif partida.jogador_turno is agente_minimax:
                        print("Vez do agente_minimax")
                        
                        if len(partida.no_jogadas) > 0:
                            partida.no_anterior = partida.no_jogadas[-1] 
                        
                        jogada_agente_minimax = agente_minimax.jogar(copy.deepcopy(partida))

                        partida = partida.jogar(jogada_agente_minimax)                

                        no = partida.pentago.no

                        partida.no_jogadas.append(no)

                        if rodada_atual >= 9:
                            if partida.empate():
                                self.empate += 1
                                partida.finalizarPartida(no, partida.no_anterior, jogada_agente_minimax)
                                break
                            elif partida.venceu():
                                self.vitorias_agente_minimax += 1
                                partida.finalizarPartida(no, partida.no_anterior, jogada_agente_minimax)
                                break    
                    
                    # print()
                    # print(partida.pentago.imprimir(no.estado_apos_giro))
                    rodada_atual += 1
            except Exception as e:
                print(e)
            
            if episodio % 500 == 0 and self.partida_avaliacao is False:
                logging.info(f"Episódio {episodio} finalizado")
                self.epsilon_dinamico = max(0.1, self.epsilon_dinamico * 0.995)

            agente_qlearning.salvar_modelo("agente_pentago.pkl")
            print(partida.historico.pop())


treinamento = TreinarAgente()
treinamento.avaliacao_qlearning()