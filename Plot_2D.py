from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import sys

class Plot2D:
    def __init__(self):
        self.traces = dict()
        self.traces1 = dict()

        self.app = QtGui.QApplication([])

        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.win.showMaximized()
        self.win.setWindowTitle('pyqtgraph example: Plotting')

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        self.waveform = self.win.addPlot(title='WAVEFORM', row=1, col=1, bottom='Time (s)', left = 'Amplitude')
        self.spectrum = self.win.addPlot(title='SPECTRUM', row=2, col=1, bottom = "Frequency (Hz)", left = 'Amplitude')

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def trace(self,name,dataset_x,dataset_y, freq):
        if name in self.traces:
            self.traces[name].setData(dataset_x,dataset_y)

        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(min(dataset_y) * 5/4, max(dataset_y) * 5/4, padding=0)
                self.waveform.setXRange(0, 10*1/freq, padding=0)
                self.waveform.showGrid(x=True, y=True, alpha=0.45)

            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='m', width=3)
                self.spectrum.setLogMode(x=False, y=True)
                self.spectrum.setXRange(0, 22050, padding=0)
                self.spectrum.setYRange(np.log10(min(dataset_y) * (5/4)), np.log10(max(dataset_y *5/4)), padding=0)
                self.spectrum.showGrid(x=True, y=True, alpha=0.45)
