import numpy as np

from Substrato import Substrato
from AGUtil import AGUtil

class Individuo:
    fitness = None

    # Curva de Absorção
    curva_a = None
    # Curva de Transmissão
    curva_t = None
    # Curva de Reflexão
    curva_r = None

    # Primeira Espira Quadrada
    d = None
    p = None
    w = None
    r = None

    # Dielétrico
    l = None
    e = None
    u = None

    def __str__(self):
        return 'p: {}, d: {}, w: {}, r{}'.format(self.p, self.d, self.w, self.r)

    # set_arranjo(Tamanho Quadrado Maior, Espessura, Periodicidade, Resistência,
    # Largura Dieletrico, Permissividade, Permeabilidade)
    def set_arranjo(self, d, w, p, r, l, e, u):
        self.d = d
        self.w = w
        self.p = p
        self.r = r

        self.l = l
        self.e = e
        self.u = u

    # set_espira_quadrada(Tamanho Quadrado Maior, Espessura, Periodicidade, Resistência)
    def set_espira_quadrada(self, d, w, p, r):
        self.d = d
        self.w = w
        self.p = p
        self.r = r

        self.l = 0
        self.e = 0
        self.u = 0

    @staticmethod
    def mutar_variavel(taxa_mutacao, variavel, limite_inf, limite_sup):
        if variavel == 0:
            return 0
        c = 0
        while True:
            c += 1
            mutar = np.random.normal(1, taxa_mutacao)
            valor = variavel * mutar
            if c >= 5:
                if limite_inf <= valor:
                    return limite_sup
                else:
                    return limite_inf
            if limite_inf <= valor < limite_sup:
                return valor

    def mutacao(self, taxa_mutacao, busca_dieletrico, l_inf, l_sup, intervalo_salisbury, angulo_incidencia, dados):

        self.p = self.mutar_variavel(
            taxa_mutacao,
            self.p,
            dados["INTERVALO_P_PRIMEIRO_ESPIRA_VALIDO"][0],
            dados["INTERVALO_P_PRIMEIRO_ESPIRA_VALIDO"][1]
        )
        self.d = self.mutar_variavel(
            taxa_mutacao,
            self.d,
            dados["INTERVALO_D/P_PRIMEIRO_ESPIRA_VALIDO"][0] * self.p,
            dados["INTERVALO_D/P_PRIMEIRO_ESPIRA_VALIDO"][1] * self.p
        )
        self.w = self.mutar_variavel(
            taxa_mutacao,
            self.w,
            dados["INTERVALO_W/D_PRIMEIRO_ESPIRA_VALIDO"][0] * self.d,
            dados["INTERVALO_W/D_PRIMEIRO_ESPIRA_VALIDO"][1] * self.d
        )
        self.r = self.mutar_variavel(
            taxa_mutacao,
            self.r,
            dados["INTERVALO_R_PRIMEIRO_ESPIRA_VALIDO"][0],
            dados["INTERVALO_R_PRIMEIRO_ESPIRA_VALIDO"][1]
        )
        if busca_dieletrico:
            self.e = self.mutar_variavel(
                taxa_mutacao,
                self.e,
                dados["INTERVALO_E/E0_PERMITIDO"][0] * 8.85418 * (10 ** -12),
                dados["INTERVALO_E/E0_PERMITIDO"][1] *  8.85418 * (10 ** -12)
            )
            # self.u = self.mutar_variavel(taxa_mutacao, self.u, 0.8*1.2566*(10**-6), 1.2*1.2566*(10**-6))
            # Intervalo: intervalo_salisbury[0]-intervalo_salisbury[1] (Definido pelo usuário)
            substrato = Substrato(None, self.e, self.u)
            l_inf = substrato.largura_salisbury(
                intervalo_salisbury[1] * 10 ** 9,
                angulo_incidencia
            )
            l_sup = substrato.largura_salisbury(
                intervalo_salisbury[0] * 10 ** 9,
                angulo_incidencia
            )
            self.l = self.mutar_variavel(taxa_mutacao, self.l, l_inf, l_sup)

        else:
            self.l = self.mutar_variavel(taxa_mutacao, self.l, l_inf, l_sup)
