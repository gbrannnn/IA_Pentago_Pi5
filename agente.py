from collections import defaultdict
import numpy as np
import pickle
import copy

from jogador import JogadorHumano, JogadorAgente
from ambiente import Ambiente

class Agente(Ambiente):
    def __init__(self, partida=None, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.identificador = "Agente"  # Corrigido: era "indentificador"
        self.corPeca = "B"
        self.estados = []  # Inicializar como lista vazia
        self.acoes = []  # Inicializar como lista vazia
        self.partida = partida
        # Adicionar estado inicial
        self.estados.append(partida.pentago.estado)
        self.acoes.append(partida.jogos_validos())

        self.alpha = alpha  # Taxa de aprendizado
        self.gamma = gamma  # Fator de desconto
        self.epsilon = epsilon  # Taxa de exploração

        self.Q = defaultdict(lambda: defaultdict(float))

        self.n_estados = len(self.estados)
        self.n_acoes = len(self.acoes)

    def T(self, partida, acao):
        """
        Função de transição que retorna os possíveis estados resultantes e suas probabilidades
        """
        self.partida = partida

        # Verificar se a ação é válida
        acoes_validas = partida.jogos_validos()
        if acao not in acoes_validas:
            return []

        try:
            # Simular a jogada
            partida_simulada = self._simular_jogada(partida, acao)
            novo_estado = partida_simulada.pentago.estado

            # Atualizar listas de estados e ações
            self.estados.append(novo_estado)
            self.acoes.append(partida_simulada.pentago.jogos_validos())

            # Para Pentago (jogo determinístico), retorna apenas um estado com probabilidade 1.0
            return [(novo_estado, 1.0)]

        except Exception as e:
            print(f"Erro ao simular jogada: {e}")
            return []

    def _simular_jogada(self, partida, acao):
        """
        Simula uma jogada sem modificar o estado original
        """
        partida_copia = copy.deepcopy(partida)

        # Preparar dados da jogada
        jogada = {
            "corPeca": self.corPeca,
            "index": acao["index"],
            "quadrante": acao["quadrante"],
            "direcao": acao["direcao"],
        }

        # Executar jogada na cópia
        partida_copia = partida_copia.jogar(jogada)

        return partida_copia

    def R(self, estado, acao, proximo_estado):
        """
        Função de recompensa - você pode implementar baseado na sua lógica de pontuação
        """
        # Exemplo básico - você deve adaptar conforme sua lógica
        if self.partida.venceu() and type(self.partida.turno()) is JogadorAgente:
            return 100  # Recompensa alta por vitória
        elif self.partida.venceu() and type(self.partida.turno()) is JogadorHumano:
            return -100  # Penalidade por derrota

        return self._calcular_recompensa_intermediaria(estado, self.partida.pentago.estado)


    def _calcular_recompensa_intermediaria(self, estado_atual):
        """
        Usa a lógica similar ao seu método calcular_utilidade da partida
        """
        # Simular uma jogada fictícia para usar sua lógica existente
        ultima_jogada = self.partida.historico[-1]

        if ultima_jogada:
            # Usar sua função verificarSequenciaPecas
            quantidades_de_pecas = self.partida.pentago.verificarSequenciaPecas(
                estado_atual, ultima_jogada["index"], ultima_jogada["quadrante"]
            )

            maior_sequencia_agente = max(quantidades_de_pecas[self.corPeca])
            cor_oponente = "B" if self.corPeca == "W" else "W"
            maior_sequencia_oponente = max(quantidades_de_pecas[cor_oponente])

            # Recompensa exponencial baseada no tamanho da sequência
            recompensa_agente = (2**maior_sequencia_agente) - 1
            penalidade_oponente = (2**maior_sequencia_oponente) - 1

            return recompensa_agente - penalidade_oponente

        return 1  # Recompensa padrão pequena

    def escolher_jogada_qlearning(self, partida, agente_qlearning, politica):
        """
        Escolhe a melhor jogada usando a política aprendida pelo Q-learning
        """
        # Obter estado atual
        estado_atual = partida.pentago.estado
        
        # Encontrar o índice do estado atual na lista de estados do agente
        estado_index = self.encontrar_estado_index(agente_qlearning.estados, estado_atual)
        
        if estado_index == -1:
            # Se o estado não foi visto durante o treinamento, usar jogada aleatória
            print("Estado não encontrado, usando jogada aleatória")
            jogadas_validas = partida.jogos_validos()
            import random
            return random.choice(jogadas_validas)
        
        # Usar a política para escolher a ação
        acao_index = politica[estado_index]
        
        # Converter índice da ação para jogada válida
        if acao_index < len(agente_qlearning.acoes[estado_index]):
            return agente_qlearning.acoes[estado_index][acao_index]
        else:
            jogadas_validas = partida.jogos_validos()
            import random
            return random.choice(jogadas_validas)

    def encontrar_estado_index(self, estados, estado_procurado):
        """
        Encontra o índice de um estado na lista de estados
        """
        for i, estado in enumerate(estados):
            if estado == estado_procurado:
                return i
        return -1
    def estado_para_string(self, estado):
        """Converte estado para string para usar como chave"""
        return ''.join(estado)
    
    def acao_para_string(self, acao):
        """Converte ação para string para usar como chave"""
        return f"{acao['index']}-{acao['quadrante']}-{acao['direcao']}"

    def atualizar_q(self, estado, acao, recompensa, proximo_estado, acoes_proximas):
        """Atualiza valor Q usando a equação de Bellman"""
        estado_str = self.estado_para_string(estado)
        acao_str = self.acao_para_string(acao)
        proximo_estado_str = self.estado_para_string(proximo_estado)
        
        # Encontrar valor máximo do próximo estado
        max_q_proximo = 0
        if acoes_proximas:
            max_q_proximo = max(
                self.Q[proximo_estado_str][self.acao_para_string(a)] 
                for a in acoes_proximas
            )
        
        # Atualização Q-learning
        q_atual = self.Q[estado_str][acao_str]
        self.Q[estado_str][acao_str] = q_atual + self.alpha * (
            recompensa + self.gamma * max_q_proximo - q_atual
        )    

    def salvar_modelo(self, arquivo):
        """Salva o modelo treinado"""
        with open(arquivo, 'wb') as f:
            pickle.dump(dict(self.Q), f)

    def carregar_modelo(self, arquivo):
        """Carrega modelo treinado"""
        try:
            with open(arquivo, 'rb') as f:
                q_dict = pickle.load(f)
                self.Q = defaultdict(lambda: defaultdict(float), q_dict)
            return True
        except FileNotFoundError:
            return False
        
    def __str__(self):
        return f"Agente {self.identificador} - Estados: {len(self.estados)}"

    def imprimir_valor(self, V):
        valor_texto = ""
        for i in range(0, self.n_estados, self.n_acoes):
            valor_texto += "|\t%.2f\t|\t%.2f\t|\t%.2f\t|\t%.2f\t|\n" % (V[i], V[i + 1], V[i + 2], V[i + 3])
        return valor_texto

    def imprimir_politica(self, politica):
        poltica_texto = ""
        ps = [] # política com símbolos
        for estado in politica:
            ps.append(self.acoes[estado])

        for i in range(0, self.n_estados, self.n_acoes):
            for j in range(0, self.n_acoes):
                ps[i+j] = self.estados[i+j]
            
            poltica_texto += f"|\t{ps[i]}\t|\t{ps[i+1]}\t|\t{ps[i+2]}\t|\t{ps[i+3]}\t|\n"
        return poltica_texto
    
    def imprimir_q(self, Q):
        valor_texto = "|\ts\t|\ts\t|\ta\t|\tQ(s,a)\t|\n"
            
        for i in range(0, len(self.estados)):
            for j in range(0, len(self.acoes)):
                valor_texto += "|\t%s\t|\t%s\t|\t%s\t|\t%.2f\t|\n" % (i, self.estados[i], self.acoes[j], Q[i][j])
        return valor_texto
