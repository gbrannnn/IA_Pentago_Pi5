from pentago import Pentago
from no import No

class Partida:
    @classmethod
    @staticmethod
    def iniciarPartida(cls):
        rodadas = 36
        rodada_atual = 1
        cls.no_jogadas = []
        cls.historico = []


        cls.pentago = Pentago()
        no_inicial = cls.pentago.iniciar()
        cls.no_jogadas.append(no_inicial)
        print(cls.pentago.imprimir(no_inicial.estado))

        confirmacao_de_instrucoes = cls.instrucoes()

        if confirmacao_de_instrucoes == "n": 
            raise Exception("Não está de acordo com as intruções")
        
    
        print("Partida iniciada")
        
        while rodada_atual <= rodadas + 1:
            cor_peca = cls.definirCorPecaApartirDaRodada(rodada_atual)
            
            jogada_dados = cls.receberJogada()

            if not cls.dadosDeEntradaValidos(jogada_dados): continue

            jogada = cls.tratarJogada(jogada_dados, cor_peca)

            no_anterior = cls.no_jogadas.pop()

            if not cls.pentago.jogadaValida(no_anterior, jogada):
                print("Index selecionado não pode receber um valor!!!")
                cls.no_jogadas.append(no_anterior)
                continue

            estado_novo = cls.pentago.posicionarPeca(no_anterior, jogada)

            #if rodada_atual >= 9:
            # if cls.existeGanhador(estado_novo, jogada):
            #     cls.finalizarPartida(no.estado, no_anterior, jogada)
            #     break     

            no = cls.pentago.executarGiro(no_anterior, estado_novo, jogada)

            if cls.existeGanhador(no.estado, jogada, True):
                cls.finalizarPartida(no.estado, no_anterior, jogada)
                break 

            cls.no_jogadas.append(no)
            cls.historico.append(jogada)

            print()
            print(cls.pentago.imprimir(no.estado))
            rodada_atual += 1
        
        print(cls.historico)
        return

    @classmethod
    def existeGanhador(cls, estado, jogada, isDepoisDoGiro=False):
        if isDepoisDoGiro:
            quantidades_de_pecas = cls.pentago.verificarSequenciaPecas(estado, jogada["index"], jogada["quadrante"])
        else:
            quantidades_de_pecas = cls.pentago.verificarSequenciaPecas(estado, jogada["index"])
                                                                
        valor_sequecia_vencedor = 4
        if valor_sequecia_vencedor in quantidades_de_pecas["B"] and valor_sequecia_vencedor in quantidades_de_pecas["W"]:
            print("Empate!!! As duas peças possuem 5 em seqência")
            return True
        elif valor_sequecia_vencedor in quantidades_de_pecas["B"]:
            print("Jogador com a peca B venceu!!!")
            return True
        elif valor_sequecia_vencedor in quantidades_de_pecas["W"]:
            print("Jogador com a peca W venceu!!!")
            return True
        
        return False


    @classmethod
    def finalizarPartida(cls, estado, no_anterior, jogada):
        no = No(estado, no_anterior, jogada)
        cls.no_jogadas.append(no)
        cls.historico.append(jogada)

        print()
        print(cls.pentago.imprimir(no.estado))
        print()
        print("Jogo Finalizado!!")
        return
    
    @classmethod
    def receberJogada(cls):
        jogada = input("Digite valores a serem jogados: ")
        return jogada

    @classmethod
    def dadosDeEntradaValidos(cls, jogada_dados):
        jogada_dados_arr = jogada_dados.split(",")
        
        qtd_valores_jogada = 3
        if len(jogada_dados_arr) != qtd_valores_jogada:
            print("Valores da jogada não atendidos, é necessario 3 valores separados por virgula, valores esses que foram passados de exemplo nas instruções")
            return False

        if int(jogada_dados_arr[0]) >= 36:
            print("valor de Index Invalido!!, deve ser menor que 36") 
            return False
        
        return True
    
    @classmethod
    def tratarJogada(cls, jogada, cor_peca):
        jogada_arr = jogada.split(",")

        jogada_tratada = {
            "corPeca": cor_peca,
            "index": None,
            "quadrante": None,
            "direcao": None
        }

        jogada_tratada["index"] = int(jogada_arr[0])
        jogada_tratada["quadrante"] = jogada_arr[1]
        jogada_tratada["direcao"] = jogada_arr[2]

        return jogada_tratada

    @classmethod
    def definirCorPecaApartirDaRodada(cls, rodada_atual):
        if(rodada_atual % 2 == 0):
            return "W"
        return "B"
    
    @classmethod
    def instrucoes(cls):
        print("Para que possa jogar o Pentago sera necessario realizar um input de duas informações por rodada,\n" \
                "essas que seriam um valor/index de onde ira jogar e o quadrante/qn (sendo n valor do quadrante que irá girar, exemplo q1)," \
                "e para onde irá girar o quadrante (exemplo d/e)"\
                "Sendo eles separados por virgula.")
        
        confirmacao_de_instrucoes = input("De acordo? y/n: ")

        return confirmacao_de_instrucoes
