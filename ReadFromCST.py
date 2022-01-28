import numpy as np
from Plots import Plots


class ReadFromCST:

    @staticmethod
    def s_cascade(x, y):

        denominador = (1 - x[3] * y[0])

        s11 = x[0] + (x[2] * x[1] * y[0]) / denominador
        s12 = (x[1] * y[1]) / denominador
        s21 = (x[2] * y[2]) / denominador
        s22 = y[3] + (y[2] * y[1] * x[3]) / denominador

        result = np.array([s11, s12, s21, s22])

        return result
    
    def plotar_S(self):  

        file_s11d = np.loadtxt('ExportsZ/s11D.txt')
        file_s12d = np.loadtxt('ExportsZ/s12D.txt')
        file_s21d = np.loadtxt('ExportsZ/s21D.txt')
        file_s22d = np.loadtxt('ExportsZ/s22D.txt')
        file_s11p = np.loadtxt('ExportsZ/s11P.txt')
        file_s12p = np.loadtxt('ExportsZ/s12P.txt')
        file_s21p = np.loadtxt('ExportsZ/s21P.txt')
        file_s22p = np.loadtxt('ExportsZ/s22P.txt')
        file_s11r = np.loadtxt('ExportsZ/s11R.txt')
        file_s12r = np.loadtxt('ExportsZ/s12R.txt')
        file_s21r = np.loadtxt('ExportsZ/s21R.txt')
        file_s22r = np.loadtxt('ExportsZ/s22R.txt')

        s11D = (file_s11d[:,1]+1j*file_s11d[:,2])
        s12D = (file_s12d[:,1]+1j*file_s12d[:,2])
        s21D = (file_s21d[:,1]+1j*file_s21d[:,2])
        s22D = (file_s22d[:,1]+1j*file_s22d[:,2])

        s11P = (file_s11p[:,1]+1j*file_s11p[:,2])
        s12P = (file_s12p[:,1]+1j*file_s12p[:,2])
        s21P = (file_s21p[:,1]+1j*file_s21p[:,2])
        s22P = (file_s22p[:,1]+1j*file_s22p[:,2])

        s11R = file_s11r[:,1]+1j*file_s11r[:,2]
        s12R = file_s12r[:,1]+1j*file_s12r[:,2]
        s21R = file_s21r[:,1]+1j*file_s21r[:,2]
        s22R = file_s22r[:,1]+1j*file_s22r[:,2]

        dielectric_s = np.array([s11D,s12D,s21D,s22D])
        pass_band_s = np.array([s11P,s12P,s21P,s22P])
        resistive_s = np.array([s11R,s12R,s21R,s22R])

        pass_band_s = pass_band_s / pass_band_s
        pass_band_s[1] = np.zeros(len(pass_band_s[1]))
        pass_band_s[2] = 9999999*np.zeros(len(pass_band_s[1]))
        cascade = np.ones(len(resistive_s))*0.5
        cascade = [cascade, cascade, cascade, cascade]
        cascade = self.s_cascade(cascade, cascade)
        #cascade = self.s_cascade(abs(resistive_s) ** 2, abs(dielectric_s) ** 2)
        #cascade = self.s_cascade(abs(cascade) ** 2, abs(pass_band_s) ** 2)

        #cascade = self.s_cascade(abs(pass_band_s), abs(dielectric_s))
        #cascade = self.s_cascade(abs(cascade), abs(resistive_s))
        
        rdb = 10 * np.log10(cascade[0])
        tdb = 10 * np.log10(cascade[1])
        adb = -10 * np.log10(cascade[0] + abs(cascade[1]))

        show = Plots(linspace=np.linspace(1, 25, len(rdb)))

        show.plotar(rdb,
                    x="Frequency (GHz)",
                    y="S11(dB)",
                    title="S11"
                    )
        
        show.plotar(tdb,
                    x="Frequency (GHz)",
                    y="S12(dB)",
                    title="S12"
                    )
        
        show.plotar(adb,
                    x="Frequency (GHz)",
                    y="A(dB)",
                    title="A"
                    )


from_cst = ReadFromCST()
from_cst.plotar_S()
