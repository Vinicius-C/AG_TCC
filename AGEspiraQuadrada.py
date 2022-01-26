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

        s1 = []
        s2 = []
        s3 = []
        s4 = []

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
                    [1, zfss],
                    [0, 1]
            ]

            '''s1.append(
                AGUtil.calculo_s2(
                    self.otimizacao,
                    [[1, 0],
                     [1 / zfss, 1]],
                    espira_quadrada.z0
                )
            )
            s2.append(AGUtil.calculo_s2(
                    self.otimizacao,
                    [[1, 0],
                     [zfss, 1]],
                    espira_quadrada.z0
                )
            )
            s3.append(AGUtil.calculo_s2(
                    self.otimizacao,
                    [[1, 1 / zfss],
                     [0, 1]],
                    espira_quadrada.z0
                )
            )
            s4.append(
                AGUtil.calculo_s2(
                    self.otimizacao,
                    [[1, zfss],
                     [0, 1]],
                    espira_quadrada.z0
                )
            )'''

            z_pass_band_r.append(z["r"])
            z_pass_band_i.append(z["x"])

            s_ao_quadrado = AGUtil.calculo_s2(self.otimizacao, abcd, espira_quadrada.z0)

            zespira = np.append(curva, abs(zfss))
            curva = np.append(curva, 10 * math.log(s_ao_quadrado, 10))

        curva_normalizada = np.true_divide(curva, max(np.abs(curva))) + 1

        diferenca = []

        if self.otimizacao == "r":
            diferenca = curva_normalizada - self.curva_referencia_r

            pico = abs(np.min(curva))
            f = np.sum(np.square(diferenca)) * ((pico + 10) / pico)

        elif self.otimizacao == "t":
            diferenca = curva_normalizada - self.curva_referencia_t
            c = self.dados["SENSIBILIDADE_FAIXA_ESPIRA"]
            diferenca = np.array(diferenca) * (c / (c - 1) - np.array(self.curva_referencia_r))

            pico = abs(np.max(curva))
            f = np.sum(np.square(diferenca)) * ((pico + 10) / pico)

        elif self.otimizacao == "a":
            diferenca = curva_normalizada - self.curva_referencia_a


        return {
                "fitness": f,
                "curva_normalizada": curva_normalizada,
                "curva": curva,
                "impedancia": zespira,
                "z_pass_band_r": z_pass_band_r,
                "z_pass_band_i": z_pass_band_i,
                "s1": 10*np.log10(s1),
                "s2": 10*np.log10(s2),
                "s3": 10*np.log10(s3),
                "s4": 10*np.log10(s4)
        }

    def crossover_espira_quadrada(self, macho, femea):
        # Ultrapassagem do crossover, assim será possivel o filho ter um valor fora do intervalo dos pais
        n = self.ultrapassagem_crossover

        return super().crossover(n, macho, femea)
