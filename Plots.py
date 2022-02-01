import numpy as np


from matplotlib import pyplot as plt


class Plots:
    eixo_x = None

    def __init__(self, ag=None, linspace=None):
        if ag is not None:
            self.eixo_x = np.linspace(ag.intervalo_curva[0], ag.intervalo_curva[1], ag.passos)
        if linspace is not None:
            self.eixo_x = linspace

    def plotar(self, dados, x="x", y="y", title="Title", legends=None, xvline=None, ylim=None, many=False):
        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])

        if xvline is not None:
            plt.axvline(x=xvline[0])
            plt.axvline(x=xvline[1])

        plt.grid(linestyle="dotted")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)

        if not many:
            if legends is not None:
                plt.plot(
                    self.eixo_x,
                    dados,
                    color=legends["color"],
                    label=legends["label"]
                )
            else:
                plt.plot(
                    self.eixo_x,
                    dados
                )
            try:
                plt.legend()
            finally:
                plt.show()
        else:
            i = 0

            for dado in dados:
                if legends is not None:
                    plt.plot(
                        self.eixo_x, dado,
                        color=legends[i]["color"],
                        label=legends[i]["label"]
                    )
                else:
                    plt.plot(self.eixo_x, dado)

                i += 1
            try:
                plt.legend()
            finally:
                plt.show()

    def plots_arranjo(self, ag, dados):
        self.plotar(
            dados["curva"],
            legends={
                "color": "#17a589",
                "label": "Absorção da RFSS + Dielétrico - Referência"
            },
            x="Frequencia (GHz)",
            y=ag.otimizacao.upper() + "(dB)",
            xvline=ag.faixa_f_antena,
            title="Referência"
        )

        self.plotar(
            dados["s11"],
            legends={
                "color": "#17a589",
                "label": "Reflexão da RFSS + Dielétrico"
            },
            x="Frequency (GHz)",
            y="S11 (dB)",
            xvline=ag.faixa_f_antena,
            title="Solução"
        )

        self.plotar(
            dados["s12"],
            legends={
                "color": "#17a589",
                "label": "Transmissão da RFSS + Dielétrico"
            },
            x="Frequency (GHz)",
            y="S12 (dB)",
            xvline=ag.faixa_f_antena,
            title="Solução"
        )

        use_ground = ag.dados["UTILIZAR_GROUND"]

        if not use_ground:
            self.plotar(
                dados["z_pass_band_r"],
                legends={
                    "color": "#17a589",
                    "label": "Resistência da FSS Passa Banda"
                },
                x="Frequency (GHz)",
                y="Re{Z_Pass-Band} (dB)",
                xvline=ag.faixa_f_antena,
                title="Solução: Passa Faixa"
            )

            self.plotar(
                dados["z_pass_band_i"],
                legends={
                    "color": "#17a589",
                    "label": "Reatância da FSS Passa Banda"
                },
                x="Frequency (GHz)",
                y="Im{Z_EQ} (dB)",
                xvline=ag.faixa_f_antena,
                title="Solução: Passa Faixa"
            )

        metodo = ag.dados["METODO_FITNESS_ARRANJO"]

        if metodo == "compare_ideal":
            self.plotar(
                [
                    dados["curva normalizada"],
                    ag.curva_referencia_a,
                    dados["diferenca ao quadrado"]
                ],
                legends=[
                    {"color": "#17a589", "label": "Curva Normalizada"},
                    {"color": "#f4d03f", "label": "Curva A Ideal"},
                    {"color": "red", "label": "Diferença²"}
                ],
                x="Frequency (GHz)",
                y="A Normalizado",
                xvline=ag.faixa_f_antena,
                title="Curvas Normalizadas",
                many=True
            )

        elif metodo == "sum_influence":
            self.plotar(
                [
                    dados["curva normalizada"],
                    ag.curva_referencia_a,
                    dados["curva_fitness"]
                ],
                legends=[
                    {"color": "#17a589", "label": "Curva Normalizada"},
                    {"color": "#f4d03f", "label": "Curva A Ideal"},
                    {"color": "red", "label": "Influência no Fitness"}
                ],
                x="Frequency (GHz)",
                y="A Normalizado",
                xvline=ag.faixa_f_antena,
                title="Curvas Normalizadas",
                many=True
            )

        elif metodo == "compare_curve":
            self.plotar(
                [
                    dados["curva normalizada"],
                    ag.curva_referencia_a,
                    dados["curva_fitness"]
                ],
                legends=[
                    {"color": "#17a589", "label": "Curva Normalizada"},
                    {"color": "#f4d03f", "label": "Curva A Ideal"},
                    {"color": "red", "label": "Influência no Fitness"}
                ],
                x="Frequency (GHz)",
                y="A Normalizado",
                xvline=ag.faixa_f_antena,
                title="Curvas Normalizadas",
                many=True
            )


        self.plotar(
            dados["zfssr"],
            legends={
                "color": "#17a589",
                "label": "Resistência da RFSS"
            },
            x="Frequency (GHz)",
            y="Re{Z_RFSS} (Ohm)",
            xvline=ag.faixa_f_antena,
            title="Parte Real da Impedância da RFSS"
        )

        self.plotar(
            dados["zsubstrato"],
            legends={
                "color": "#17a589",
                "label": "Módulo da Impedância do Substrato"
            },
            x="Frequency (GHz)",
            y="Zd (Ohm)",
            xvline=ag.faixa_f_antena,
            ylim=[-2000, 2000],
            title="Impedância do Substrato"
        )

        self.plotar(
            [
                dados["zfssi"],
                dados["zsubstrato"],
                dados["zfssi"] + dados["zsubstrato"]
            ],
            legends=[
                {"color": "#17a589", "label": "Reatância da RFSS"},
                {"color": "#f4d03f", "label": "Impedância do Dielétrico"},
                {"color": "red", "label": "Soma dos 2 Anteriores"}
            ],
            x="Frequency (GHz)",
            y="I{ZFSS} e Zd (Ohm)",
            xvline=ag.faixa_f_antena,
            ylim=[-1000, 1000],
            title="Ressonância e Salisbury's Screen",
            many=True
        )

        self.plotar(
            [
                dados["zrr"],
                dados["zri"]
            ],
            legends=[
                {"color": "#17a589", "label": "Resistência da RFSS + Dielétrico"},
                {"color": "#f4d03f", "label": "Reatância da RFSS + Dielétrico"}
            ],
            x="Frequency (GHz)",
            y="Zr (Ohm)",
            xvline=ag.faixa_f_antena,
            title="Impedância RFSS + Substrato (Real e Imaginária)",
            many=True
        )
            