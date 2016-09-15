import sys
from PySide import QtGui, QtCore
from ui_mainWindow import Ui_MainWindow
import ujson
import sys
import os
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends import qt_compat

import seaborn as sns
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE

if use_pyside:
    from PySide.QtCore import *
    from PySide.QtGui import *
else:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

class ConsoleStream(QtCore.QObject):

    message = QtCore.Signal(str)
    def __init__(self, parent=None):
        super(ConsoleStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))


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

        self.parameter_labels = [
            self.param_label_0.text(),
            self.param_label_1.text(),
            self.param_label_2.text(),
            self.param_label_3.text(),
            self.param_label_4.text(),
            self.param_label_5.text(),
            self.param_label_6.text(),
            self.param_label_7.text(),
            self.param_label_8.text(),
            self.param_label_9.text(),
            self.param_label_10.text(),
            self.param_label_11.text(),
            self.param_label_12.text(),
            self.param_label_13.text(),
            self.param_label_14.text(),
            self.param_label_15.text(),
            self.param_label_16.text(),
            self.param_label_17.text(),
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

        self.num_params = len(self.parameter_list)

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


    @QtCore.Slot(str)
    def on_stream_message(self, message):
        self.console.moveCursor(QtGui.QTextCursor.End)
        self.console.insertPlainText(message)

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.mplwindow)
        self.mplvl.addWidget(self.mpl_toolbar)



    def assignWidgets(self):

        # self.import_data.clicked.connect(self.load_parameters)
        self.menu_open_xrd_pattern.triggered.connect(self.open_pattern)
        self.menu_import_carboninp.triggered.connect(self.import_from_carboninp)
        self.menu_import_diffsettings.triggered.connect(self.import_diffractometer_params)
        self.menu_import_fittingparams.triggered.connect(self.import_fitting_params)

        # Export Data
        self.menu_export_diffsettings.triggered.connect(self.export_diffractometer_params)
        self.menu_export_fittingparams.triggered.connect(self.export_fitting_params)

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

    def export_diffractometer_params(self):

        fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export File', os.path.join('config', 'diffractometer settings'), filter="*.json")

        if fname:

            data_file = open(fname, 'w')

            diffractometer_settings = {"wavelength":self.wavelength.value(),
                                       "beam_width":self.beam_width.value(),
                                       "sample_width":self.sample_width.value(),
                                       "sample_depth":self.sample_depth.value(),
                                       "sample_density":self.sample_density.value(),
                                       "gonio_radius":self.goniometer_radius.value(),


                                       }


            ujson.dump(diffractometer_settings, data_file, indent = 4)

            print 'Exported Diffractometer Settings to: %s'%fname
            self.statusBar.showMessage('Exported Diffractometer Settings to: %s'%fname)



    def import_diffractometer_params(self):

        fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Export File', os.path.join('config','diffractometer settings'), filter="*.json")

        if fname:

            data_file = open(fname, 'r')

            diffractometer_settings = ujson.load(data_file)

            self.wavelength.setValue(diffractometer_settings['wavelength'])
            self.beam_width.setValue(diffractometer_settings['beam_width'])
            self.sample_width.setValue(diffractometer_settings['sample_width'])
            self.sample_depth.setValue(diffractometer_settings['sample_depth'])
            self.sample_density.setValue(diffractometer_settings['sample_density'])
            self.goniometer_radius.setValue(diffractometer_settings['gonio_radius'])

            print 'Imported Diffractometer Settings from: %s'%fname

            self.statusBar.showMessage('Imported Diffractometer Settings from: %s'%fname)


    def export_fitting_params(self):

        fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export File', os.path.join('config', 'fitting parameters'), filter="*.json")

        if fname:

            data_file = open(fname, 'w')

            fitting_params = {}

            for index, label in enumerate(self.parameter_labels):

                fitting_params[label] = (self.parameter_list[index].value(), self.parameter_enable_list[index].isChecked())

            ujson.dump(fitting_params, data_file, indent = 4)

            print 'Exported Fitting Parameters to: %s'%fname
            self.statusBar.showMessage('Exported Fitting Parameters to: %s'%fname)

    def import_fitting_params(self):

        fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Export File', os.path.join('config','fitting parameters'), filter="*.json")

        if fname:

            data_file = open(fname, 'r')

            fitting_params = ujson.load(data_file)

            for index, label in enumerate(self.parameter_labels):

                param_value, enabled = fitting_params[label]

                self.parameter_list[index].setValue(param_value)
                self.parameter_enable_list[index].setChecked(enabled)

            print 'Imported Fitting Parameters from: %s'%fname
            self.statusBar.showMessage('Imported Fitting Parameters from: %s'%fname)




    def import_from_carboninp(self):

        fname, _= QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.', filter='CARBON.INP')

        if fname:

            config_file = open(fname, 'r')

            data_lines = config_file.readlines()

            # Thetamin, theta max, wavelength, nskip
            data_elements_1 = data_lines[1].split()

            self.theta_min_value.setValue(float(data_elements_1[0]))
            self.theta_max_value.setValue(float(data_elements_1[1]))
            self.wavelength.setValue(float(data_elements_1[2]))
            self.nskip.setValue(int(data_elements_1[3]))

            # TODO: Add readin for fitting parameters Npar, Nphi, Nsg, Nlayer
            data_elements_2 = data_lines[2].split()

            self.n_phi.setValue(float(data_elements_2[1]))
            self.n_sg.setValue(float(data_elements_2[2]))

            if int(data_elements_2[3]) == 1:
                self.number_layers.setCurrentIndex(0)
            elif int(data_elements_2[3]) == 2:
                self.number_layers.setCurrentIndex(1)
            else:
                print "Number of layers is not 1 or 2. Setting to 1"
                self.number_layers.setCurrentIndex(0)

            # Diffractometer Parameters
            data_elements_3 = data_lines[3].split()
            self.sample_density.setValue(float(data_elements_3[0]))
            self.goniometer_radius.setValue(float(data_elements_3[1]))
            self.sample_depth.setValue(float(data_elements_3[2]))
            self.sample_width.setValue(float(data_elements_3[3]))
            self.beam_width.setValue(float(data_elements_3[4]))


            data_elements_4 = data_lines[4].split()

            self.iterations.setValue(int(data_elements_4[0]))
            self.epsilon.setValue(float(data_elements_4[1]))

            data_elements_5 = data_lines[5].split()
            if int(data_elements_5[0]):
                # Enable Gradient Checking
                self.number_layers.setCurrentIndex(1)
            else:
                # Disable Gradient Checking
                self.number_layers.setCurrentIndex(1)


            self.gradient_check_delta.setValue(float(data_elements_5[1]))



            for index, line in enumerate(data_lines[6:]):
                config_elements = line.split()

                param_value = float(config_elements[0])

                if config_elements[1] == '1':
                    param_enable = True
                else:
                    param_enable = False

                self.parameter_list[index].setValue(param_value)
                self.parameter_enable_list[index].setChecked(param_enable)


            print 'Imported CARBON.INP parameters from: %s' % fname
            self.statusBar.showMessage('Imported CARBON.INP parameters from: %s' % fname)

def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()

    console_stream = ConsoleStream()
    console_stream.message.connect(ex.on_stream_message)

    sys.stdout = console_stream
    sys.stderr = console_stream

    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
