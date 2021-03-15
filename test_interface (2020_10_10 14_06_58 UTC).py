#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import argparse
import queue
import sys
import wave

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from scipy.fftpack import fft , ifft
import soundfile as sf
from matplotlib.widgets import CheckButtons


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'channels', type=int, default=[1,2], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=10, metavar='N',
    help='display every Nth sample (default: %(default)s)')
parser.add_argument(
    '-m', '--downsample_dft', type=int, default=1, metavar='N',
    help='display every Nth sample (default: %(default)s)')
args = parser.parse_args(remaining)
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
q = queue.Queue()
q_dft = queue.Queue()
q_FRF = queue.Queue()


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::args.downsample, mapping])
    q_dft.put(indata[::args.downsample_dft, mapping])
    q_FRF.put(indata[::args.downsample_dft, mapping])





def update_plot(frame):
    """This is called by matplotlib for each plot update.

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

def update_FRF(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotFRF
    while True:
        try:
            data = q_FRF.get_nowait()
        except queue.Empty:
            break
        data = data[:,0]#/data[:,1]
        shift = len(data)
        plotFRF[-shift:, 0] = data
    for column, linee in enumerate(lines2):
        linee.set_ydata(plotFRF[:, column])
    return lines2

def update_dft(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdft
    while True:
        try:
            data = q_dft.get_nowait()
        except queue.Empty:
            break
        NDFT = int(args.samplerate)
        data = data
        data = fft(data[:,0], NDFT)
        #plotdft = np.roll(plotdft, -shift, axis=0)
        plotdft[:int(args.samplerate),0] = np.abs(data)
    for column, lin in enumerate(line):
        lin.set_ydata(plotdft[:, column])
    return line


try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']

    length = int(args.window * args.samplerate / (1000 * args.downsample))
    plotdata = np.zeros((length, len(args.channels)))

    length_FRF = 512
    plotFRF = np.zeros((length_FRF, len(args.channels)))

    #sensitivity = float(input('Sensibilité = '))

    length_dft = int(args.samplerate)
    plotdft = np.zeros((length_dft, len(args.channels)))

    fig, ax = plt.subplots(2,1)
    lines = ax[0].plot(plotdata, color = 'gold')
    line = ax[1].plot(plotdft, color = 'gold')
    #lines2 = ax[2].plot(plotFRF, color = 'gold')
    #if len(args.channels) > 1:
     #   ax.legend(['channel {}'.format(c) for c in args.channels],
      #            loc='lower left', ncol=len(args.channels))

    ax[0].axis((0, len(plotdata), -1, 1))
    ax[0].set_facecolor('mediumblue')
    #ax.set_yticks([0])
    ax[0].yaxis.grid(True)
    ax[0].tick_params(bottom=False, top=False, labelbottom=False,right=False, left=True, labelleft=True)
    ax[1].axis((0, len(plotdft)/2,0,150))
    ax[1].yaxis.grid(True)
    ax[1].set_facecolor('mediumblue')
    ax[0].set_title('Temporal analysis')
    ax[1].set_title('Frequency analysis')
   # ax[2].axis((0, len(plotFRF),0,1.5))
    #ax[2].set_facecolor('mediumblue')
    fig.tight_layout()
    
    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)
    anim = FuncAnimation(fig, update_dft, interval=args.interval, blit=True)
    #anim2 = FuncAnimation(fig, update_FRF, interval=args.interval, blit=True)
    with stream:
        plt.show()
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))