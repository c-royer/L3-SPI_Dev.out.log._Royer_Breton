# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:18:57 2020

@author: ninad
"""

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

Fs =44100
time = 1
N = int(time*Fs)
t = np.arange(N)/Fs

x = np.cos(2*np.pi*20*t)

#---------------------------------Hanning----------------------------------#

hann = signal.hann(len(x))
x_windowed = x*hann

plt.figure()
plt.plot(t,x,label='signal brut')
plt.plot(t,hann,'--',label='fenêtre')
plt.plot(t,x_windowed,label='signal fenêtré')
plt.legend()
plt.show()

#---------------------------------Hamming----------------------------------#

hamm = signal.hamming(len(x))
x_windowed = x*hamm

plt.figure()
plt.plot(t,x,label='signal brut')
plt.plot(t,hamm,'--',label='fenêtre')
plt.plot(t,x_windowed,'--',label='signal fenêtré')
plt.legend()
plt.show()

#---------------------------------Flat Top----------------------------------#

ft = signal.flattop(len(x))
x_windowed = x*ft

plt.figure()
plt.plot(t,x,label='signal brut')
plt.plot(t,ft,'--',label='fenêtre')
plt.plot(t,x_windowed,'--',label='signal fenêtré')
plt.legend()
plt.show()

#------------------------------Exponential----------------------------------#
M = len(x)
exp = signal.exponential(M, tau = 5000)
x_windowed = x*exp

plt.figure()
plt.plot(t,x,label='signal brut')
plt.plot(t,exp,'--',label='fenêtre')
plt.plot(t,x_windowed,label='signal fenêtré hamming')
plt.legend()
plt.show()
