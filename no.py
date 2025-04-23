class No:
  def __init__(self, estado_antes_giro, no_pai=None, estado_apos_giro=None, aresta=None):
    self.estado_antes_giro = estado_antes_giro
    self.estado_apos_giro = estado_apos_giro
    self.no_pai = no_pai
    self.aresta = aresta

  def __repr__(self):
    return str([self.estado_antes_giro, self.estado_apos_giro])

  def __lt__(self, outro):
    return (self.custo + self.heuristica) < (outro.custo + outro.heuristica)