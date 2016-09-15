import sys
from PySide import QtGui, QtCore
from ui_mainWindow import Ui_MainWindow

import sys

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends import qt4_compat

import seaborn as sns
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE

if use_pyside:
    from PySide.QtCore import *
    from PySide.QtGui import *
else:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):

        sns.set_style('whitegrid')

        super(MainWindow, self).__init__()

        self.setupUi(self)
        self.assignWidgets()

        self.parameter_list = [
            self.param_0,
            self.param_1,
            self.param_2,
            self.param_3,
            self.param_4,
            self.param_5,
            self.param_6,
            self.param_7,
            self.param_8,
            self.param_9,
            self.param_10,
            self.param_11,
            self.param_12,
            self.param_13,
            self.param_14,
            self.param_15,
            self.param_16,
            self.param_17,
        ]

        self.parameter_enable_list = [
            self.param_enable_0,
            self.param_enable_1,
            self.param_enable_2,
            self.param_enable_3,
            self.param_enable_4,
            self.param_enable_5,
            self.param_enable_6,
            self.param_enable_7,
            self.param_enable_8,
            self.param_enable_9,
            self.param_enable_10,
            self.param_enable_11,
            self.param_enable_12,
            self.param_enable_13,
            self.param_enable_14,
            self.param_enable_15,
            self.param_enable_16,
            self.param_enable_17,
        ]

        self.init_ui_elements()

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.x_data = None
        self.y_data = None

        self.addmpl(self.fig)

        self.show()


    def init_ui_elements(self):

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Crtl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.close)
        self.menuFile.addAction(exitAction)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)


    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()


    def assignWidgets(self):

        # self.import_data.clicked.connect(self.load_parameters)
        self.menu_open_xrd_pattern.triggered.connect(self.open_pattern)
        self.menu_import_carboninp.triggered.connect(self.import_from_carboninp)

    def open_pattern(self):


        fname, _= QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.')
        input_file = open(fname, 'r')

        plot_data = np.loadtxt(input_file, delimiter='\t')

        self.x_data = plot_data[:,0]
        self.y_data = plot_data[:,1]

        self.theta_min_value.setValue(np.min(self.x_data))
        self.theta_max_value.setValue(np.max(self.x_data))


        self.fig.delaxes(self.ax)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.x_data, self.y_data)

        self.canvas.draw()

    def import_from_carboninp(self):

        fname, _= QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.')

        config_file = open(fname, 'r')

        for index, line in enumerate(config_file.readlines()[6:]):
            config_elements = line.split()

            param_value = float(config_elements[0])

            if config_elements[1] == '1':
                param_enable = True
            else:
                param_enable = False

            self.parameter_list[index].setValue(param_value)
            self.parameter_enable_list[index].setChecked(param_enable)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
