from ReadFromCST import ReadFromCST
import numpy as np

class Teste(ReadFromCST):

    def __init__(self) -> None:
        super().__init__()

    def teste_s_to_abcd(self):
        s = np.array([
            np.array([0.6, 0.6]).astype("complex"),
            np.array([0.8, 0.8]).astype("complex"),
            np.array([0.8, 0.8]).astype("complex"),
            np.array([0.6, 0.6]).astype("complex")
        ])
        resultado = self.s_to_abcd(s)
        s_param = np.array([0.6, 0.8, 0.8, 0.6]).astype("complex")
        abcd_correta = np.array([
            [
                [Teste.get_a(s_param), Teste.get_b(s_param)],
                [Teste.get_c(s_param), Teste.get_d(s_param)]
            ],[
                [Teste.get_a(s_param), Teste.get_b(s_param)],
                [Teste.get_c(s_param), Teste.get_d(s_param)]
            ]
        ])

        print(resultado)
        print(abcd_correta)


teste = Teste()
teste.teste_s_to_abcd()
