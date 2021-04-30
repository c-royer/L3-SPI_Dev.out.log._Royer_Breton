import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import pandas as pd
import sounddevice as sd
from scipy import signal
from scipy.fftpack import fft, fftfreq
#from UliEngineering.SignalProcessing.Simulation import square_wave, sawtooth, triangle_wave


Fs = 44100



def sinus(freq, duration, i):

    time = np.arange(0, duration, 1/(Fs))
    noise = 0.01*np.random.randn(len(time))

    function = np.sin(2*np.pi* freq * time + i) + noise


    return time, function

def multiple_sinus(freq, duration, i):

    Fs = 44100
    time = np.arange(0, duration, 1/(Fs))
    noise = 0.05 * np.random.randn(len(time))


    function_1 = 1*np.sin(2*np.pi* freq * time + i ) + noise
    function_2 = 1.2*np.sin(2 * np.pi * (freq*6/5) * time + i )
    function_3 =  1.3*np.sin(2 * np.pi * (freq * 3 / 2) * time + i)
    function_4 = 2*np.sin(2 * np.pi * (freq * 2) * time + i + np.pi )
    function_5 = np.sin(2 * np.pi * (freq * 3) * time + i)
    function_7 = np.sin(2 * np.pi * (freq * 9/2) * time + i)


    function_final = function_1 + function_2 + function_3 + function_4 + function_5# + function_7

    return time, function_final



def chirp(Fmin, Fmax, duration, number, i):
    Fs = 44100
    time = np.arange(0, duration, 1 / Fs)
    w = signal.chirp(time + i , f0=Fmin, f1=Fmax, t1=duration, method='linear')
    for k in range(1, number):
        w = np.concatenate([w, w])

        time = np.concatenate([time+duration, time])

    return time, w








    return tf, wf


def tone_bursts(F0,A0,duration, i):

    Fs = 44100
    time = np.arange(0, duration, 1/Fs)
    phi0 = 2*np.pi*np.random.rand(1)
    sigma_t = 0.05/6
    tc = 3*sigma_t

    # signal, window and windowed signal
    x = A0*np.cos(2*np.pi*F0*time+phi0+i)

    w = np.exp(-(time-tc)**2/(2*sigma_t**2))
    x = np.tile(x, 3)
    w = np.tile(w, 3)
    xw = x*w
    t = np.arange(len(xw))/Fs
    return t, xw


def sawtooth(freq,  duration, i):

        Fs = 44100
        time = np.arange(0, duration, 1/Fs)

        noise = 0.02 * np.random.randn(len(time))

        f = signal.sawtooth(2 * np.pi * freq * time + i) + noise
        f1 = signal.sawtooth(2 * np.pi * freq * time)
        return time, f


def multiple_sawtooth(freq, duration, i):
    Fs = 44100

    time = np.arange(0, duration, 1 / Fs)

    noise = 0.02 * np.random.randn(len(time))

    function_1 = signal.sawtooth(2 * np.pi * freq * time + i) * noise
    function_2 = signal.sawtooth(2 * np.pi * (freq*6/5)* time + i)
    function_3 = signal.sawtooth(2 * np.pi * (freq*3/2) * time+ i)
    function_4 = signal.sawtooth(2 * np.pi * freq *3* time + i)
    function_5 = signal.sawtooth(2 * np.pi * (freq * 9/2) * time + i)
    function_final = function_1 + function_2 + function_3
    return time, function_final, Fs

def triangle(freq, duration, i):
    Fs = 44100
    time = np.arange(0, duration, 1 / Fs)
    noise = 0.0 * np.random.randn(len(time))

    f = signal.sawtooth(2 * np.pi * freq * time + i, 0.5) + noise
    f1 = signal.sawtooth(2 * np.pi * freq * time, 0.5) + noise
    return time, f



def multiple_triangle(freq, duration, i):
    Fs = 44100

    time = np.arange(0, duration, 1 / Fs)
    noise = 0.01 * np.random.randn(len(time))

    f = signal.sawtooth(2 * np.pi * freq * time + i , 0.5) + noise
    f1 = signal.sawtooth(2 * np.pi * (freq*6/5) * time + i, 0.5)
    f2 = signal.sawtooth(2 * np.pi * (freq*3/2) * time + i, 0.5)
    f3 = signal.sawtooth(2 * np.pi * (freq *2) * time + i, 0.5)
    f4 = signal.sawtooth(2 * np.pi * (freq * 3) * time + i, 0.5)
    f5 = signal.sawtooth(2 * np.pi * (freq * 9/2) * time + i, 0.5)
    #f1 = signal.sawtooth(2 * np.pi * freq * time, 0.5) + noise
    f_final = f + f1 + f2# + f3 + f4 + f5
    return time, f_final, f

def square(freq, duration, i):

    Fs = 44100

    time = np.arange(0, duration, 1/Fs)
    noise = 0.0 * np.random.randn(len(time))

    function = signal.square(2 * np.pi * freq * time  + i) +  noise

    return time, function

def Gibbs(freq, duration, number_of_sin, i):

    Fs = 44100

    time = np.arange(0, duration, 1/Fs)

    noise = 0.01 * np.random.randn(len(time))

    function = 0
    for k in range(1, number_of_sin):
        function = function + ((np.sin(2*np.pi*((2*k)-1)*freq*time+i))/((2*k)-1))
        function1 = (4/np.pi)*function

    #function=+ noise

    return time, function1

def multiple_square(freq, duration,i):
    Fs = 44100

    time = np.arange(0, duration, 1/Fs)
    noise = 0.03 * np.random.randn(len(time))

    f = 1*signal.square(2 * np.pi * freq * time  + i) +noise
    f1 = 1.2*signal.square(2 * np.pi * (freq*6/5) * time + i )
    f2 = 0.8* signal.square(2 * np.pi * (freq*3/2) * time + i)
    f3 = signal.square(2 * np.pi * freq * 2* time + i)
    f4 = signal.square(2 * np.pi * freq *3* time + i)
    f5 = signal.square(2 * np.pi * (freq*9/2) * time + i)
    f_final = f + f1# + f2 ##f3 + f4 + f5
    return time, f_final


def plot(sig):
    plt.figure()
    plt.plot(sig)
    plt.show()

def white_noise(N):
    wgn = np.random.randn(N)
    time = np.arange(N)/Fs
    return time, wgn, N



def FFT(y, Fs):
    Ntfd = len(y)
    fft_data = abs(fft(y, Ntfd))
    frequency = np.arange(Ntfd) * Fs / Ntfd
    return frequency, fft_data



if __name__ == "__main__":
    fig, ax = plt.subplots()

    time, sig= chirp(20, 1000, 1, 2, 0)
    print(sig)
    ax.plot(time, sig)#+0.02*np.random.randn(time.shape[0]))
    #ax.set_xlim(0, 44100/2)

    plt.show()
    print(max(sig))

    wavfile.write("sound/test_chirp.wav", 44100, sig.astype(np.float64))
    sd.play(chirp(20, 1000, 1, 2, 0)[1])
