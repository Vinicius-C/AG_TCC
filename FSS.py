import math


class FSS:
    # Velocidade da Luz
    vluz = 299792458
    # Impedância do Vácuo
    z0 = 376.73

    def __init__(self):
        pass

    def calculo_impedancia(self, frequencia, angulo_incidencia):
        pass

    @staticmethod
    def beta(w, p):
        return math.sin((math.pi * w) / (2 * p))

    # tipo = 1 e -1 para +/-

    @staticmethod
    def c(tipo, phi, _lambda, p):
        primeiro_termo = 2 * p * math.sin(phi) / _lambda
        segundo_termo = (p * math.cos(phi) / _lambda) ** 2
        try:
            1 / math.sqrt(1 + tipo * primeiro_termo - segundo_termo) - 1
        except:
            import ipdb; ipdb.set_trace()

        return 1 / math.sqrt(1 + tipo * primeiro_termo - segundo_termo) - 1

    def g(self, p, w, _lambda, phi):
        beta = self.beta(w, p)
        beta2 = beta ** 2
        # cp = c+ e cn = c-
        cp = self.c(1, phi, _lambda, p)
        cn = self.c(-1, phi, _lambda, p)
        termo = 1 - beta2 / 4
        numerador = 0.5 * (1 - beta2)**2 * (termo * (cp + cn) + 4 * beta2 * cp * cn)
        denominador = termo + beta2 * (1 + beta2 / 4 - (beta ** 4) / 8) * (cp + cn) + 2 * (beta ** 6) * cp * cn
        return numerador / denominador

    def f(self, p, w, _lambda, phi):
        primeiro_termo = p * math.cos(phi) / _lambda
        try:
            segundo_termo = math.log(1 / self.beta(w, p), math.e)
        except:
            import ipdb
            ipdb.set_trace()

        return primeiro_termo * (segundo_termo + self.g(p, w, _lambda, phi))
