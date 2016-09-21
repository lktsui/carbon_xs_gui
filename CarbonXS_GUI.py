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
import shutil
import csv

use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE

if use_pyside:
    from PySide.QtCore import *
    from PySide.QtGui import *

class ConsoleStream(QtCore.QObject):

    message = QtCore.Signal(str)
    def __init__(self, parent=None):

        super(ConsoleStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, version):

        """
        Initializes the main window of the program
        :param version: String to use in the window header indicating the program version
        """

        super(MainWindow, self).__init__()

        self.setupUi(self)

        self.setWindowTitle("CarbonXS GUI v"+version)

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

        self.x_data = []
        self.y_data = []

        self.ax.tick_params(axis='both', which='major', labelsize=14)
        self.ax.set_xlabel('2 $\\theta$ / Degrees', fontsize=14)
        self.ax.set_ylabel(r'Intensity / a.u.', fontsize=14)
        self.ax.grid(True)
        self.addmpl(self.fig)


        # Fitting Process
        self.fitting_process = QtCore.QProcess(self)
        self.fitting_process.readyRead.connect(self.on_process_message)
        self.fitting_process.finished.connect(self.fitting_finished)
        self.pattern_calc_flag = False
        self.abort_flag = False

        self.assignWidgets()
        self.show()

    def data_init(self):
        """"
        On startup, read the last used Carbon.INP file
        """

        # Attempts to load a Carbon.INP file if it exists
        try:
            self.read_carboninp(os.path.join('carbonxs', 'CARBON.INP'))

            print "Loaded most recently used parameters successfully from 'carbonxs' directory."
        except IOError:
            print "No previous parameters found in 'carbonxs' directory."

        # Clears any SCAN.DAT file already in carbonxs directory
        if 'SCAN.DAT' in os.listdir('carbonxs'):
            os.remove(os.path.join('carbonxs', 'SCAN.DAT'))


    def init_ui_elements(self):
        """
        Initiates the toolbar buttons

        :return:
        """


        self.open_pattern_button = QtGui.QAction(QtGui.QIcon(os.path.join('icons','open.png')), 'Open Pattern', self)
        self.open_pattern_button.setStatusTip('Open Pattern')
        self.open_pattern_button.setToolTip("Opens a new XRD pattern.")

        self.calculate_pattern_button= QtGui.QAction(QtGui.QIcon(os.path.join('icons','calculator.png')), 'Calculate', self)
        self.calculate_pattern_button.setStatusTip('Calculate Pattern')
        self.calculate_pattern_button.setToolTip("Calculates pattern using current parameters without performing a fit.")

        self.fit_pattern_button= QtGui.QAction(QtGui.QIcon(os.path.join('icons','fit.png')), 'Fit', self)
        self.fit_pattern_button.setStatusTip('Fit Pattern')
        self.fit_pattern_button.setToolTip("Uses current parameters to perform a fit.")

        self.abort_fit_button= QtGui.QAction(QtGui.QIcon(os.path.join('icons','stop.png')), 'Abort', self)
        self.abort_fit_button.setStatusTip('Abort Fit')
        self.abort_fit_button.setEnabled(False)
        self.abort_fit_button.setToolTip("Aborts current fit by killing CarbonXS process.")

        self.export_fit_button= QtGui.QAction(QtGui.QIcon(os.path.join('icons','export.png')), 'Export Last Fit', self)
        self.export_fit_button.setStatusTip('Export Last Fit')
        self.export_fit_button.setToolTip("Export the carbon.out, carbon.dat, and new CARBON.INP files of the most recent fit run by CarbonXS.")

        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(self.open_pattern_button)
        self.toolbar.addAction(self.calculate_pattern_button)
        self.toolbar.addAction(self.fit_pattern_button)
        self.toolbar.addAction(self.abort_fit_button)
        self.toolbar.addAction(self.export_fit_button)

    @QtCore.Slot(str)
    def on_stream_message(self, message):
        """
        Method for reading print messages and error messages that are sent to the console
        :param message:
        :return:
        """


        self.console.moveCursor(QtGui.QTextCursor.End)
        self.console.insertPlainText(message)
        self.console.moveCursor(QtGui.QTextCursor.End)

    def on_process_message(self):
        """
        Method for reading messages from the carbonxs.exe process

        :return:
        """

        self.console.moveCursor(QtGui.QTextCursor.End)

        message = str(self.fitting_process.readAll())
        self.console.insertPlainText(message)
        self.console.moveCursor(QtGui.QTextCursor.End)

        # if a singular matrix is detected raise the option to abort the fit.
        if "Singular matrix." in message:
            reply = QtGui.QMessageBox.question(self, 'Singular matrix detected.',
                                               "Singular matrix detected. Abort?", QtGui.QMessageBox.Yes |
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)

            if reply == QtGui.QMessageBox.Yes:
                self.abort_fit_process()



    def addmpl(self, fig):
        """
        Add a Matplotlib object to the plot

        :param fig:
        :return:
        """


        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.mplwindow)
        self.mplvl.addWidget(self.mpl_toolbar)


        self.plot_buttons_layout = QtGui.QHBoxLayout()
        self.plot_pattern_button = QtGui.QPushButton(self)
        self.plot_pattern_button.setText("Pattern + Last Fit")
        self.plot_pattern_button.setToolTip("Plots the currently loaded pattern and the last fit result.")

        self.plot_difference_button = QtGui.QPushButton(self)
        self.plot_difference_button.setText("Last Fit Difference")
        self.plot_difference_button.setToolTip("Plots the difference between source and fit data for the last fit result.")

        self.plot_buttons_layout.addWidget(self.plot_pattern_button)
        self.plot_buttons_layout.addWidget(self.plot_difference_button)

        self.mplvl.addLayout(self.plot_buttons_layout)



    def assignWidgets(self):
        """
        Assigns buttons and menu items to functions

        :return:
        """


        # Toolbar buttons
        self.open_pattern_button.triggered.connect(self.open_pattern)
        self.calculate_pattern_button.triggered.connect(self.calculate_pattern)
        self.fit_pattern_button.triggered.connect(self.start_fitting_process)
        self.abort_fit_button.triggered.connect(self.abort_fit_process)
        self.export_fit_button.triggered.connect(self.export_fit_results)

        # Enable/Disable/Invert All Parameter Buttons
        self.enable_all_button.clicked.connect(self.enable_all_params)
        self.enable_none_button.clicked.connect(self.disable_all_params)
        self.enable_invert_button.clicked.connect(self.invert_all_params)


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
        self.menu_calculate_pattern.triggered.connect(self.calculate_pattern)
        self.menu_start_fit.triggered.connect(self.start_fitting_process)
        self.menu_abort_fit.triggered.connect(self.abort_fit_process)

        # Graph buttons
        self.plot_pattern_button.clicked.connect(self.plot_fit_results)
        self.plot_difference_button.clicked.connect(self.plot_difference)



    def plot_difference(self):

        """
        Loads the current carbon.dat and plots the difference between source and fit data.

        :return:
        """

        pattern_filename = os.path.join('carbonxs', 'carbon.dat')

        self.x_fit_data = []
        self.difference = []

        source_color = "#66c2a5"
        fit_color = "#fc8d62"


        pattern_file = open(pattern_filename, 'r')
        for line in pattern_file.readlines():
            data_elements = line.split()
            self.x_fit_data.append(float(data_elements[0]))
            self.difference.append(float(data_elements[1]) - float(data_elements[2]))

        self.fig.delaxes(self.ax)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.x_fit_data, self.difference, label="Source - Fit", linewidth = 2, color=fit_color)

        self.ax.tick_params(axis='both', which='major', labelsize=14)
        self.ax.set_xlabel('2 $\\theta$ / Degrees', fontsize=14)
        self.ax.set_ylabel(r'Intensity / a.u.', fontsize=14)
        self.ax.set_title("Difference Plot")
        self.ax.legend(fontsize=14, frameon=True)
        self.ax.grid(True)
        self.canvas.draw()



    def disable_all_params(self):
        """
        Turns off all fitting parameters
        :return:
        """

        for setting in self.parameter_enable_list:
            setting.setChecked(False)

    def enable_all_params(self):
        """
        Turns on all fitting parameters
        :return:
        """

        for setting in self.parameter_enable_list:
            setting.setChecked(True)

    def invert_all_params(self):
        """
        Inverts all fitting parameters. Enabled becomes disabled and disabled becomes enabled.
        :return:
        """

        for setting in self.parameter_enable_list:
            setting.setChecked(not setting.isChecked())



    def open_pattern(self):

        """
        Method to call up a file dialog and ask the user to load an XRD pattern
        :return:
        """

        fname, _= QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.')

        if fname:
            input_file = open(fname, 'r')

            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(input_file.readline())
            try:
                plot_data = np.loadtxt(input_file, delimiter=dialect.delimiter)

                source_color = "#66c2a5"



                self.x_data = plot_data[:, 0]
                self.y_data = plot_data[:, 1]

                self.theta_min_value.setValue(np.min(self.x_data))
                self.theta_max_value.setValue(np.max(self.x_data))

                data_pts = len(self.x_data)

                if data_pts > 3000:


                    new_dps = data_pts
                    divisor = 1
                    while new_dps > 3000:
                        divisor += 1
                        new_dps = data_pts / divisor

                    if divisor == 2:
                        divisor_str = '2nd'
                    elif divisor == 3:
                        divisor_str = '3rd'
                    else:
                        divisor_str = "%d th"%divisor


                    reply = QtGui.QMessageBox.question(self, 'Too many data points.',
                                                       "CarbonXS cannot process > 3000 data points. Do you want to truncate to every %s point?"%divisor_str, QtGui.QMessageBox.Yes |
                                                       QtGui.QMessageBox.No, QtGui.QMessageBox.No)

                    if reply == QtGui.QMessageBox.Yes:

                        self.x_data = self.x_data[0::divisor]
                        self.y_data = self.y_data[0::divisor]

                        new_length = len(self.x_data)
                        print "Data reduced from %d data points to %s data points by taking every %s point."%(data_pts, new_length, divisor_str)

                    else:

                        print "Warning: CarbonXS cannot process datasets larger than 3000 data points and will not fit the full pattern."



                self.fig.delaxes(self.ax)
                self.ax = self.fig.add_subplot(111)
                self.ax.plot(self.x_data, self.y_data, linewidth=2, label="Source", color=source_color)






                self.ax.tick_params(axis='both', which='major', labelsize=14)
                self.ax.set_xlabel('2 $\\theta$ / Degrees', fontsize=14)
                self.ax.set_ylabel(r'Intensity / a.u.', fontsize=14)
                self.ax.legend(fontsize=14, frameon=True)
                self.ax.grid(True)
                self.canvas.draw()


            except ValueError:
                print "Error: Improperly formatted pattern file in file %s."%fname
                print "The pattern file should be two columns of data."

    def plot_fit_results(self):
        """
        Load the most recently generated carbon.dat file and plot the fit results

        :return:
        """


        pattern_filename = os.path.join('carbonxs', 'carbon.dat')

        self.x_fit_data = []
        self.difference = []

        source_color = "#66c2a5"
        fit_color = "#fc8d62"


        pattern_file = open(pattern_filename, 'r')
        for line in pattern_file.readlines():
            data_elements = line.split()
            self.x_fit_data.append(float(data_elements[0]))
            self.difference.append(float(data_elements[2]))

        # colors = sns.color_palette('Set2', 2)

        self.fig.delaxes(self.ax)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.x_data, self.y_data, label="Source", linewidth = 2, color=source_color)
        self.ax.plot(self.x_fit_data, self.difference, label="Fit", linewidth = 2, color=fit_color)

        self.ax.tick_params(axis='both', which='major', labelsize=14)
        self.ax.set_xlabel('2 $\\theta$ / Degrees', fontsize=14)
        self.ax.set_ylabel(r'Intensity / a.u.', fontsize=14)
        self.ax.set_title("Fit Pattern")
        self.ax.legend(fontsize=14, frameon=True)
        self.ax.grid(True)
        self.canvas.draw()



    def export_diffractometer_params(self):
        """
        Exports currently loaded diffractometer files to a JSON file
        The default directory is "/config/diffractometer settings"

        :return:
        """


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
        """
        Imports diffractometer files from a JSON file
        The default directory is "/config/diffractometer settings"

        :return:
        """

        fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Export Diffractometer Settings', os.path.join('config','diffractometer settings'), filter="*.json")

        if fname:

            data_file = open(fname, 'r')


            try:
                diffractometer_settings = ujson.load(data_file)

                self.wavelength.setValue(diffractometer_settings['wavelength'])
                self.beam_width.setValue(diffractometer_settings['beam_width'])
                self.sample_width.setValue(diffractometer_settings['sample_width'])
                self.sample_depth.setValue(diffractometer_settings['sample_depth'])
                self.sample_density.setValue(diffractometer_settings['sample_density'])
                self.goniometer_radius.setValue(diffractometer_settings['gonio_radius'])

                print 'Imported Diffractometer Settings from: %s'%fname

                self.statusBar.showMessage('Imported Diffractometer Settings from: %s'%fname)

            except ValueError:
                print "Error in loading JSON file: %s."%(fname)
                print "Verify that the configuration file is properly formatted."

            except KeyError:
                import_type = 'diffractometer settings'
                print 'Error in importing %s from: %s.'%(import_type, fname)
                print 'Verify that this settings file is the right kind for this import.'


    def export_fitting_params(self):
        """
        Exports currently loaded fitting parameters files to a JSON file
        The default directory is "/config/fitting parameters"

        :return:
        """

        fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export Fitting Parameters', os.path.join('config', 'fitting parameters'), filter="*.json")

        if fname:

            data_file = open(fname, 'w')

            fitting_params = {}

            for index, label in enumerate(self.parameter_labels):

                fitting_params[label] = (self.parameter_list[index].value(), self.parameter_enable_list[index].isChecked())

            ujson.dump(fitting_params, data_file, indent = 4)

            print 'Exported Fitting Parameters to: %s'%fname
            self.statusBar.showMessage('Exported Fitting Parameters to: %s'%fname)

    def import_fitting_params(self):
        """
        Imports fitting parameters files from a JSON file
        The default directory is "/config/fitting parameters"

        :return:
        """

        fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Import Fitting Parameters', os.path.join('config','fitting parameters'), filter="*.json")

        if fname:

            try:
                data_file = open(fname, 'r')

                fitting_params = ujson.load(data_file)

                for index, label in enumerate(self.parameter_labels):

                    param_value, enabled = fitting_params[label]

                    self.parameter_list[index].setValue(param_value)
                    self.parameter_enable_list[index].setChecked(enabled)

                print 'Imported Fitting Parameters from: %s'%fname
                self.statusBar.showMessage('Imported Fitting Parameters from: %s'%fname)
            except ValueError:
                print "Error in loading JSON file: %s."%(fname)
                print "Verify that the configuration file is properly formatted."

            except KeyError:
                import_type = 'fitting parameters'
                print 'Error in importing %s from: %s.'%(import_type, fname)
                print 'Verify that this settings file is the right kind for this import.'

    def export_fitting_settings(self):

        """
        Exports currently loaded fitting settings files to a JSON file
        The default directory is "/config/fitting settings"

        :return:
        """
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

        """
        Import fitting settings from a JSON file
        The default directory is "/config/fitting settings"

        :return:
        """

        fname, opened = QtGui.QFileDialog.getOpenFileName(self, 'Import Fitting Settings', os.path.join('config', 'fitting settings'), filter="*.json")

        if fname:

            try:
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


            except ValueError:
                print "Error in loading JSON file: %s."%(fname)
                print "Verify that the configuration file is properly formatted."

            except KeyError:
                import_type = 'fitting settings'
                print 'Error in importing %s from: %s.'%(import_type, fname)
                print 'Verify that this settings file is the right kind for this import.'


    def export_to_carboninp(self):
        """
        Exports all current settings to a new CARBON.INP file
        This method is the part where user selects the destination.

        :return:
        """


        fname, opened = QtGui.QFileDialog.getSaveFileName(self, 'Export CARBON.INP',
                                                          os.path.join('config', 'fitting settings'), filter="CARBON.INP")

        if fname:
            self.write_carboninp(fname)

        print 'Exported in CARBON.INP format to: %s'%fname
        self.statusBar.showMessage('Exported in CARBON.INP format to: %s'%fname)

    def write_carboninp(self, destination, disable_fit = False):
        """
        Method which writes the currently loaded data to a Carbon.inp file

        :param destination: - File path to export to
        :param disable_fit: - Boolean which disables fit and only performs a pattern calculation if true

        :return:
        """


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


        if not disable_fit:
            iterations = self.iterations.value()
        else:
            iterations = 0

        export_file.write("      %d   %6.5f                        "%(iterations, self.epsilon.value())+
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

        """
        Method to read all settings from a carbon.inp file
        This is the method which the user choses the file

        :return:
        """

        fname, _= QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.', filter="*.inp")

        if fname:
            self.read_carboninp(fname)
            print 'Imported CARBON.INP parameters from: %s' % fname
            self.statusBar.showMessage('Imported CARBON.INP parameters from: %s' % fname)

    def read_carboninp(self, filename):
        """
        Method which processes loading of data from carbon.inp file

        :param filename: file path to load data from
        :return:
        """


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
            self.gradient_check_enable.setCurrentIndex(1)
        else:
            # Disable Gradient Checking
            self.gradient_check_enable.setCurrentIndex(0)


        self.gradient_check_delta.setValue(float(data_elements_5[1]))





        for index, line in enumerate(data_lines[6:]):
            config_elements = line.split()

            if "*" in config_elements[0]:
                print "Warning: Bad parameter found in "+self.parameter_labels[index]
                print "Setting parameter value to 0"
                param_value = 0
            else:

                param_value = float(config_elements[0])

            if config_elements[1] == '1':
                param_enable = True
            else:
                param_enable = False

            self.parameter_list[index].setValue(param_value)
            self.parameter_enable_list[index].setChecked(param_enable)


    def write_scan_data(self, output_file):
        """
        Uses currently loaded XRD pattern data and writes it to a format that carbonxs.exe can read

        :param output_file: file path for the destination
        :return:
        """


        scan_file = open(output_file, 'w')

        for x, y in zip(*(self.x_data, self.y_data)):

            data_line = "%4.2f\t%4.2f\n"%(x, y)

            scan_file.write(data_line)

    def sanity_checks(self):
        """
        Performs sanity checks on current settings and parameters before a fit is run.

        :return:
        """

        errors = 0

        if self.iterations.value() < 1:
            print "Number of iterations is less than 1. No fitting will be performed."
            print "Use Fitting -> Calculate Pattern to perform pattern calculation."
            errors += 1

        if not any([enable.isChecked() for enable in self.parameter_enable_list]):
            print "Error: No fitting parameters are enabled."
            errors +=1


        if self.sample_density.value() > 1.0 or self.sample_density.value() < 0.0:
            print "Sample Density must be between 0 and 1"
            errors += 1
        if self.param_14.value() > 1 or  self.param_14.value() < 0:
            print "Pr must be between 0 and 1"
            errors += 1
        if self.param_15.value() > 1 or  self.param_15.value() < 0:
            print "Pt must be between 0 and 1"
            errors += 1
        if self.param_12.value() < 0:
            print "Dab (In plane strain) must be greater than 0"
            errors += 1
        if self.param_13.value() < 0:
            print "Del (Interplanar strain) must be greater than 0"
            errors += 1

        if errors > 0:
            print "Found %d errors. Aborting Fit."%errors
            return False
        else:
            print "Parameter check passed with 0 errors. Proceeding with fit."
            return True



    def start_fitting_process(self):
        """
        Calls the fitting process to begin
        :return:
        """


        # Verifies that XRD pattern data has been loaded
        if len(self.x_data) > 0 and len(self.y_data) > 0:
            print "Beginning Fitting Process"

            # If all sanity checks pass, proceed with fit
            if self.sanity_checks():
                self.call_fit_program()

        # If not, prompt the user to load data
        else:

            reply = QtGui.QMessageBox.question(self, 'No XRD Pattern Loaded',
                                               "Do you want to load a pattern?", QtGui.QMessageBox.Yes |
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:

                self.open_pattern()
                # If a pattern has been loaded, proceeed with fit.
                if len(self.x_data) > 0 and len(self.y_data) > 0 and self.sanity_checks():
                    print "Loaded an XRD pattern"
                    if self.sanity_checks():
                        self.call_fit_program()

    def call_fit_program(self):
        """
        Starts the carbonxs.exe fit process
        :return:
        """


        os.chdir('carbonxs')

        print "Wrote CARBON.INP to the CarbonXS Directory"

        self.write_carboninp("CARBON.INP")

        print "Wrote SCAN.DAT to the CarbonXS Directory"

        self.write_scan_data("SCAN.DAT")
        self.pattern_calc_flag = False

        print "Calling CARBONXS.exe"
        self.fitting_process.start('CARBONXS.exe')

        # Sets menu flags to disable start of another process and enable aborting fit process
        self.menu_start_fitting.setEnabled(False)
        self.menu_calculate_pattern.setEnabled(False)
        self.calculate_pattern_button.setEnabled(False)
        self.fit_pattern_button.setEnabled(False)
        self.menu_abort_fit.setEnabled(True)
        self.abort_fit_button.setEnabled(True)
        os.chdir('..')


    def calculate_pattern(self):
        """
        Calculate a pattern based on the currently loaded parameters without performing a fit
        :return:
        """

        print "Beginning Pattern Calculation Process"

        os.chdir('carbonxs')

        print "Wrote CARBON.INP to the CarbonXS Directory"

        self.write_carboninp("CARBON.INP", disable_fit=True)

        print "Calling CARBONXS.exe"
        self.pattern_calc_flag = True

        self.menu_start_fitting.setEnabled(False)
        self.menu_calculate_pattern.setEnabled(False)
        self.calculate_pattern_button.setEnabled(False)
        self.fit_pattern_button.setEnabled(False)


        self.fitting_process.start('CARBONXS.exe')
        self.menu_abort_fit.setEnabled(True)
        self.abort_fit_button.setEnabled(True)

        os.chdir('..')

    def abort_fit_process(self):
        """
        Kills the currently running carbon.exe process
        :return:
        """

        self.fitting_process.kill()
        self.menu_abort_fit.setEnabled(False)
        self.abort_fit_button.setEnabled(False)

        self.menu_start_fitting.setEnabled(True)
        self.menu_calculate_pattern.setEnabled(True)
        self.calculate_pattern_button.setEnabled(True)
        self.fit_pattern_button.setEnabled(True)
        self.abort_flag = True

    def fitting_finished(self):
        """
        Method to handle completion of fitting process
        :return:
        """


        if not self.abort_flag:

            print "CarbonXS.exe Process Complete"

            # Exit Code 0 indicates successful completion
            if self.fitting_process.exitCode() == 0:

                if not self.pattern_calc_flag:
                    print "Reading new CARBON.INP data and plotting new data"
                    self.read_carboninp(os.path.join('carbonxs', 'CARBON.INP'))

                self.plot_fit_results()

                # If in fitting mode, give option to export fitting results
                if not self.pattern_calc_flag:

                    reply = QtGui.QMessageBox.question(self, 'Fit Completed',
                                                       "Export the results?", QtGui.QMessageBox.Yes |
                                                       QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        self.export_fit_results()


            # Exit Code 1 indicates a crash in CarbonXS
            # Do NOT load any settings the program wrote
            elif self.fitting_process.exitCode() == 1:
                print "Error: Fit failed due to crash in CarbonXS"
            else:
                print "Other error occurred"

            # Re-enable buttons to start process and disable buttons that abort process
            self.menu_abort_fit.setEnabled(False)
            self.abort_fit_button.setEnabled(False)

            self.menu_start_fitting.setEnabled(True)
            self.menu_calculate_pattern.setEnabled(True)
            self.calculate_pattern_button.setEnabled(True)
            self.fit_pattern_button.setEnabled(True)


        else:
            print "\n\n Fitting process aborted"

            self.abort_flag = False


    def export_fit_results(self):
        """
        Copies the carbon.out, carbon.dat, and CARBON.INP files currently in the carbonxs
        directory to a destination of your choice.
        :return:
        """


        fname, _ = QtGui.QFileDialog.getSaveFileName(self, 'Select Base Name For Results', '.')

        if fname:

            for data_file, export_suffix in [('carbon.out', '_carbon_out.txt'), ('carbon.dat', '_carbon_dat.txt'), ('CARBON.INP','_CARBON.INP')]:

                # Checks if the files exist in the directory
                if data_file in os.listdir('carbonxs'):
                    destination = fname + export_suffix

                    # Checks if the destination files already exists
                    if os.path.exists(destination):

                        # Prompts user to overwrite if it does
                        _, filename = os.path.split(destination)
                        reply = QtGui.QMessageBox.question(self, 'Fit Completed',
                                                           "%s exists. Overwrite?"%filename, QtGui.QMessageBox.Yes |
                                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                        if reply == QtGui.QMessageBox.Yes:
                            shutil.copy(os.path.join('carbonxs', data_file), fname + export_suffix)
                            print "Copied %s file to %s. (Overwrote old file)" % (data_file, destination)
                        else:
                            print "%s already exists. Did not overwrite." % destination

                    else:

                        shutil.copy(os.path.join('carbonxs', data_file), destination)
                        print "Copied %s file to %s" %(data_file, destination)



def main():

    version = "0.1.1"

    app = QtGui.QApplication(sys.argv)


    ex = MainWindow(version)

    console_stream = ConsoleStream()
    console_stream.message.connect(ex.on_stream_message)

    sys.stdout = console_stream
    sys.stderr = console_stream

    ex.data_init()

    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
