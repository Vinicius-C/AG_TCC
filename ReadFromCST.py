import math

import openpyxl
from pathlib import Path
import numpy as np
from AGUtil import AGUtil
from FSS import FSS
from Plots import Plots


class ReadFromCST:

    pass_band_s11 = pass_band_s12 = pass_band_s21 = pass_band_s22 = dieletric_s11 \
        = dieletric_s12 = dieletric_s21 = dieletric_s22 = resistive_fss_s11 \
        = resistive_fss_s12 = resistive_fss_s21 = resistive_fss_s22 = None

    # Usando Matriz ABCD
    '''
    def __init__(self) -> None:               
        self.ler_all_s()

    @staticmethod
    def ler_s_parameters(name):
        xlsx_file = Path('ExportsZ', name)

        wb_obj = openpyxl.load_workbook(xlsx_file)
        sheet = wb_obj.active
        data = [[], []]

        for i, row in enumerate(sheet.iter_rows(values_only=True)):
            if i < 3:
                continue

            data[0] = np.append(data[0], float(row[0]))
            # data[1] = np.append(data[1], math.sqrt(10 ** (float(row[1] / 10))))
            data[1] = np.append(data[1], complex(row[1] + 1j * row[2]))

        wb_obj.close()

        return data

    def ler_all_s(self):
        self.pass_band_s11 = self.ler_s_parameters('Pass_Band/s11.xlsx')[1]
        self.pass_band_s12 = self.ler_s_parameters('Pass_Band/s12.xlsx')[1]
        self.pass_band_s21 = self.ler_s_parameters('Pass_Band/s21.xlsx')[1]
        self.pass_band_s22 = self.ler_s_parameters('Pass_Band/s22.xlsx')[1]

        self.dieletric_s11 = self.ler_s_parameters('Dieletric/s11.xlsx')[1]
        self.dieletric_s12 = self.ler_s_parameters('Dieletric/s12.xlsx')[1]
        self.dieletric_s21 = self.ler_s_parameters('Dieletric/s21.xlsx')[1]
        self.dieletric_s22 = self.ler_s_parameters('Dieletric/s22.xlsx')[1]

        self.resistive_fss_s11 = self.ler_s_parameters('Resistive_FSS/s11.xlsx')[1]
        self.resistive_fss_s12 = self.ler_s_parameters('Resistive_FSS/s12.xlsx')[1]
        self.resistive_fss_s21 = self.ler_s_parameters('Resistive_FSS/s21.xlsx')[1]
        self.resistive_fss_s22 = self.ler_s_parameters('Resistive_FSS/s22.xlsx')[1]

    @staticmethod
    def get_a(s):
        import ipdb; ipdb.set_trace()
        s11, s12, s21, s22 = s[0].astype(complex), \
                             s[1].astype(complex), \
                             s[2].astype(complex), \
                             s[3].astype(complex)

        numerador = (1 + s11) * (1 - s22) + (s12 * s21)
        denominador = 2 * s21
        a = numerador / denominador
        return a

    @staticmethod
    def get_b(s):
        s11, s12, s21, s22 = s[0].astype(complex), \
                             s[1].astype(complex), \
                             s[2].astype(complex), \
                             s[3].astype(complex)

        z0 = FSS.z0

        numerador = (1 + s11) * (1 + s22) - (s12 * s21)
        denominador = 2 * s21
        b = z0 * numerador / denominador
        return b

    @staticmethod
    def get_c(s):
        s11, s12, s21, s22 = s[0].astype(complex), \
                             s[1].astype(complex), \
                             s[2].astype(complex), \
                             s[3].astype(complex)

        z0 = FSS.z0

        numerador = (1 - s11) * (1 - s22) - (s12 * s21)
        denominador = 2 * s21
        c = (1 / z0) * numerador / denominador
        return c

    @staticmethod
    def get_d(s):
        s11, s12, s21, s22 = s[0].astype(complex), \
                             s[1].astype(complex), \
                             s[2].astype(complex), \
                             s[3].astype(complex)

        numerador = (1 - s11) * (1 + s22) + (s12 * s21)
        denominador = 2 * s21
        d = numerador / denominador
        return d

    def s_to_abcd(self, s):
        a = self.get_a(s)
        b = self.get_b(s)
        c = self.get_c(s)
        d = self.get_d(s)

        abcd = np.apply_along_axis(self.reshape_2,
                                   axis=1,
                                   arr=np.array([a, b, c, d]).transpose())
        return abcd
    
    @staticmethod
    def abcd_to_r_t(abcd):
        z0 = FSS.z0
        result = [None, None]

        for matrix in abcd:
            a = matrix[0][0]
            b = matrix[0][1]
            c = matrix[1][0]
            d = matrix[1][1]

            denominador = a + b / z0 + c * z0 + d

            s11 = (a + b / z0 - c * z0 - d) / denominador
            s12 = 2 * (a * d - b * c) / denominador

            result = np.vstack((result, [s11, s12]))

        return np.delete(result, 0, 0)
    '''

    @staticmethod
    def reshape_2(x):
        return x.reshape(2, -1)
        
    def reshape_s(self, s):
        return np.apply_along_axis(self.reshape_2,
                                   axis=1,
                                   arr=np.array(s).transpose())

    @staticmethod
    def s_cascade(x, y):
        result = []
        for i in range(len(x)):
            x11 = x[i][0][0] ** 2
            x12 = x[i][0][1] ** 2
            x21 = x[i][1][0] ** 2
            x22 = x[i][1][1] ** 2

            y11 = y[i][0][0] ** 2
            y12 = y[i][0][1] ** 2
            y21 = y[i][1][0] ** 2
            y22 = y[i][1][1] ** 2

            denominador = (1 - x22 * y11)

            s11 = x11 + (x21 * x12 * y11) / denominador
            s12 = (x12 * y12) / denominador
            s21 = (x21 * y21) / denominador
            s22 = y22 + (y21 * y12 * y22) / denominador

            result.append([[s11, s12], [s21, s22]])

        return result

    @staticmethod
    def dissociate(array):
        result1 = []
        result2 = []

        for elem in array:
            result1.append(elem[0])
            result2.append(elem[1])

        return [result1, result2]

    @staticmethod
    def sdb_to_s(s):
        return np.apply_along_axis(lambda x: math.sqrt(10 ** (x / 10)),
                                   axis=1,
                                   arr=s)
    '''
    def plotar_ABCD(self): 
        pass_band_abcd = self.s_to_abcd(np.array([self.pass_band_s11,
                                                  self.pass_band_s12,
                                                  self.pass_band_s21,
                                                  self.pass_band_s22]
                                                 )
                                        )
        dieletric_abcd = self.s_to_abcd(np.array([self.dieletric_s11,
                                                  self.dieletric_s12,
                                                  self.dieletric_s21,
                                                  self.dieletric_s22]
                                                 )
                                        )
        resistive_fss_abcd = self.s_to_abcd(np.array([self.resistive_fss_s11,
                                                      self.resistive_fss_s12,
                                                      self.resistive_fss_s21,
                                                      self.resistive_fss_s22]
                                                     )
                                            )

        # abcd_arranjo = np.matmul(pass_band_abcd, dieletric_abcd)
        # abcd_arranjo = np.matmul(abcd_arranjo, resistive_fss_abcd)

        abcd_arranjo = np.matmul(resistive_fss_abcd, dieletric_abcd)
        abcd_arranjo = np.matmul(abcd_arranjo, pass_band_abcd)

        r_t = self.abcd_to_r_t(abcd_arranjo).transpose()

        r2 = np.abs(r_t[0]) ** 2
        t2 = np.abs(r_t[1]) ** 2
        rdb = 10 * np.log10(r2.astype("float"))
        tdb = 10 * np.log10(t2.astype("float"))
        a = -10 * np.log10(r2.astype("float") + t2.astype("float"))

        dados = AGUtil.ler_config()
        faixa_f_antena = dados["FAIXA_ANTENA"]

        show = Plots(linspace=np.linspace(1, 25, len(r_t[1])))

        show.plotar(rdb,
                    x="Frequency (GHz)",
                    y="S11(dB)",
                    xvline=faixa_f_antena,
                    title="S"
                    )

        show.plotar(tdb,
                    x="Frequency (GHz)",
                    y="S12(dB)",
                    xvline=faixa_f_antena,
                    title="S"
                    )

        show.plotar(a,
                    x="Frequency (GHz)",
                    y="A(db)",
                    xvline=faixa_f_antena,
                    title="A"
                    )
    '''

    def plotar_S(self, s, tamanho):   
        #self.pass_band_s11 = self.pass_band_s12 = self.pass_band_s21 = self.pass_band_s22 =\
        #    self.dieletric_s11 = self.dieletric_s12 = self.dieletric_s21 = self.dieletric_s22 =\
        #    self.resistive_fss_s11 = self.resistive_fss_s12 = self.resistive_fss_s21 =\
        #    self.resistive_fss_s22 = s*np.ones(tamanho)

        pass_band_s = self.reshape_s([self.pass_band_s11,
                                      self.pass_band_s12,
                                      self.pass_band_s21,
                                      self.pass_band_s22]
                                     )
        dieletric_s = self.reshape_s([self.dieletric_s11,
                                      self.dieletric_s12,
                                      self.dieletric_s21,
                                      self.dieletric_s22]
                                     )
        resistive_s = self.reshape_s([self.resistive_fss_s11,
                                      self.resistive_fss_s12,
                                      self.resistive_fss_s21,
                                      self.resistive_fss_s22]
                                     )

        cascade = self.s_cascade(np.abs(resistive_s), np.abs(dieletric_s))
        cascade = self.s_cascade(np.abs(cascade), np.abs(pass_band_s))

        r_t = np.apply_along_axis(lambda x: x[0], 1, cascade)
        r_t = np.array(self.dissociate(r_t))

        r2 = r_t[0]
        t2 = r_t[1]
        
        rdb = 10 * np.log10(r2.astype("float"))
        tdb = 10 * np.log10(t2.astype("float"))
        a = -10 * np.log10(r2.astype("float") + t2.astype("float"))

        show = Plots(linspace=np.linspace(1, 25, len(r2)))

        show.plotar(rdb,
                    x="Frequency (GHz)",
                    y="S11(dB)",
                    title="S"
                    )
        
        show.plotar(tdb,
                    x="Frequency (GHz)",
                    y="S12(dB)",
                    title="S"
                    )
        
        show.plotar(a,
                    x="Frequency (GHz)",
                    y="A(dB)",
                    title="A"
                    )


from_cst = ReadFromCST()
#from_cst.plotar_ABCD()
from_cst.plotar_S(0.70710678118654752440084436210485, 100)
