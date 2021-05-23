from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
import sys
import random
import color

class Plot2D:
    def __init__(self):
        self.traces = dict()
        self.traces1 = dict()

        self.app = QtGui.QApplication([])

        self.win = pg.GraphicsWindow(title="Sound Analyser")
        self.win.showMaximized()
        self.win.setWindowTitle('Sound Analyser')
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'w')

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
                self.traces[name] = self.waveform.plot(pen=color.royalblue[1], width=2)
                self.waveform.setYRange(min(dataset_y) * 3/2, max(dataset_y) * 3/2, padding=0)
                self.waveform.setXRange(-2E-4, 10*1/freq, padding=0)
                self.waveform.showGrid(x=True, y=True, alpha=0.45)




            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen=color.pink[1], width=2)
                self.spectrum.setLogMode(x=False, y=True)
                self.spectrum.setXRange(-200, 22050, padding=0)
                self.spectrum.setYRange(np.log10(min(dataset_y) * (5/4)), np.log10(max(dataset_y *5/4)), padding=0)
                self.spectrum.showGrid(x=True, y=True, alpha=0.45)
