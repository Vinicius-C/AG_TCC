from FSS import FSS


class EspiraQuadrada(FSS):
    # Periodicidade
    p = None
    # Tamanho do Quadrado Maior
    d = None
    # Espessura
    w = None
    # Resistencia
    r = None

    def __str__(self):
        return 'p: {}, d: {}, w: {}'.format(self.p, self.d, self.w)

    def __init__(self, tamanho, espessura, periodicidade, resistencia):
        super().__init__()
        self.d = tamanho
        self.w = espessura
        self.p = periodicidade
        self.r = resistencia

    def calculo_impedancia(self, frequencia, angulo_incidencia):
        xl = self.z0*self.d/self.p*self.f(self.p, 2*self.w, self.vluz/frequencia, angulo_incidencia)
        bc = 4*self.d/self.p*self.f(self.p, self.p-self.d, self.vluz/frequencia, angulo_incidencia)/self.z0

        # A Variável bc Não Pode Ser 0, Pois Existe 1/bc
        if bc == 0:
            bc = 0.000001

        return {
            "r": self.r,
            "x": xl-1/bc,
            "xl": xl,
            "bc": bc
        }
