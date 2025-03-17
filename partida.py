from pentago import Pentago
from no import No

class Partida:
    @classmethod
    @staticmethod
    def iniciarPartida(cls):
        rodadas = 36
        rodada_atual = 1
        no_jogadas = []
        historico = []


        cls.pentago = Pentago()
        no_inicial = cls.pentago.iniciar()
        no_jogadas.append(no_inicial)
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

            no_anterior = no_jogadas.pop()

            if not cls.pentago.jogadaValida(no_anterior, jogada):
                print("Index selecionado não pode receber um valor!!!")
                no_jogadas.append(no_anterior)
                continue

            estado_novo = cls.pentago.posicionarPeca(no_anterior, jogada)

            if cls.existeGanhador(estado_novo, jogada):
                print(f"Jogador com a peca {jogada["corPeca"]} venceu!!!")
                no = No(estado_novo, no_anterior, jogada)
                no_jogadas.append(no)
                historico.append(jogada)

                print()
                print(cls.pentago.imprimir(no.estado))
                break

            no = cls.pentago.executarGiro(no_anterior, estado_novo, jogada)

            if rodada_atual >= 9:
                if cls.existeGanhador(no, jogada):
                    print(f"Jogador com a peca {jogada["corPeca"]} venceu!!!") 

            no_jogadas.append(no)
            historico.append(jogada)

            print()
            print(cls.pentago.imprimir(no.estado))
            rodada_atual += 1
            
        print(historico)
        return

    @classmethod
    def existeGanhador(cls, estado, jogada):
        valor_sequecia_vencedor = 4
        return valor_sequecia_vencedor in cls.pentago.verificarSequenciaPecas(estado, jogada["index"])
    
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
            return "R"
        return "B"
    
    @classmethod
    def instrucoes(cls):
        print("Para que possa jogar o Pentago sera necessario realizar um input de duas informações por rodada,\n" \
                "essas que seriam um valor/index de onde ira jogar e o quadrante/qn (sendo n valor do quadrante que irá girar, exemplo q1)," \
                "e para onde irá girar o quadrante (exemplo d/e)"\
                "Sendo eles separados por virgula.")
        
        confirmacao_de_instrucoes = input("De acordo? y/n: ")

        return confirmacao_de_instrucoes
