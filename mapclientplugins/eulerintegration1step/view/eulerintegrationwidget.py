'''
Created on May 26, 2015

@author: andre
'''
from PySide2 import QtCore, QtWidgets

import numpy as np

import matplotlib

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler

from mapclientplugins.eulerintegration1step.view.ui_eulerintegrationwidget import Ui_EulerIntegrationWidget
from mapclientplugins.eulerintegration1step.sedml.execute import ExecuteSedml


class EulerIntegrationWidget(QtWidgets.QWidget):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(EulerIntegrationWidget, self).__init__(parent)
        self._ui = Ui_EulerIntegrationWidget()
        self._ui.setupUi(self)
        self.sedml = ExecuteSedml()
        # create the plot
        self.fig = Figure((5.0, 4.0), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self._ui.plotPane)
        self.canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.canvas.setFocus()
        self.mpl_toolbar = NavigationToolbar(self.canvas, self._ui.plotPane)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        vbox.addWidget(self.mpl_toolbar)
        self._ui.plotPane.setLayout(vbox)

        self.createAxes()
        self._makeConnections()

    def createAxes(self):
        self.axes = self.fig.add_subplot(111)
        self.drawSineFunction()
        self.axes.legend()
        self.canvas.draw()

    def _makeConnections(self):
        self._ui.doneButton.clicked.connect(self._doneButtonClicked)
        self._ui.simulateButton.clicked.connect(self._simulateButtonClicked)
        self._ui.clearButton.clicked.connect(self._clearButtonClicked)

    def setSimulationRoot(self, location):
        self.sedml.setSimulationRoot(location)

    def drawSineFunction(self):
        # draw sine function
        t = np.arange(0.0, 2.0 * np.pi, 0.01)
        s = np.sin(t)
        self.axes.plot(t, s, label="sin(t)")

    def on_key_press(self, event):
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.canvas, self.mpl_toolbar)

    def _simulateButtonClicked(self):
        h = self._ui.stepSizeSpinBox.value()
        n = self._ui.nSpinBox.value()
        data = self.sedml.execute(h, n)
        if data is None:
            return
        data1 = np.arange(20).reshape([4, 5]).copy()
        title = "h=" + str(h)
        self.axes.plot(data['X'], data['Derivative_approximation'], marker="o", label=title)
        self.axes.legend()
        self.canvas.draw()

    def _clearButtonClicked(self):
        self.fig.clear()
        self.createAxes()

    def initialise(self):
        print("Initialise called?")

    def registerDoneExecution(self, callback):
        self._callback = callback

    def _doneButtonClicked(self):
        self._callback()
