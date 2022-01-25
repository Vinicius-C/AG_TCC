import math
import numpy as np

from AG import AG
from AGUtil import AGUtil
from EspiraQuadrada import EspiraQuadrada
from FSS import FSS
from Individuo import Individuo
from Substrato import Substrato


class AGArranjo(AG):
    # Criar geração inicial do arranjo
    def __init__(self):
        super().__init__()
        dados = self.dados

        self.passos = dados["PASSOS_ARRANJO"]
        self.otimizacao = dados["OTIMIZACAO_ARRANJO"]
        self.max_geracoes = dados["MAX_GERACOES_ARRANJO"]
        self.max_repeticao = dados["MAX_REPETICAO_FITNESS_ARRANJO"]

        self.busca_dieletrico = dados["BUSCA_DIELETRICO"]
        self.busca_espira = dados["BUSCA_ESPIRA"]

        self.er = dados["ER"]
        self.ur = dados["UR"]

        self.pesos_absorcao = dados["PESOS_ABSORCAO"]
        # Colocando intervalo correto nos pesos (Onde era nulo)
        self.pesos_absorcao[0][0] = self.intervalo_curva[0]
        self.pesos_absorcao[3][1] = self.intervalo_curva[1]
        self.pesos_absorcao[4][1] = self.intervalo_curva[1]
        self.set_pesos()

        self.set_passos_antena(self.passos)

        self.curva_a()
        self.curva_r_t_metalic_fss()

        self.set_limites_dieletrico()

    def set_limites_dieletrico(self):
        substrato = Substrato(None, None, None)
        substrato.e = substrato.e0 * self.er
        substrato.u = substrato.u0 * self.ur

        # Intervalo: intervalo_salisbury[0]-intervalo_salisbury[1] (Definido pelo usuário)
        self.l_inf = substrato.largura_salisbury(
            self.dados["INTERVALO_SALISBURY"][0] * 10 ** 9, self.angulo_incidencia
        )
        self.l_sup = substrato.largura_salisbury(
            self.dados["INTERVALO_SALISBURY"][1] * 10 ** 9, self.angulo_incidencia
        )

    # Setar a curva com pesos em cada faixa de frequência para fitness de absorção
    def set_pesos(self):
        self.pesos = []

        passos_faixa1 = self.calcula_passos(self.pesos_absorcao[0])
        self.pesos.extend(np.ones(passos_faixa1) * self.pesos_absorcao[0][2])

        passos_faixa2 = self.calcula_passos(self.pesos_absorcao[1])
        self.pesos.extend(np.ones(passos_faixa2) * self.pesos_absorcao[1][2])

        passos_faixa3 = self.calcula_passos(self.pesos_absorcao[2])
        self.pesos.extend(np.ones(passos_faixa3) * self.pesos_absorcao[2][2])

        self.pesos.extend(np.ones(self.passos - passos_faixa1 -
                                  passos_faixa2 - passos_faixa3) * self.pesos_absorcao[3][2])

    def set_geracao_arranjo(self):
        super().set_geracao(self.gerar_individuo_arranjo)

    # Individuo sendo o arranjo inteiro
    def gerar_individuo_arranjo(self):
        # Dieletrico
        substrato = Substrato(None, None, None)

        if self.busca_dieletrico:
            e = substrato.e0 *\
                AGUtil.gerar_no_intervalo(self.dados["INTERVALO_PRIMEIRO_E"])
            u = substrato.u0 *\
                AGUtil.gerar_no_intervalo(self.dados["INTERVALO_PRIMEIRO_U"])

            substrato.e = e
            substrato.u = u

            # Intervalo: intervalo_salisbury[0]-intervalo_salisbury[1] (Definido pelo usuário)
            l_inf = substrato.largura_salisbury(
                self.dados["INTERVALO_SALISBURY"][0] * 10 ** 9, self.angulo_incidencia
            )
            l_sup = substrato.largura_salisbury(
                self.dados["INTERVALO_SALISBURY"][1] * 10 ** 9, self.angulo_incidencia
            )
            # Intervalo definido pelo usuário onde pode haver Salisbury's Screen
            l = AGUtil.gerar_no_intervalo([l_inf, l_sup])
        else:
            e = substrato.e0 * self.er
            u = substrato.u0 * self.ur
            # Intervalo definido pelo usuário onde pode haver Salisbury's Screen
            l = AGUtil.gerar_no_intervalo([self.l_inf, self.l_sup])

        # Espira Quadrada
        p = AGUtil.gerar_no_intervalo(self.dados["INTERVALO_P_PRIMEIRO_ARRANJO"])
        d = AGUtil.gerar_no_intervalo(self.dados["INTERVALO_D/P_PRIMEIRO_ARRANJO"]) * p
        w = AGUtil.gerar_no_intervalo(self.dados["INTERVALO_W/D_PRIMEIRO_ARRANJO"]) * d

        # Rop = Zm^2*tan(km*d)^2/Z0
        frequencia = (10 ** 9) * 9
        dieletrico = Substrato(l, e, u)
        zm = dieletrico.get_impedancia(self.modo, frequencia, self.angulo_incidencia)
        r = (zm ** 2) / FSS.z0

        # EspiraQuadrada(Tamanho Quadrado Maior, Espessura, Periodicidade, Resistência,
        # Largura Dieletrico, Permissividade, Permeabilidade)
        individuo = Individuo()
        individuo.set_arranjo(d, w, p, r, l, e, u)
        return individuo

    def solve_arranjo(self, individuo):
        curva = []
        zfssr = []
        zfssi = []
        list_zsubstrato = []
        zr = []

        d = individuo.d
        w = individuo.w
        p = individuo.p
        r = individuo.r
        e = individuo.e
        u = individuo.u
        l = individuo.l

        substrato = Substrato(l, e, u)
        espira_quadrada = EspiraQuadrada(d, w, p, r)

        # Grating Lobe
        if p * (1 + math.sin(self.angulo_incidencia)) > FSS.vluz / (self.intervalo_curva[1] * 10 ** 9):
            return {
                "fitness": 9999999
            }
        for i in range(self.passos):
            frequencia = self.frequencia_hz(passo=i)

            z = espira_quadrada.calculo_impedancia(frequencia, self.angulo_incidencia)

            zfss = z[0] + 1j * z[1]
            abcd_fss = [
                [1, 0],
                [1 / zfss, 1]
            ]

            beta = substrato.beta(frequencia, self.angulo_incidencia)
            zd = substrato.zm(self.modo, frequencia, self.angulo_incidencia)

            abcd_substrato = [
                [math.cos(beta * l), zd * math.sin(beta * l) * 1j],
                [1j * math.sin(beta * l) / zd, math.cos(beta * l)]
            ]

            abcd = np.dot(abcd_fss, abcd_substrato)

            # Se houver espira quadrada passa-faixa selecionada anteriormente
            if self.espira_passa_faixa is not None:
                x = self.espira_passa_faixa
                espira_passa_faixa = EspiraQuadrada(x.d, x.w, x.p, x.e)
                # Grating Lobe
                if x.p * (1 + math.sin(self.angulo_incidencia)) > FSS.vluz / (self.intervalo_curva[1] * 10 ** 9):
                    return {
                        "fitness": 9999999
                    }
                z2 = espira_passa_faixa.calculo_impedancia(frequencia, self.angulo_incidencia)
                zfss2 = z2[0] + 1j * z2[1]
                abcd_passa_faixa = [
                    [1, 0],
                    [1 / zfss2, 1]
                ]

                abcd = np.dot(abcd, abcd_passa_faixa)

            x2 = AGUtil.calculo_db(self.otimizacao, abcd, espira_quadrada.z0)
            curva = np.append(curva, 10 * math.log(x2, 10))
            zfssr = np.append(zfssr, z[0])
            zfssi = np.append(zfssi, z[1])
            zdieletrico = zd * math.tan(beta * l)
            list_zsubstrato = np.append(list_zsubstrato, zdieletrico)
            zr = np.append(zr, (1j * zdieletrico * (z[0] + 1j * z[1]) / (1j * zdieletrico + (z[0] + 1j * z[1]))))

        diferenca = []
        curva_normalizada = []
        curva_fitness = []

        f = 0

        if self.otimizacao == "r":
            curva_normalizada = np.true_divide(curva, max(np.abs(curva))) + 1
            diferenca = curva_normalizada - self.curva_referencia_r
            f = np.sum(np.square(diferenca))
        elif self.otimizacao == "t":
            curva_normalizada = np.true_divide(curva, max(np.abs(curva))) + 1
            diferenca = curva_normalizada - self.curva_referencia_t
            f = np.sum(np.square(diferenca))
        elif self.otimizacao == "a":
            curva_normalizada = np.true_divide(curva, max(np.abs(curva)))
            diferenca = curva_normalizada - self.curva_referencia_a
            diferenca = np.multiply(diferenca, self.pesos)

            x = abs(np.max(curva))
            f = np.sum(np.square(diferenca)) * (1 / x ** 2)
            g = abs(espira_quadrada.calculo_impedancia(15 * 10 ** 9, self.angulo_incidencia)[1])
            f *= (g ** 2 / 1000) + 1

        return {
            "fitness": f,
            "curva normalizada": curva_normalizada,
            "curva": curva,
            "zfssr": zfssr,
            "zfssi": zfssi,
            "zsubstrato": list_zsubstrato,
            "diferenca ao quadrado": np.square(diferenca),
            "zrr": zr.real,
            "zri": zr.imag,
            "curva_fitness": curva_fitness,
        }

    def crossover_arranjo(self, macho, femea):
        # Ultrapassagem do crossover, assim será possivel o filho ter um valor fora do intervalo dos pais
        n = self.ultrapassagem_crossover

        espira_quadrada = super().crossover(n, macho, femea)
        d = espira_quadrada.d
        w = espira_quadrada.w
        p = espira_quadrada.p
        r = espira_quadrada.r

        if self.busca_dieletrico:
            l = AGUtil.combinar_real(n, [self.l_inf, self.l_sup], macho.l, femea.l)
            # Limites de p: [0, 5eo]
            e = AGUtil.combinar_real(n, [0.8 * Substrato.e0, 1.6 * Substrato.e0], macho.e, femea.e)
            # Limites de p: [0, 5u0]
            u = macho.u
            # u = self.combinar_real(n, [0.8*1.2566*(10**-6), 2*1.2566*(10**-6)], macho.u, femea.u)
        else:
            e = self.er * Substrato.e0
            u = self.ur * Substrato.u0
            l = AGUtil.combinar_real(n, [self.l_inf, self.l_sup], macho.l, femea.l)

        resultado = Individuo()
        resultado.set_arranjo(d, w, p, r, l, e, u)

        return resultado
