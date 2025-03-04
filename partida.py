class Partida:

    @classmethod
    @staticmethod
    def iniciarPartida(cls):
        cls.rodadas = 2
        cls.rodada_atual = 1

        confirmacaoDeInstrucoes = cls.instrucoes()

        if confirmacaoDeInstrucoes == "n": 
            raise Exception("Não está de acordo com as intruções")
        else:
            print("Partida iniciada")
        
        while cls.rodada_atual <= cls.rodadas + 1:
            corPeca = cls.definirCorPeçaAprtirDaRodada()
            print(corPeca)
            jogada = cls.receberJogada()
            print(jogada[0])
            cls.rodada_atual += 1
        return
    
    @classmethod
    def receberJogada(cls):
        jogada = input("Digite valores a serem jogados: ").split(",")
        return jogada

    @classmethod
    def definirCorPeçaAprtirDaRodada(cls):
        if(cls.rodada_atual % 2 == 0):
            return "W"
        return "P"
    
    @classmethod
    def instrucoes(cls):
        print("Para que possa jogar o Pentago sera necessario realizar um input de duas informações por rodada,\n" \
                "essas que seriam um valor/index de onde ira jogar e o quadrante/qn (sendo n valor do quadrante que irá girar, exemplo q1)." \
                "Sendo eles separados por virgula.")
        
        confirmacaoDeInstrucoes = input("De acordo? y/n: ")

        return confirmacaoDeInstrucoes
