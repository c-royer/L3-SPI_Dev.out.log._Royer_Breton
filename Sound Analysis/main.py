import numpy as np
import sounddevice as sd
from signals_generator import *
from interface import *
from pyqtgraph.Qt import QtCore


if __name__ == '__main__':

    print('-' * 30)
    print("Select a method (Signal / Microphone) ? [s/m]")
    print('-' * 30)

    method = input()

    if method == 's':

        p = Plot2D()
        i = 0
        frequency = 500  # allows to change the frequency of the signal

        def update():

            global p, i

            method_plot = square(frequency, 1.5, 35, i)  # allows to choose the desired signal. To know all the parameters you had to use, please refer to the "signals_generator" program.
            t, s =  method_plot                          # please, let the duration on 1 seconds.

            fft_freq, fft_data = FFT(s, 44100)

            p.trace("waveform", t, s, frequency)
            p.trace("spectrum", fft_freq, fft_data, frequency)
            i += 0.4


        print('-'*30)
        print("Play the sound? [o/n] ")
        print('-' * 30)
        input = input()

        if input == 'o' :

            method_play = square(frequency, 1.5, 35, i, 50) #allows to play the signal. Put a duration of 50 seconds except for the white noise where it's necessary to put
            # a number of point of 2 000 000.

            sd.play(method_play[1], samplerate = 44100)


        timer = QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(25)

        p.start()

    else:
        import microphone






