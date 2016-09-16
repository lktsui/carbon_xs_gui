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

import csv

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

        # Fitting Process
        self.fitting_process = QtCore.QProcess(self)
        self.fitting_process.readyRead.connect(self.on_process_message)
        self.fitting_process.finished.connect(self.fitting_finished)
        self.abort_flag = False

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
        self.console.moveCursor(QtGui.QTextCursor.End)

    def on_process_message(self):
        self.console.moveCursor(QtGui.QTextCursor.End)
        self.console.insertPlainText(str(self.fitting_process.readAll()))
        self.console.moveCursor(QtGui.QTextCursor.End)


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
        self.menu_import_fittingsettings.triggered.connect(self.import_fitting_settings)

        # Export Data
        self.menu_export_carboninp.triggered.connect(self.export_to_carboninp)
        self.menu_export_diffsettings.triggered.connect(self.export_diffractometer_params)
        self.menu_export_fittingparams.triggered.connect(self.export_fitting_params)
        self.menu_export_fittingsettings.triggered.connect(self.export_fitting_settings)

        # Fitting Process Options
        self.menu_start_fit.triggered.connect(self.start_fitting_process)
        self.menu_abort_fit.triggered.connect(self.abort_fit_process)


    def open_pattern(self):

        fname, _= QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.')


        input_file = open(fname, 'r')

        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(input_file.readline())
        plot_data = np.loadtxt(input_file, delimiter=dialect.delimiter)

        self.x_data = plot_data[:,0]
        self.y_data = plot_data[:,1]

        self.theta_min_value.setValue(np.min(self.x_data))
        self.theta_max_value.setValue(np.max(self.x_data))

        self.fig.delaxes(self.ax)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.x_data, self.y_data)

        self.canvas.draw()

    def plot_fit_results(self):

        filename = os.path.join('carbonxs', 'carbon.dat')
        plot_file = open(filename, 'r')
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(plot_file.readline())

        self.x_data = []
        self.y_data = []
        self.y_fit_data = []

        for line in plot_file.readlines():
            data_elements = line.split()
            self.x_data.append(float(data_elements[0]))
            self.y_data.append(float(data_elements[1]))
            self.y_fit_data.append(float(data_elements[2]))

        colors = sns.color_palette('Set2', 2)

        self.fig.delaxes(self.ax)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.x_data, self.y_data, label="Source", color=colors[0])
        self.ax.plot(self.x_data, self.y_fit_data, label="Fit", color=colors[1])

        self.ax.tick_params(axis='both', which='major', labelsize=14)
        self.ax.set_xlabel('2 $\\theta$ / Degrees', fontsize=14)
        self.ax.set_ylabel(r'Intensity / a.u.', fontsize=14)
        self.ax.legend(fontsize=14, frameon=True)

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

        fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Export Diffractometer Settings', os.path.join('config','diffractometer settings'), filter="*.json")

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

        fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Import Diffractometer Settings', os.path.join('config', 'fitting parameters'), filter="*.json")

        if fname:

            data_file = open(fname, 'w')

            fitting_params = {}

            for index, label in enumerate(self.parameter_labels):

                fitting_params[label] = (self.parameter_list[index].value(), self.parameter_enable_list[index].isChecked())

            ujson.dump(fitting_params, data_file, indent = 4)

            print 'Exported Fitting Parameters to: %s'%fname
            self.statusBar.showMessage('Exported Fitting Parameters to: %s'%fname)

    def import_fitting_params(self):

        fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Import Fitting Parameters', os.path.join('config','fitting parameters'), filter="*.json")

        if fname:

            data_file = open(fname, 'r')

            fitting_params = ujson.load(data_file)

            for index, label in enumerate(self.parameter_labels):

                param_value, enabled = fitting_params[label]

                self.parameter_list[index].setValue(param_value)
                self.parameter_enable_list[index].setChecked(enabled)

            print 'Imported Fitting Parameters from: %s'%fname
            self.statusBar.showMessage('Imported Fitting Parameters from: %s'%fname)

    def export_fitting_settings(self):

        fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export Fitting Settings', os.path.join('config', 'fitting settings'), filter="*.json")

        if fname:

            data_file = open(fname, 'w')

            fitting_settings = {}

            fitting_settings['theta min'] = self.theta_min_value.value()
            fitting_settings['theta max'] = self.theta_max_value.value()

            fitting_settings['iterations'] = self.iterations.value()
            fitting_settings['nskip']  = self.nskip.value()

            if self.number_layers.currentIndex() == 0:
                fitting_settings['layers'] = 1
            else:
                fitting_settings['layers'] = 2

            fitting_settings['nphi']  = self.n_phi.value()
            fitting_settings['nsg']  = self.n_sg.value()
            fitting_settings['epsilon'] = self.epsilon.value()

            if self.gradient_check_enable.currentIndex() == 0:
                fitting_settings['enable_gc'] = False
            else:
                fitting_settings['enable_gc'] = True

            fitting_settings['gc_delta']  = self.gradient_check_delta.value()

            ujson.dump(fitting_settings, data_file, indent = 4)

            print 'Exported Fitting Settings to: %s'%fname
            self.statusBar.showMessage('Exported Fitting Settings to: %s'%fname)

    def import_fitting_settings(self):

        fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Import Fitting Settings', os.path.join('config', 'fitting settings'), filter="*.json")

        if fname:

            data_file = open(fname, 'r')

            fitting_settings = ujson.load(data_file)

            self.theta_min_value.setValue(fitting_settings['theta min'])
            self.theta_max_value.setValue(fitting_settings['theta max'])

            self.iterations.setValue(fitting_settings['iterations'])
            self.nskip.setValue(fitting_settings['nskip'])


            if fitting_settings['layers'] == 1:
                self.number_layers.setCurrentIndex(0)
            elif fitting_settings['layers'] == 2:
                self.number_layers.setCurrentIndex(1)
            else:
                print "Error: Number of layers is not 1 or 2. Setting it to 1."
                self.number_layers.setCurrentIndex(0)

            self.n_phi.setValue(fitting_settings['nphi'])
            self.n_sg.setValue(fitting_settings['nsg'])
            self.epsilon.setValue(fitting_settings['epsilon'])

            if fitting_settings['enable_gc']:
                self.gradient_check_enable.setCurrentIndex(1)
            else:
                self.gradient_check_enable.setCurrentIndex(0)

            self.gradient_check_delta.setValue(fitting_settings['gc_delta'])

            print 'Imported Fitting Settings from: %s'%fname
            self.statusBar.showMessage('Imported Fitting Settings to: %s'%fname)


    def export_to_carboninp(self):

        fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export CARBON.INP',
                                                          os.path.join('config', 'fitting settings'), filter="CARBON.INP")

        if fname:
            self.write_carboninp(fname)

        print 'Exported in CARBON.INP format to: %s'%fname
        self.statusBar.showMessage('Exported in CARBON.INP format to: %s'%fname)

    def write_carboninp(self, destination):

        export_file = open(destination, 'w')

        export_file.write("SCAN.DAT\n")

        #
        export_file.write("  %5.2f    %5.2f %6.6f       %d  "%(self.theta_min_value.value(),
                                                        self.theta_max_value.value(),
                                                        self.wavelength.value(),
                                                        self.nskip.value())+
                          "            Thmin   Thmax   Lambda  Nskip\n")

        if self.number_layers.currentIndex() == 0:
            num_layers = 1
        else:
            num_layers = 2
        export_file.write("     18        %d        %d       %d  "%(self.n_phi.value(),
                                                                   self.n_sg.value(),
                                                                   num_layers
                                                                   )
                           +"            Npar    Nphi    Nsg     Nlayer\n")

        export_file.write(" %6.3f   %6.3f   %6.3f  %6.3f   %6.3f"%(self.sample_density.value(),
                                                                                 self.goniometer_radius.value(),
                                                                                 self.sample_depth.value(),
                                                                                 self.sample_width.value(),
                                                                                 self.beam_width.value()

                                                                                 )
                          +"     Rdens   L0      Wd      Ww      Bw\n")
        export_file.write("      %d   %6.5f                        "%(self.iterations.value(), self.epsilon.value())+
                          "       Itmax   Eps\n")

        if self.gradient_check_enable.currentIndex() == 1:
            enable_gc = 1
        else:
            enable_gc = 0

        export_file.write("      %d   %6.5f                        "%(enable_gc, self.gradient_check_delta.value())+
                          "       Itest   Dx\n")

        for index, label in enumerate(self.parameter_labels):

            param_value = self.parameter_list[index].value()
            if index == 0:
                param_str = ("%4.3E"%param_value).rjust(12)
            else:

                param_str = ("%10.6f"%param_value).rjust(12)

            if self.parameter_enable_list[index].isChecked():
                param_str += "  1    "
            else:
                param_str += "  0    "

            param_str += label.ljust(70)
            param_str += "\n"

            export_file.write(param_str)







    def import_from_carboninp(self):

        fname, _= QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.', filter='CARBON.INP')

        if fname:
            self.read_carboninp(fname)
            print 'Imported CARBON.INP parameters from: %s' % fname
            self.statusBar.showMessage('Imported CARBON.INP parameters from: %s' % fname)

    def read_carboninp(self, filename):

        config_file = open(filename, 'r')

        data_lines = config_file.readlines()

        # Thetamin, theta max, wavelength, nskip
        data_elements_1 = data_lines[1].split()

        self.theta_min_value.setValue(float(data_elements_1[0]))
        self.theta_max_value.setValue(float(data_elements_1[1]))
        self.wavelength.setValue(float(data_elements_1[2]))
        self.nskip.setValue(int(data_elements_1[3]))

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



    def start_fitting_process(self):

        print "Beginning Fitting Process"

        os.chdir('carbonxs')

        print "Wrote CARBON.INP to the CarbonXS Directory"

        self.write_carboninp("CARBON.INP")


        print "Calling CARBONXS.exe"
        self.fitting_process.start('CARBONXS.exe')
        self.menu_abort_fit.setEnabled(True)
        os.chdir('..')

    def abort_fit_process(self):

        self.fitting_process.kill()
        self.menu_abort_fit.setEnabled(False)
        self.abort_flag = True

    def fitting_finished(self):

        if not self.abort_flag:

            print "Fitting Complete"
            print "Reading new CARBON.INP data and plotting new data"

            self.menu_abort_fit.setEnabled(False)
            self.read_carboninp(os.path.join('carbonxs', 'CARBON.INP'))
            self.plot_fit_results()

        else:
            print "\n\n Fitting process aborted"

            self.abort_flag = False




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
