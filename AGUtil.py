import numpy as np
import random
import json


class AGUtil:
    def __init__(self):
        dados = self.ler_config()

        self.dados = dados

        self.taxa_mutacao = dados["TAXA_MUTACAO"]
        self.ultrapassagem_crossover = dados["ULTRAPASSAGEM_CROSSOVER"]
        self.tamanho_geracao = dados["TAMANHO_GERACAO"]
        self.intervalo_curva = dados["INTERVALO_CURVA"]
        self.faixa_f_antena = dados["FAIXA_ANTENA"]
        self.n_selecionados = dados["N_SELECIONADOS"]
        self.modo = dados["MODO"]
        self.angulo_incidencia = dados["ANGULO_INCIDENCIA"]

        self.passos = None
        self.passo_comeco_banda = None
        self.passo_fim_banda = None
        self.rank_weight = None

        self.curva_referencia_r = None
        self.curva_referencia_t = None
        self.curva_referencia_a = None

    def set_passos_antena(self, passos):
        self.passo_comeco_banda = int(passos * ((self.faixa_f_antena[0] - self.intervalo_curva[0]) /
                                                (self.intervalo_curva[1] - self.intervalo_curva[0])))
        self.passo_fim_banda = int(passos * ((self.faixa_f_antena[1] - self.intervalo_curva[0]) /
                                             (self.intervalo_curva[1] - self.intervalo_curva[0])))

    @staticmethod
    def ler_config():
        with open("Config.json", encoding='utf-8') as ag_config:
            dados = json.load(ag_config)
        return dados

    def calcula_passos(self, intervalo):
        return int(self.passos * ((intervalo[1] - intervalo[0]) /
                                  (self.intervalo_curva[1] - self.intervalo_curva[0])))

    # Setar a curva com funcionamento ideal de absorção e transmissão
    def curva_a(self):
        # Array contendo a curva com funcionamento ideal de absorção
        self.curva_referencia_a = []

        self.curva_referencia_a = np.append(self.curva_referencia_a,
                                            np.zeros(self.passo_comeco_banda))

        self.curva_referencia_a = np.append(self.curva_referencia_a,
                                            np.zeros(self.passo_fim_banda - self.passo_comeco_banda))

        self.curva_referencia_a = np.append(self.curva_referencia_a,
                                            np.ones(self.passos - self.passo_fim_banda))

    # Setar a curva com funcionamento ideal de reflexão e transmissão
    def curva_r_t_metalic_fss(self):
        # Array contendo a curva com funcionamento ideal de transmissão
        self.curva_referencia_t = []
        # Array contendo a curva com funcionamento ideal de reflexão
        self.curva_referencia_r = []
        self.curva_referencia_r = np.append(self.curva_referencia_r,
                                            np.ones(self.passo_comeco_banda))
        self.curva_referencia_t = np.append(self.curva_referencia_t,
                                            np.zeros(self.passo_comeco_banda))

        self.curva_referencia_r = np.append(self.curva_referencia_r,
                                            np.zeros(self.passo_fim_banda - self.passo_comeco_banda))
        self.curva_referencia_t = np.append(self.curva_referencia_t,
                                            np.ones(self.passo_fim_banda - self.passo_comeco_banda))

        self.curva_referencia_r = np.append(self.curva_referencia_r,
                                            np.ones(self.passos - self.passo_fim_banda))
        self.curva_referencia_t = np.append(self.curva_referencia_t,
                                            np.zeros(self.passos - self.passo_fim_banda))

    # Z é a impedância
    @staticmethod
    def calculo_db(otimizacao, abcd, z0):
        a = abcd[0][0]
        b = abcd[0][1]
        c = abcd[1][0]
        d = abcd[1][1]

        x2 = 0

        if otimizacao == "r":
            x2 = abs(((a + b / z0 - c * z0 - d) / (a + b / z0 + c * z0 + d)) ** 2)
        elif otimizacao == "t":
            x2 = abs((2 / (a + b / z0 + c * z0 + d)) ** 2)
        elif otimizacao == "a":
            r2 = abs(((a + b / z0 - c * z0 - d) / (a + b / z0 + c * z0 + d)) ** 2)
            t2 = abs((2 / (a + b / z0 + c * z0 + d)) ** 2)
            x2 = 1 / (r2 + t2)

        # Erro de arredondamento, x2 não pode ser 1
        if x2 == 1:
            x2 = 0.9999
        elif x2 == 0:
            x2 = 0.00001

        return x2

    def selecionar_mate(self, selecionados, n_individuos):
        p = random.random()
        mate = None
        self.set_rank_weight(n_individuos)
        for m in range(n_individuos):
            if p < self.rank_weight[m]:
                mate = selecionados[m]
                break
        return mate

    def set_rank_weight(self, n_selecionados):
        soma = (1 + n_selecionados) * n_selecionados / 2
        acumulado = 0
        self.rank_weight = []
        for i in range(1, n_selecionados + 1):
            acumulado += (n_selecionados - i + 1) / soma
            self.rank_weight.append(acumulado)

    # Com o multiplicador é possível haver uma combinação fora do intervalor entre n1 e n2
    @staticmethod
    def combinar_real(multiplicador, limite, n1, n2):
        gene_maior, gene_menor, intervalo = None, None, [None, None]

        if n2 > n1:
            gene_maior = n2 * (1 + multiplicador)
            gene_menor = n1 * (1 - multiplicador)
        else:
            gene_maior = n1 * (1 + multiplicador)
            gene_menor = n2 * (1 - multiplicador)

        if limite[0] < gene_menor:
            intervalo[0] = gene_menor
        else:
            intervalo[0] = limite[0]

        if limite[1] > gene_maior:
            intervalo[1] = gene_maior
        else:
            intervalo[1] = limite[1]

        if intervalo[0] > intervalo[1]:
            intervalo = [limite[0], limite[1]]

        beta = random.random()

        return intervalo[0]*(1-beta) + intervalo[1]*beta

    def frequencia_hz(self, passo):
        return (10 ** 9) * (self.intervalo_curva[0] + (passo / self.passos) *
                            (self.intervalo_curva[1] - self.intervalo_curva[0]))

    @staticmethod
    def gerar_no_intervalo(intervalo):
        return intervalo[0] + (intervalo[1] - intervalo[0]) * random.random()
