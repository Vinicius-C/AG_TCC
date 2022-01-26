from datetime import datetime

from AGUtil import AGUtil
from AGManager import AGManager
from Individuo import Individuo
from EspiraQuadrada import EspiraQuadrada

class Main:
    time_inicio = 0

    def __init__(self):
        self.time_inicio = datetime.now()

    def show_time(self):
        now = datetime.now()
        print("Horário: ", now)
        print("Tempo de Execução: ", now - self.time_inicio, "\n")

    def run(self):
        print("Início")
        self.show_time()

        espira_quadrada_otima = EspiraQuadrada(
            tamanho=10.7255e-3,
            espessura=0.7444e-4,
            periodicidade=11.5145e-3,
            resistencia = 0
        )

        manager = AGManager()
        #espira_quadrada_otima = manager.otimizar_espira_quadrada()
        espira_quadrada_otima = AGUtil().get_passa_faixa(espira_quadrada_otima)

        print("Passa-Faixa Finalizada")
        self.show_time()

        fss_artigo = Individuo()
        fss_artigo.set_arranjo(
            w=0.011 * 3 / 16,
            d=0.011 * 14 / 16,
            p=0.011,
            r=260,
            l=0.005,
            e=1.01 * 8.85418 * (10 ** -12),
            u=1.2566 * (10 ** -6)
        )

        fss = Individuo()
        fss.set_arranjo(
            d=0.006443234849969896,
            p=0.011875353218173514,
            w=7.231710347257352e-05,
            r=800,
            e=9.296889e-12,
            u=1.2566e-06,
            l=0.0045714363307545105
        )
        manager.plotar_arranjo(fss_artigo, espira_quadrada_otima)
        manager.plotar_arranjo(fss, espira_quadrada_otima)
        #manager.plotar_espira(espira_quadrada_otima)

        #manager.otimizar_arranjo(espira_quadrada_otima)

        print("Arranjo Finalizado")
        self.show_time()

main = Main()
main.run()
