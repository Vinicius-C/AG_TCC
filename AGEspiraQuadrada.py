import math
import numpy as np
import random

from AG import AG
from AGUtil import AGUtil
from EspiraQuadrada import EspiraQuadrada
from FSS import FSS
from Individuo import Individuo


class AGEspiraQuadrada(AG):
    # Criar geração inicial da espira quadrada
    def __init__(self):
        super().__init__()
        dados = self.dados

        self.passos = dados["PASSOS_ESPIRA"]
        self.otimizacao = dados["OTIMIZACAO_ESPIRA"]
        self.max_geracoes = dados["MAX_GERACOES_ESPIRA"]
        self.max_repeticao_fitness = dados["MAX_REPETICAO_FITNESS_ESPIRA"]

        self.set_passos_antena(self.passos)

        self.curva_a()
        self.curva_r_t_metalic_fss()

    def set_geracao_espira_quadrada(self):
        super().set_geracao(self.gerar_individuo_espira_quadrada)

    def gerar_individuo_espira_quadrada(self):
        # Espira Quadrada
        p = AGUtil.gerar_no_intervalo(self.dados["INTERVALO_P_PRIMEIRO_ESPIRA"])
        d = AGUtil.gerar_no_intervalo(self.dados["INTERVALO_D/P_PRIMEIRO_ESPIRA"]) * p
        w = AGUtil.gerar_no_intervalo(self.dados["INTERVALO_W/D_PRIMEIRO_ESPIRA"]) * d

        r = 0

        # set_espira_quadrada(Tamanho Quadrado Maior, Espessura, Periodicidade, Resistência)
        individuo = Individuo()
        individuo.set_espira_quadrada(d, w, p, r)
        return individuo

    def solve_espira_quadrada(self, individuo):
        curva = []
        zespira = []
        z_pass_band_r = []
        z_pass_band_i = []

        d = individuo.d
        w = individuo.w
        p = individuo.p
        r = individuo.r

        # Grating Lobe
        if p * (1 + math.sin(self.angulo_incidencia)) > FSS.vluz / (self.intervalo_curva[1] * 10 ** 9):
            return {
                "fitness": 9999999
            }

        espira_quadrada = EspiraQuadrada(d, w, p, r)

        for i in range(self.passos):
            frequencia = self.frequencia_hz(passo=i)

            z = espira_quadrada.calculo_impedancia(frequencia, self.angulo_incidencia)
            zfss = z["r"] + 1j * z["x"]
            abcd = [
                    [1, 0],
                    [1 / zfss, 1]
                   ]

            z_pass_band_r.append(z["r"])
            z_pass_band_i.append(z["x"])

            s_ao_quadrado = AGUtil.calculo_s2(self.otimizacao, abcd, espira_quadrada.z0)

            zespira = np.append(curva, abs(zfss))
            curva = np.append(curva, 10 * math.log(1 - s_ao_quadrado, 10))

        curva_normalizada = np.true_divide(curva, max(np.abs(curva))) + 1

        diferenca = []

        if self.otimizacao == "r":
            diferenca = curva_normalizada - self.curva_referencia_r
            c = self.dados["SENSIBILIDADE_FAIXA_ESPIRA"]
            diferenca = np.array(diferenca) * (c / (c - 1) - np.array(self.curva_referencia_r))
        elif self.otimizacao == "t":
            diferenca = curva_normalizada - self.curva_referencia_t
        elif self.otimizacao == "a":
            diferenca = curva_normalizada - self.curva_referencia_a

        
        pico = abs(np.min(curva))
        f = np.sum(np.square(diferenca)) * ((pico + 10) / pico)

        return {
                "fitness": f,
                "curva_normalizada": curva_normalizada,
                "curva": curva,
                "impedancia": zespira,
                "z_pass_band_r": z_pass_band_r,
                "z_pass_band_i": z_pass_band_i
        }

    def crossover_espira_quadrada(self, macho, femea):
        # Ultrapassagem do crossover, assim será possivel o filho ter um valor fora do intervalo dos pais
        n = self.ultrapassagem_crossover

        # Limites de p: [1e-4, 9999]
        p = AGUtil.combinar_real(n, [1e-4, 9999], macho.p, femea.p)
        # Limites de d: [1e-4, 0.9p]
        d = AGUtil.combinar_real(n, [1e-4, 0.9 * p], macho.d, femea.d)
        # Limites de w: [1e-4, d/2]
        w = AGUtil.combinar_real(n, [1e-4, d / 2], macho.w, femea.w)
        # Limites de p: [0, 9999]
        r = AGUtil.combinar_real(n, [0, 9999], macho.r, femea.r)

        resultado = Individuo()
        resultado.set_espira_quadrada(d, w, p, r)

        return resultado
