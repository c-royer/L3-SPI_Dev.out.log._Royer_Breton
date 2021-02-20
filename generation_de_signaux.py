import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd

Fs = 44100
t = np.arange(0, 2*np.pi, 1/Fs)


def sinus(freq):
    f = np.sin(2*np.pi* freq * t)
    return f

def plot(f):
    plt.figure()
    plt.plot(t, f)
    plt.show()


wavfile.write("test_sinus.wav", 22050, sinus(5000))
sd.play(sinus(5000), samplerate = 22050)
