from datetime import datetime

from AGManager import AGManager
from Individuo import Individuo


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

        manager = AGManager()
        espira_quadrada_otima = manager.otimizar_espira_quadrada()

        print("Passa-Faixa Finalizada")
        self.show_time()

        fss_artigo = Individuo()
        fss_artigo.set_arranjo(
            d=0.011 * 1 / 16,
            w=0.011 * 5 / 8,
            p=0.011,
            r=260,
            l=0.005,
            e=1.01 * 8.85418 * (10 ** -12),
            u=1.2566 * (10 ** -6)
        )

        manager.plotar_arranjo(fss_artigo, x="GHz", y="A(db)", title="Arranjo do Artigo")

        manager.otimizar_arranjo(espira_quadrada_otima)

        print("Arranjo Finalizado")
        self.show_time()

main = Main()
main.run()
