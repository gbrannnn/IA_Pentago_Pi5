from pentago import Pentago
from partida import Partida

def main():
    pentago = Pentago()
    no_inicial = pentago.iniciar()

    print("\n")
    print("Pentago Iniciado!!")
    print(pentago.imprimir(no_inicial))
    print("\n")

    try:
        Partida.iniciarPartida()
    except Exception as erro:
        print(erro)
        
    # try:
    #     for i in range(1,5):
    #         estado_novo = pentago.girarEsquerda(pentago.estado_inicial, "q"+ str(i))
    #         print()
    #         print(pentago.imprimir(estado_novo))
    #         print()
    # except Exception as erro:
    #     print(erro)
    #     return
    return

main()