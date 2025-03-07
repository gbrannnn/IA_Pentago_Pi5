from pentago import Pentago

class Partida:
    @classmethod
    @staticmethod
    def iniciarPartida(cls):
        rodadas = 2
        rodada_atual = 1
        no_jogadas = []
        historico = []


        pentago = Pentago()
        no_inicial = pentago.iniciar()
        no_jogadas.append(no_inicial)
        print(pentago.imprimir(no_inicial))

        confirmacaoDeInstrucoes = cls.instrucoes()

        if confirmacaoDeInstrucoes == "n": 
            raise Exception("Não está de acordo com as intruções")
        
    
        print("Partida iniciada")
        
        while rodada_atual <= rodadas + 1:
            cor_peca = cls.definirCorPecaApartirDaRodada(rodada_atual)
            
            jogadaDados = cls.receberJogada()

            if not cls.dadosDeEntradaValidos(jogadaDados): continue

            jogada = cls.tratarJogada(jogadaDados, cor_peca)

            no_anterior = no_jogadas.pop()

            if not pentago.jogadaValida(no_anterior, jogada):
                print("Index selecionado não pode receber um valor!!!")
                no_jogadas.append(no_anterior)
                continue

            no = pentago.aplicarJogada(no_anterior, jogada)
            no_jogadas.append(no)
            historico.append(jogada)

            print()
            print(pentago.imprimir(no))
            rodada_atual += 1
            
        print(historico)
        return
    

    @classmethod
    def receberJogada(cls):
        jogada = input("Digite valores a serem jogados: ")
        return jogada

    @classmethod
    def dadosDeEntradaValidos(cls, jogadaDados):
        jogadaDadosArr = jogadaDados.split(",")
        
        qtdValoresjogada = 3
        if len(jogadaDadosArr) != qtdValoresjogada:
            print("Valores da jogada não atendidos, é necessario 3 valores separados por virgula, valores esses que foram passados de exemplo nas instruções")
            return False

        if int(jogadaDadosArr[0]) >= 36:
            print("valor de Index Invalido!!, deve ser menor que 36") 
            return False
        
        return True
    
    @classmethod
    def tratarJogada(cls, jogada, cor_peca):
        jogadaArr = jogada.split(",")

        jogadaTratada = {
            "corPeca": cor_peca,
            "index": None,
            "quadrante": None,
            "direcao": None
        }

        jogadaTratada["index"] = int(jogadaArr[0])
        jogadaTratada["quadrante"] = jogadaArr[1]
        jogadaTratada["direcao"] = jogadaArr[2]

        return jogadaTratada

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
        
        confirmacaoDeInstrucoes = input("De acordo? y/n: ")

        return confirmacaoDeInstrucoes
