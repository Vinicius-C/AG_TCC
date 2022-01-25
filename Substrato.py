import math
from FSS import FSS


class Substrato:
    # Velocidade da Luz no Substrato
    v = None

    # Espessura
    l = None
    # Permissividade Elétrica
    e = None
    # Permebalidade Magnética
    u = None

    # Permissividade Elétrica do Vácuo
    e0 = 8.85418 * (10 ** -12)
    # Permebalidade Magnética do Vácuo
    u0 = 1.2566 * (10 ** -6)

    def __init__(self, espessura, permissividade, permeabilidade):
        self.l = espessura
        self.e = permissividade
        self.u = permeabilidade

    def get_v(self):
        return math.sqrt(1 / (self.e * self.u))

    def km(self, frequencia):
        km = 2 * math.pi / (self.get_v() / frequencia)
        return km

    def beta(self, frequencia, angulo_incidencia):
        km = self.km(frequencia)
        k0 = 2 * math.pi / (FSS.vluz / frequencia)
        kt = k0 * math.sin(angulo_incidencia)
        beta = math.sqrt(km ** 2 - kt ** 2)
        return beta

    # modo = 1 para TE e 2 para TM
    def zm(self, modo, frequencia, angulo_incidencia):
        beta = self.beta(frequencia, angulo_incidencia)
        zs = beta / (2 * math.pi * frequencia * self.e) if (modo == 1) else 2 * math.pi * frequencia * self.u0 / beta
        return zs

    # modo = 1 para TE e 2 para TM
    def get_impedancia(self, modo, frequencia, angulo_incidencia):
        beta = self.beta(frequencia, angulo_incidencia)
        zs = self.zm(modo, frequencia, angulo_incidencia)
        return zs*math.tan(beta*self.l)

    def largura_salisbury(self, frequencia, angulo_incidencia):
        beta = self.beta(frequencia, angulo_incidencia)
        return math.pi / (2 * beta)

    def frequencia_salisbury(self, largura, angulo_incidencia):
        return self.v / (4 * largura)
