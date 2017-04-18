from PySide import QtGui, QtCore
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends import qt_compat

from scalable_mw import Ui_MainWindow
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide.QtCore import *
    from PySide.QtGui import *

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):

        """
        Initializes the main window of the program
        :param version: String to use in the window header indicating the program version
        """



        super(MainWindow, self).__init__()

        self.setupUi(self)


        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.x_data = []
        self.y_data = []
        self.x_fit_data = []
        self.y_fit_data = []
        self.prev_x_fit = []
        self.prev_y_fit = []

        self.ax.tick_params(axis='both', which='major', labelsize=14)
        self.ax.set_xlabel('2 $\\theta$ / Degrees', fontsize=14)
        self.ax.set_ylabel(r'Intensity / a.u.', fontsize=14)
        self.ax.grid(True)

        self.addmpl(self.fig)

        self.showMaximized()

    def addmpl(self, fig):
        """
        Add a Matplotlib object to the plot

        :param fig:
        :return:
        """


        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        self.mplvl.addWidget(self.mpl_toolbar)



        self.plot_buttons_layout = QtGui.QHBoxLayout()
        self.plot_pattern_button = QtGui.QPushButton(self)
        self.plot_pattern_button.setText("Pattern + Last Fit")
        self.plot_pattern_button.setToolTip("Plots the currently loaded pattern and the last fit result.")

        self.plot_difference_button = QtGui.QPushButton(self)
        self.plot_difference_button.setText("Last Fit Difference")
        self.plot_difference_button.setToolTip("Plots the difference between source and fit data for the last fit result.")

        self.lock_y_axis = QtGui.QCheckBox(self)
        self.lock_y_axis.setText("Lock Pattern/Fit Y-Axis")
        self.lock_y_axis.setToolTip("Locks the Y-Axis during pattern/fit plotting.")

        self.lock_x_axis = QtGui.QCheckBox(self)
        self.lock_x_axis.setText("Lock Pattern/Fit X-Axis")
        self.lock_x_axis.setToolTip("Locks the X-Axis during pattern/fit plotting.")

        self.show_previous = QtGui.QCheckBox(self)
        self.show_previous.setText("Show Previous Fit")
        self.show_previous.setToolTip("Shows the Previous Iteration's Fit Result")

        self.plot_buttons_layout.addWidget(self.plot_pattern_button)
        self.plot_buttons_layout.addWidget(self.plot_difference_button)

        self.plot_buttons_layout.addWidget(self.lock_y_axis)
        self.plot_buttons_layout.addWidget(self.lock_x_axis)
        self.plot_buttons_layout.addWidget(self.show_previous)



        self.mplvl.addLayout(self.plot_buttons_layout)

def main():

    version = "1.2.1"

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
