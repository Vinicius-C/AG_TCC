import numpy as np

from matplotlib import pyplot as plt

from AGEspiraQuadrada import AGEspiraQuadrada
from AGArranjo import AGArranjo

from Individuo import Individuo
from Plots import Plots


class AGManager:
    @staticmethod
    def otimizar_espira_quadrada():
        ag = AGEspiraQuadrada()

        ag.set_geracao_espira_quadrada()

        fitness = 0
        count_mesmo_fitness = 0

        plt.xlabel("Genes (p, d, w)")
        plt.ylabel("Valores")
        plt.title("Individuos")
        plt.xlim(2, 8)

        for j in range(ag.max_geracoes):
            x = ag.solve_espira_quadrada(
                ag.nova_geracao(
                    ag.solve_espira_quadrada,
                    ag.crossover_espira_quadrada
                )
            )["fitness"]

            if fitness == x:
                count_mesmo_fitness += 1
            else:
                count_mesmo_fitness = 0
                fitness = x

            if count_mesmo_fitness >= ag.max_repeticao_fitness:
                print("Parada por repetição de fitness: " + str(j) + "\n")
                break

            plt.plot(np.linspace(2.5, 7.5, 3), [ag.geracao[0].p, ag.geracao[0].d, ag.geracao[0].w])

        plt.figure()
        plt.show()
        plt.close()

        # Mostrar melhor
        index_menor = 0
        for i in range(ag.tamanho_geracao):
            if ag.solve_espira_quadrada(ag.geracao[i])["fitness"] <\
                    ag.solve_espira_quadrada(ag.geracao[index_menor])["fitness"]:
                index_menor = i

        espira_quadrada_otima = ag.geracao[index_menor]
        resultado = ag.solve_espira_quadrada(espira_quadrada_otima)

        print("A melhor espira quadrada encontrada foi: ")
        print("d: " + str(espira_quadrada_otima.d))
        print("p: " + str(espira_quadrada_otima.p))
        print("w: " + str(espira_quadrada_otima.w))
        print("r: " + str(espira_quadrada_otima.r))
        print("f: " + str(resultado["fitness"]) + "\n")

        show = Plots(ag=ag)
        show.plotar(
            resultado["curva"],
            x="Frequency (GHz)",
            y=ag.otimizacao.upper() + "(dB)",
            xvline=ag.faixa_f_antena,
            title="S"
        )

        curva_referencia = {
            "r": ag.curva_referencia_r,
            "t": ag.curva_referencia_t,
            "a": ag.curva_referencia_a
        }

        show.plotar(
            curva_referencia[ag.otimizacao],
            x="Frequency (GHz)",
            y=ag.otimizacao.upper() + "[Curva Ideal]",
            xvline=ag.faixa_f_antena,
            title="S"
        )
        show.plotar(
            [
                resultado["z_pass_band_r"],
                resultado["z_pass_band_i"]
            ],
            x="Frequency (GHz)",
            y="Z (Ohms)",
            xvline=ag.faixa_f_antena,
            title="Impedância da FSS",
            many=True
        )

        return espira_quadrada_otima

    @staticmethod
    def otimizar_arranjo(espira_quadrada_otima):
        espira_passa_faixa = espira_quadrada_otima

        ag_artigo = AGArranjo()
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
        resultado_artigo = ag_artigo.solve_arranjo(fss_artigo)

        ag = AGArranjo(referencia=resultado_artigo["curva"])
        ag.espira_passa_faixa = espira_passa_faixa
        ag.set_geracao_arranjo()

        show = Plots(ag=ag)

        fitness = 0
        count_mesmo_fitness = 0

        for j in range(ag.max_geracoes):
            novo = ag.nova_geracao(
                    ag.solve_arranjo,
                    ag.crossover_arranjo
                )
            x = ag.solve_arranjo(novo)

            if fitness == x["fitness"]:
                count_mesmo_fitness += 1
            else:
                title = "S, Fit: {:.2f} - p: {:.2f} - " \
                        "d: {:.2f} - \n w: {:.2f} - r: {:.1f} - " \
                        "e: {:.3f} - u: {:.3f}"
                show.plotar(
                    [
                        x["curva"],
                        resultado_artigo["curva"]
                    ],
                    x="Frequency (GHz)",
                    y=ag.otimizacao.upper() + "(dB) [Novo Fitness]",
                    xvline=ag.faixa_f_antena,
                    title=title.format(
                        x["fitness"],
                        novo.p * 10 ** 3,
                        novo.d * 10 ** 3,
                        novo.w * 10 ** 3,
                        novo.r,
                        novo.e * 10 ** 12,
                        novo.u * 10 ** 7
                    ),
                    many=True
                )
                print(novo.r)
                count_mesmo_fitness = 0
                fitness = x["fitness"]
                
            if count_mesmo_fitness >= ag.max_repeticao_fitness:
                print("Parada por repetição de fitness: " + str(j))
                break

        # Mostrar melhor
        index_menor = 0
        for i in range(ag.tamanho_geracao):
            if ag.solve_arranjo(ag.geracao[i])["fitness"] <\
                    ag.solve_arranjo(ag.geracao[index_menor])["fitness"]:
                index_menor = i

        arranjo_otimo = ag.geracao[index_menor]

        show.plots_arranjo(ag, ag.solve_arranjo(arranjo_otimo))

        print("d: " + str(arranjo_otimo.d))
        print("p: " + str(arranjo_otimo.p))
        print("w: " + str(arranjo_otimo.w))
        print("r: " + str(arranjo_otimo.r))
        print("e: " + str(arranjo_otimo.e))
        print("u: " + str(arranjo_otimo.u))
        print("l: " + str(arranjo_otimo.l))
        print("f: " + str(ag.solve_arranjo(arranjo_otimo)["fitness"]) + "\n")

    def plotar_arranjo(self, individuo, espira_passa_faixa):
        ag = AGArranjo()
        ag.espira_passa_faixa = espira_passa_faixa
        show = Plots(ag=ag)
        show.plots_arranjo(ag, ag.solve_arranjo(individuo))

    def plotar_espira(self, individuo, x="x", y="y", title="Title"):
        ag = AGEspiraQuadrada()
        show = Plots(ag=ag)

        resultado = ag.solve_espira_quadrada(individuo)

        '''show.plotar(
            resultado["curva"],
            x="GHz",
            y="A(db)",
            xvline=ag.faixa_f_antena,
            title="Resultado"
        )
        show.plotar(
            resultado["s1"],
            x="Frequency (GHz)",
            y="S (dB)",
            xvline=ag.faixa_f_antena,
            title="S1"
        )
        show.plotar(
            resultado["s2"],
            x="Frequency (GHz)",
            y="S (dB)",
            xvline=ag.faixa_f_antena,
            title="S2"
        )
        show.plotar(
            resultado["s3"],
            x="Frequency (GHz)",
            y="S (dB)",
            xvline=ag.faixa_f_antena,
            title="S3"
        )
        show.plotar(
            resultado["s4"],
            x="Frequency (GHz)",
            y="S (dB)",
            xvline=ag.faixa_f_antena,
            title="S4"
        )'''