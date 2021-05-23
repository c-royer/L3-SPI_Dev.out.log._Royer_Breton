import argparse
import queue
import sys
import wave

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from scipy.fftpack import fft, ifft
import color

plt.close('all')

channels = [1]  # chois du channel à plot (default: the first)
device = None  # périphérique d'entrée (ID numérique ou script)
window = 200  # durée visible (default: %(default)s ms)
interval = 30  # interval minimum entre 2 update (default: %(default)s ms)
blocksize = 1  # block size (in samples)
samplerate = None  # fréquence d'échantillonage du périphérique audio
downsample = 10  # display every Nth sample (default: %(default)s)
downsample_dft = 1  # display every Nth sample (default: %(default)s)

if any(c < 1 for c in channels):
    print('argument CHANNEL: must be >= 1')

mapping = [c - 1 for c in channels]  # Channel numbers start with 1
q = queue.Queue()
q_dft = queue.Queue()

def audio_callback(indata, frames, time, status):
    """Fonction, nécessaire au stream, appellé pour chaque bloc audio"""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::downsample, mapping])
    q_dft.put(indata[::downsample_dft, mapping])


def update_plot(frame):
    """Fonction permettant la mise à jour de l'affichage matplotlib de la source microphonique
    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.
    """
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines


def update_dft(frame):
    """Fonction permettant la mise à jour de l'affichage matplotlib de la DFT
    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.
    """
    global plotdft
    while True:
        try:
            data = q_dft.get_nowait()
        except queue.Empty:
            break
        NDFT = int(samplerate)
        data = data
        data = fft(data[:, 0], NDFT)
        plotdft[:int(samplerate), 0] = np.abs(data)
    for column, lin in enumerate(line):
        lin.set_ydata(plotdft[:, column])
    return line


try:
    if samplerate is None:
        device_info = sd.query_devices(device, 'input')
        samplerate = device_info['default_samplerate']

    length = int(window * samplerate / (1000 * downsample))
    plotdata = np.zeros((length, len(channels)))

    # sensitivity = float(input('Sensibilité = '))

    length_dft = int(samplerate)
    plotdft = np.zeros((length_dft, len(channels)))


    with plt.rc_context(
            {'axes.edgecolor': 'white', 'xtick.color': 'white', 'ytick.color': 'white', 'figure.facecolor': 'white'}):

        fig, (ax1, ax2) = plt.subplots(2, figsize=(17, 8.2))
        lines = ax1.plot(plotdata, color=color.sea[0], lw = 1.1)
        line = ax2.semilogy(plotdft, color=color.darkorchid[0], lw = 1.1)
        fig.patch.set_facecolor('k')

        ax1.set_facecolor('k')
        ax1.axis((0, len(plotdata), -2, 2))
        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)


        ax1.grid(True, color='white', alpha=0.25)
        ax1.tick_params(bottom=False, top=False, labelbottom=False, right=False, left=True, labelleft=True)
        ax1.set_title('WAVEFORM', color = 'white')
        ax1.set_ylabel('Amplitude', color = 'white')


        ax2.set_facecolor('k')
        ax2.spines['right'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax2.set_ylabel('Amplitude', color = 'white')
        ax2.set_xlabel('Frequency (Hz)', color = 'white')
        ax2.axis((0, len(plotdft) / 2, 1E-3, 150))
        ax2.grid(True, color = 'white', alpha  = 0.25)

        ax2.set_title('SPECTRUM', color = 'white')


    plt.tight_layout()


    stream = sd.InputStream(
        device=device, channels=max(channels),
        samplerate=samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=interval, blit=True)
    anim = FuncAnimation(fig, update_dft, interval=interval, blit=True)

    with stream:
        plt.show()
        
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))

