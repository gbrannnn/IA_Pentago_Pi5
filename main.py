from pentago import Pentago

def main():
    pentago = Pentago()
    print(pentago.imprimir(pentago.estado_inicial))
    try:
        for i in range(1,5):
            estado_novo = pentago.girarDireita(pentago.estado_inicial, "q"+ str(i))
            print()
            print(pentago.imprimir(estado_novo))
            print()
    except Exception as erro:
        print(erro)
        return
    return

main()