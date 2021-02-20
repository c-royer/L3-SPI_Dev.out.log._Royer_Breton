import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd

Fs = 44100
t = np.arange(0, 2*np.pi, 1/Fs)


def sinus(freq):
    f = np.sin(2*np.pi* freq * t)
    return f

def chirp(Fmin, Fmax, T=2):
    N = int(T*Fs)
    tchirp = np.arange(N)/Fs
    alpha = Fmin
    beta = (Fmax - Fmin) / T
    phiLIN = 2 * np.pi * (alpha * tchirp + beta / 2 * tchirp ** 2) + 2 * np.pi * np.random.rand(1)
    zsLIN = np.exp(1j * phiLIN)
    sLIN = np.real(zsLIN)
    return sLIN


def tone_burst(F0, A0):
    N = Fs
    t_tone = np.arange(N) / Fs
    phi0 = 2*np.pi*np.random.rand(1)
    sigma_t = 0.05/6
    tc = 3*sigma_t
    x = A0*np.cos(2*np.pi*F0*t_tone+phi0)
    w = np.exp(-(t_tone-tc)**2/(2*sigma_t**2))
    xw = x*w
    return xw


def plot(xw):
    plt.figure()
    plt.plot(xw)
    plt.show()

#plot(tone_burst(1000, 0.2))

wavfile.write("test_chirp.wav", 44100, chirp(2500, 5000))
sd.play(chirp(2500, 5000), samplerate = 44100)
