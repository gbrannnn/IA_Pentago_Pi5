from partida import Partida

def main():
    partida = Partida()
    
    (humano, agente) = partida.inicializarJogadores()

    partida.jogador_turno = humano

    confirmacao_de_instrucoes = partida.instrucoes()

    if confirmacao_de_instrucoes == "n": 
        raise Exception("Não está de acordo com as intruções")
    
    print("Partida iniciada")
    
    rodadas = 36
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

            no = partida.pentago.no
    
            partida.no_jogadas.append(no)
            partida.historico.append(jogada_humano)
    
            #if rodada_atual >= 9:
            if partida.venceu() or partida.empate():
                partida.finalizarPartida(no, partida.no_anterior, jogada_humano)
                break     
            
            #if rodada_atual >= 9:
            if partida.venceu() or partida.empate():
                partida.finalizarPartida(no, partida.no_anterior, jogada_humano)
                break

        if partida.jogador_turno is agente:
            print("\nVez do agente\n")
            
            jogada_agente = agente.jogar(partida)

            partida.no_anterior = partida.no_jogadas.pop()

            partida = partida.jogar(jogada_agente)
        
            no = partida.pentago.no

            partida.no_jogadas.append(no)
            partida.historico.append(jogada_agente)

            #if rodada_atual >= 9:
            if partida.venceu() or partida.empate():
                partida.finalizarPartida(no, partida.no_anterior, jogada_agente)
                break     
            
            #if rodada_atual >= 9:
            if partida.venceu() or partida.empate():
                partida.finalizarPartida(no, partida.no_anterior, jogada_agente)
                break

        print()
        print(partida.pentago.imprimir(no.estado_apos_giro))
        rodada_atual += 1
    
    print(partida.historico)
    return

main()