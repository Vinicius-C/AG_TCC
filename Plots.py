import numpy as np


from matplotlib import pyplot as plt


class Plots:
    eixo_x = None

    def __init__(self, ag=None, linspace=None):
        if ag is not None:
            self.eixo_x = np.linspace(ag.intervalo_curva[0], ag.intervalo_curva[1], ag.passos)
        if linspace is not None:
            self.eixo_x = linspace

    def plotar(self, dados, x="x", y="y", title="Title", xvline=None, ylim=None, many=False):
        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])

        if xvline is not None:
            plt.axvline(x=xvline[0])
            plt.axvline(x=xvline[1])

        plt.grid(linestyle='--')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)

        if not many:
            plt.plot(self.eixo_x, dados)
            plt.show()
        else:
            for dado in dados:
                plt.plot(self.eixo_x, dado)
            plt.show()

    def plots_arranjo(self, ag, dados):
        self.plotar(
            dados["curva"],
            x="Frequency (GHz)",
            y=ag.otimizacao.upper() + "(dB)",
            xvline=ag.faixa_f_antena,
            title="Melhor Arranjo"
        )

        self.plotar(
            dados["s11"],
            x="Frequency (GHz)",
            y="S11 (dB)",
            xvline=ag.faixa_f_antena,
            title="Melhor Arranjo"
        )

        self.plotar(
            dados["s12"],
            x="Frequency (GHz)",
            y="S12 (dB)",
            xvline=ag.faixa_f_antena,
            title="Melhor Arranjo"
        )

        self.plotar(
            [
                dados["curva normalizada"],
                ag.curva_referencia_a,
                dados["diferenca ao quadrado"]
            ],
            x="Frequency (GHz)",
            y="A Normalizado",
            xvline=ag.faixa_f_antena,
            title="Normalizados",
            many=True
        )

        self.plotar(
            dados["zfssr"],
            x="Frequency (GHz)",
            y="Re{Z_RFSS} (Ohm)",
            xvline=ag.faixa_f_antena,
            title="Parte Real da Impedância da RFSS"
        )

        self.plotar(
            dados["zsubstrato"],
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
            x="Frequency (GHz)",
            y="I{ZFSS} e Zd (Ohm)",
            xvline=ag.faixa_f_antena,
            ylim=[-1000, 1000],
            title="Ressonância e Salisbury",
            many=True
        )

        self.plotar(
            [
                dados["zrr"],
                dados["zri"]
            ],
            x="Frequency (GHz)",
            y="Zr (Ohm)",
            xvline=ag.faixa_f_antena,
            title="Impedância RFSS + Substrato (Real e Imaginária)",
            many=True
        )
            