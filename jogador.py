class Jogador:
    def __init__(self, idetificador, min_max = None):
        self.identificador = idetificador
        self.min_max = min_max
    
    def define_proximo_turno(self, proximo_turno):
        self.jogador_proximo_turno = proximo_turno

    def imprimir(self):
        return self.identificador
    
    def jogar(self, jogo):
        pass

    def e_min(self):
        return self.min_max == "min"
    
    def e_max(self):
        return self.min_max == "max"

    def proximo_turno(self):
        return self.jogador_proximo_turno


class JogadorHumano(Jogador):
    def __init__(self, idetificador):
        super().__init__(idetificador, "min")

    def jogar(self):
        jogada_valida = False
        while not jogada_valida:
            jogada_dados = self.receberJogada()
            if not self.dadosDeEntradaValidos(jogada_dados): continue     
            jogada_valida = True

        jogada = self.tratarJogada(jogada_dados)
            
        return jogada

    def receberJogada(self):
        jogada = input(f"Jogador {self.identificador} Digite valores a serem jogados: ")
        return jogada

    def tratarJogada(self, jogada):
        jogada_arr = jogada.split(",")

        jogada_tratada = {
            "corPeca": self.identificador,
            "index": None,
            "quadrante": None,
            "direcao": None
        }

        jogada_tratada["index"] = int(jogada_arr[0])
        jogada_tratada["quadrante"] = jogada_arr[1]
        jogada_tratada["direcao"] = jogada_arr[2]

        return jogada_tratada

    def dadosDeEntradaValidos(self, jogada_dados):
        jogada_dados_arr = jogada_dados.split(",")
        
        qtd_valores_jogada = 3
        if len(jogada_dados_arr) != qtd_valores_jogada:
            print("Valores da jogada não atendidos, é necessario 3 valores separados por virgula, valores esses que foram passados de exemplo nas instruções")
            return False

        if int(jogada_dados_arr[0]) >= 36:
            print("valor de Index Invalido!!, deve ser menor que 36") 
            return False
        
        if jogada_dados_arr[1] not in ["q1", "q2", "q3", "q4"]:
            print("Valor de Quadrante Invalido!!, deve ser um dos seguintes valores: q1, q2, q3, q4")
            return False
        
        if jogada_dados_arr[2] not in ["d", "e"]:
            print("Valor de Direção Invalido!!, deve ser um dos seguintes valores: d, e")
            return False

        return True

from minimax import melhor_jogada_agente_poda, minimax_alfabeta

class JogadorAgente(Jogador):
    def __init__(self, idetificador):
        super().__init__(idetificador, "max")

    def jogar(self, jogo):
        profundidade_maxima = 8
        melhor_jogada = melhor_jogada_agente_poda(jogo, profundidade_maxima)
        return melhor_jogada