from collections import defaultdict
import numpy as np
import random
import pickle

from ambiente import Ambiente

class Agente(Ambiente):
    def __init__(self, corPeca, partida=None,alpha=0.1, gamma=0.9, epsilon=0.1):
        self.identificador = "Agente"  # Corrigido: era "indentificador"
        self.corPeca = corPeca
        self.estados = [self.estado_para_string(partida.pentago.estado)]  # Inicializar como lista vazia
        self.acoes = [partida.jogos_validos()]  # Inicializar como lista vazia
        self.partida = partida
        # Adicionar estado inicial

        self.alpha = alpha  # Taxa de aprendizado
        self.gamma = gamma  # Fator de desconto
        self.epsilon = epsilon  # Taxa de exploração

        # Q: estado_str -> {acao_str: valor}
        self.Q = defaultdict(dict)
        # PI: estado_str -> acao_str
        self.PI = {}

        # inicializa o estado inicial na tabela Q
        estado0 = self.estado_para_string(self.partida.pentago.estado)
        self.Q.setdefault(estado0, {})

        self.n_estados = len(self.estados)
        self.n_acoes = len(self.acoes)

    def R(self, estado):
        """
        Função de recompensa - você pode implementar baseado na sua lógica de pontuação
        """
        # Exemplo básico - você deve adaptar conforme sua lógica
        if self.partida.empate():
            return 0
        elif self.partida.venceu() and self.partida.jogador_ganhador == self.corPeca:
            return 1000  # Recompensa alta por vitória
        elif self.partida.venceu() and self.partida.jogador_ganhador == "W":
            return -1000  # Penalidade por derrota

        return self._calcular_recompensa_intermediaria(self.partida.pentago.estado)

    def _calcular_recompensa_intermediaria(self, estado_atual):
        """
        Usa a lógica similar ao seu método calcular_utilidade da partida
        """
        # Simular uma jogada fictícia para usar sua lógica existente
        ultima_jogada = self.partida.historico[-1]

        if ultima_jogada:
            # Usar sua função verificarSequenciaPecas
            quantidades_de_pecas = self.partida.pentago.verificarSequenciaPecas2(estado_atual)

            maior_sequencia_agente = max(quantidades_de_pecas[self.corPeca])
            cor_oponente = "B" if self.corPeca == "W" else "W"
            maior_sequencia_oponente = max(quantidades_de_pecas[cor_oponente])

            # Recompensa exponencial baseada no tamanho da sequência
            recompensa_agente = (2 ** maior_sequencia_agente) - 1
            penalidade_oponente = (2 ** maior_sequencia_oponente) - 1

            return (0.7 * recompensa_agente) - (0.3 * penalidade_oponente)

        return 0.1  # Recompensa padrão pequena

    def escolher_jogada_qlearning(self, partida):
        """
        Escolhe a melhor jogada usando a política aprendida pelo Q-learning com ε-greedy
        """
        estado_str = self.estado_para_string(partida.pentago.estado)
        acoes_validas = partida.jogos_validos()
        
        # Estratégia ε-greedy
        if random.random() < self.epsilon:
            print("Escolhendo ação aleatória (exploração)")
            return random.choice(acoes_validas)
        
        # Se o estado não foi visto, inicializar com valores zero
        if estado_str not in self.Q:
            self.Q[estado_str] = {}
            for acao in acoes_validas:
                acao_str = self.acao_para_string(acao)
                self.Q[estado_str][acao_str] = 0.0
        
        # Garantir que todas as ações válidas estão na tabela Q
        for acao in acoes_validas:
            acao_str = self.acao_para_string(acao)
            if acao_str not in self.Q[estado_str]:
                self.Q[estado_str][acao_str] = 0.0
        
        # Escolher a melhor ação baseada nos valores Q
        melhor_acao_str = max(
            [self.acao_para_string(a) for a in acoes_validas],
            key=lambda a_str: self.Q[estado_str].get(a_str, 0.0)
        )
        
        # Encontrar a ação correspondente
        for acao in acoes_validas:
            if self.acao_para_string(acao) == melhor_acao_str:
                print(f"Escolhendo melhor ação: {melhor_acao_str} com Q={self.Q[estado_str][melhor_acao_str]:.2f}")
                return acao
        
        # Fallback
        return random.choice(acoes_validas)


    def encontrar_estado_index(self, estado_procurado):
        """
        Encontra o índice de um estado na lista de estados
        """
        for i, estado in enumerate(self.estados):
            if estado == estado_procurado:
                return i
        return -1

    def estado_para_string(self, estado):
        """Converte estado para string para usar como chave"""
        return ''.join(estado)
    
    def acao_para_string(self, acao):
        """Converte ação para string para usar como chave"""
        return f"{acao['index']}-{acao['quadrante']}-{acao['direcao']}"

    def atualizar_q(self, estado_anterior, acao, recompensa):
        """Atualiza valor Q usando a equação de Bellman"""
        estado_str = self.estado_para_string(estado_anterior)
        acao_str  = self.acao_para_string(acao)

        # garante que existam as entradas
        self.Q.setdefault(estado_str, {})
        self.Q[estado_str].setdefault(acao_str, 0.0)

        # sempre usar a versão em string do estado
        proximo_estado_str = self.estado_para_string(self.partida.pentago.estado)
        self.Q.setdefault(proximo_estado_str, {})
        
        # valor máximo em s2
        max_q_s2 = max(self.Q[proximo_estado_str].values()) if self.Q[proximo_estado_str] else 0.0

        # Bellman update
        q_old = self.Q[estado_str][acao_str]
        novo_q =  q_old + self.alpha * (recompensa + self.gamma * max_q_s2 - q_old)
        self.Q[estado_str][acao_str] = novo_q
        print(f"[Q-UPDATE] s={estado_str} a={acao_str} → Q={novo_q:.2f}")

        # atualiza política (greedy)
        melhor_a = max(self.Q[estado_str].items(), key=lambda x: x[1])[0]
        self.PI[estado_str] = melhor_a

    def salvar_modelo(self, arquivo):
        with open(arquivo, "wb") as f:
            pickle.dump({"Q": dict(self.Q), "PI": self.PI}, f)

    def carregar_modelo(self, arquivo):
        try:
            with open(arquivo, "rb") as f:
                m = pickle.load(f)
            self.Q = defaultdict(dict, m.get("Q", {}))
            self.PI = m.get("PI", {})
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print("Erro ao carregar modelo:", e)
            return False