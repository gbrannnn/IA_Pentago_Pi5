from pentago import Pentago

class Partida:
    @classmethod
    @staticmethod
    def iniciarPartida(cls):
        cls.rodadas = 2
        cls.rodada_atual = 1
        cls.jogadas = []


        cls.pentago = Pentago()
        cls.no_inicial = cls.pentago.iniciar()
        cls.jogadas.append(cls.no_inicial)
        print(cls.pentago.imprimir(cls.no_inicial))

        confirmacaoDeInstrucoes = cls.instrucoes()

        if confirmacaoDeInstrucoes == "n": 
            raise Exception("Não está de acordo com as intruções")
        

        print("Partida iniciada")
        
        while cls.rodada_atual <= cls.rodadas + 1:
            corPeca = cls.definirCorPeçaAprtirDaRodada()
            
            jogada = cls.tratarJogada(cls.receberJogada(), corPeca)
            
            no_anterior = cls.jogadas.pop()

            no = cls.pentago.aplicarJogada(no_anterior, jogada)
            cls.jogadas.append(no)

            print()
            print(cls.pentago.imprimir(no))
            cls.rodada_atual += 1
            
        print(cls.jogadas)
        return
    
    @classmethod
    def receberJogada(cls):
        jogada = input("Digite valores a serem jogados: ")
        return jogada

    @classmethod
    def tratarJogada(cls, jogada, corPeca):
        jogadaArr = jogada.split(",")

        jogadaTratada = {
            "corPeca": corPeca,
            "index": None,
            "quadrante": None,
            "direcao": None
        }

        jogadaTratada["index"] = int(jogadaArr[0])
        jogadaTratada["quadrante"] = jogadaArr[1]
        jogadaTratada["direcao"] = jogadaArr[2]

        return jogadaTratada

    @classmethod
    def definirCorPeçaAprtirDaRodada(cls):
        if(cls.rodada_atual % 2 == 0):
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
