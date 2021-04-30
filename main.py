import numpy as np
import sounddevice as sd
from signals_generator import *
from Plot_2D import *
from pyqtgraph.Qt import QtCore



if __name__ == '__main__':
    p = Plot2D()
    i = 0
    frequency = 500

    def update():

        global p, i

        t, s = sinus(500, 1, i ) # tu change la fonction ici, et aussi en dessous pour le .wav
        #certaine méthode ne sont pas au point comme le chirp et le tone burst, ici, la durée est de 1 seconde, et en dessous c'est 50.

        fft_freq, fft_data = FFT(s, 44100)



        p.trace("waveform", t, s, frequency)
        p.trace("spectrum", fft_freq, fft_data, frequency)
        i += 0.4




    sd.play(sinus(354, 50, i )[1], samplerate = 44100)
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(25)

    p.start()




