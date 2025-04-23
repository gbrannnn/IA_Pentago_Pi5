from jogador import Jogador    

class Jogo(Jogador):   
    def turno(self):
        raise NotImplementedError("Deve ser implementado")
    
    def jogar(self, localizacao):
        raise NotImplementedError("Deve ser implementado")
    
    def jogos_validos(self):
        raise NotImplementedError("Deve ser implementado")
    
    def venceu(self):
        raise NotImplementedError("Deve ser implementado")
    
    def empate(self):
        raise NotImplementedError("Deve ser implementado")
    
    def avaliar(self, player):
        raise NotImplementedError("Deve ser implementado")
    
    def inicializarJogadores(self):
        raise NotImplementedError("Deve ser implementado")
    

