# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/untitled/mainwindow.ui'
#
# Created: Thu Sep 15 11:38:53 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1473, 907)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayoutWidget = QtGui.QWidget(self.centralWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 501, 541))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.fit_params = QtGui.QGridLayout(self.gridLayoutWidget)
        self.fit_params.setContentsMargins(0, 0, 0, 0)
        self.fit_params.setObjectName("fit_params")
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.fit_params.addWidget(self.label, 1, 0, 1, 3)
        self.param_label_3 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_3.setFont(font)
        self.param_label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_3.setObjectName("param_label_3")
        self.fit_params.addWidget(self.param_label_3, 5, 2, 1, 1)
        self.param_label_1 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_1.setFont(font)
        self.param_label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_1.setObjectName("param_label_1")
        self.fit_params.addWidget(self.param_label_1, 3, 2, 1, 1)
        self.param_3 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_3.setDecimals(6)
        self.param_3.setMaximum(99999999.0)
        self.param_3.setObjectName("param_3")
        self.fit_params.addWidget(self.param_3, 5, 0, 1, 1)
        self.param_16 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_16.setDecimals(6)
        self.param_16.setMaximum(99999999.0)
        self.param_16.setObjectName("param_16")
        self.fit_params.addWidget(self.param_16, 18, 0, 1, 1)
        self.param_17 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_17.setDecimals(6)
        self.param_17.setMaximum(99999999.0)
        self.param_17.setObjectName("param_17")
        self.fit_params.addWidget(self.param_17, 19, 0, 1, 1)
        self.param_1 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_1.setDecimals(6)
        self.param_1.setMaximum(99999999.0)
        self.param_1.setObjectName("param_1")
        self.fit_params.addWidget(self.param_1, 3, 0, 1, 1)
        self.param_5 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_5.setDecimals(6)
        self.param_5.setMaximum(99999999.0)
        self.param_5.setObjectName("param_5")
        self.fit_params.addWidget(self.param_5, 7, 0, 1, 1)
        self.param_2 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_2.setDecimals(6)
        self.param_2.setMaximum(99999999.0)
        self.param_2.setObjectName("param_2")
        self.fit_params.addWidget(self.param_2, 4, 0, 1, 1)
        self.param_label_9 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_9.setFont(font)
        self.param_label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_9.setObjectName("param_label_9")
        self.fit_params.addWidget(self.param_label_9, 11, 2, 1, 1)
        self.param_label_15 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_15.setFont(font)
        self.param_label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_15.setObjectName("param_label_15")
        self.fit_params.addWidget(self.param_label_15, 17, 2, 1, 1)
        self.param_label_17 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_17.setFont(font)
        self.param_label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_17.setObjectName("param_label_17")
        self.fit_params.addWidget(self.param_label_17, 19, 2, 1, 1)
        self.param_4 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_4.setDecimals(6)
        self.param_4.setMaximum(99999999.0)
        self.param_4.setObjectName("param_4")
        self.fit_params.addWidget(self.param_4, 6, 0, 1, 1)
        self.param_label_14 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_14.setFont(font)
        self.param_label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_14.setObjectName("param_label_14")
        self.fit_params.addWidget(self.param_label_14, 16, 2, 1, 1)
        self.param_11 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_11.setDecimals(6)
        self.param_11.setMaximum(99999999.0)
        self.param_11.setObjectName("param_11")
        self.fit_params.addWidget(self.param_11, 13, 0, 1, 1)
        self.param_12 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_12.setDecimals(6)
        self.param_12.setMaximum(99999999.0)
        self.param_12.setObjectName("param_12")
        self.fit_params.addWidget(self.param_12, 14, 0, 1, 1)
        self.param_15 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_15.setDecimals(6)
        self.param_15.setMaximum(99999999.0)
        self.param_15.setObjectName("param_15")
        self.fit_params.addWidget(self.param_15, 17, 0, 1, 1)
        self.param_enable_12 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_12.setObjectName("param_enable_12")
        self.fit_params.addWidget(self.param_enable_12, 14, 1, 1, 1)
        self.param_enable_8 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_8.setObjectName("param_enable_8")
        self.fit_params.addWidget(self.param_enable_8, 10, 1, 1, 1)
        self.param_enable_15 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_15.setObjectName("param_enable_15")
        self.fit_params.addWidget(self.param_enable_15, 17, 1, 1, 1)
        self.param_label_0 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_0.setFont(font)
        self.param_label_0.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_0.setObjectName("param_label_0")
        self.fit_params.addWidget(self.param_label_0, 2, 2, 1, 1)
        self.param_enable_14 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_14.setObjectName("param_enable_14")
        self.fit_params.addWidget(self.param_enable_14, 16, 1, 1, 1)
        self.param_enable_17 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_17.setObjectName("param_enable_17")
        self.fit_params.addWidget(self.param_enable_17, 19, 1, 1, 1)
        self.param_enable_16 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_16.setObjectName("param_enable_16")
        self.fit_params.addWidget(self.param_enable_16, 18, 1, 1, 1)
        self.param_enable_0 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_0.setObjectName("param_enable_0")
        self.fit_params.addWidget(self.param_enable_0, 2, 1, 1, 1)
        self.param_enable_9 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_9.setObjectName("param_enable_9")
        self.fit_params.addWidget(self.param_enable_9, 11, 1, 1, 1)
        self.param_label_11 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_11.setFont(font)
        self.param_label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_11.setObjectName("param_label_11")
        self.fit_params.addWidget(self.param_label_11, 13, 2, 1, 1)
        self.param_label_12 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_12.setFont(font)
        self.param_label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_12.setObjectName("param_label_12")
        self.fit_params.addWidget(self.param_label_12, 14, 2, 1, 1)
        self.param_label_13 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_13.setFont(font)
        self.param_label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_13.setObjectName("param_label_13")
        self.fit_params.addWidget(self.param_label_13, 15, 2, 1, 1)
        self.param_label_4 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_4.setFont(font)
        self.param_label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_4.setObjectName("param_label_4")
        self.fit_params.addWidget(self.param_label_4, 6, 2, 1, 1)
        self.param_label_7 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_7.setFont(font)
        self.param_label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_7.setObjectName("param_label_7")
        self.fit_params.addWidget(self.param_label_7, 9, 2, 1, 1)
        self.param_label_5 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_5.setFont(font)
        self.param_label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_5.setObjectName("param_label_5")
        self.fit_params.addWidget(self.param_label_5, 7, 2, 1, 1)
        self.param_label_8 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_8.setFont(font)
        self.param_label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_8.setObjectName("param_label_8")
        self.fit_params.addWidget(self.param_label_8, 10, 2, 1, 1)
        self.param_label_16 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_16.setFont(font)
        self.param_label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_16.setObjectName("param_label_16")
        self.fit_params.addWidget(self.param_label_16, 18, 2, 1, 1)
        self.param_label_6 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_6.setFont(font)
        self.param_label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_6.setObjectName("param_label_6")
        self.fit_params.addWidget(self.param_label_6, 8, 2, 1, 1)
        self.param_label_2 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_2.setFont(font)
        self.param_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_2.setObjectName("param_label_2")
        self.fit_params.addWidget(self.param_label_2, 4, 2, 1, 1)
        self.param_enable_6 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_6.setObjectName("param_enable_6")
        self.fit_params.addWidget(self.param_enable_6, 8, 1, 1, 1)
        self.param_enable_1 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_1.setObjectName("param_enable_1")
        self.fit_params.addWidget(self.param_enable_1, 3, 1, 1, 1)
        self.param_enable_2 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_2.setObjectName("param_enable_2")
        self.fit_params.addWidget(self.param_enable_2, 4, 1, 1, 1)
        self.param_enable_4 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_4.setObjectName("param_enable_4")
        self.fit_params.addWidget(self.param_enable_4, 6, 1, 1, 1)
        self.param_enable_3 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_3.setObjectName("param_enable_3")
        self.fit_params.addWidget(self.param_enable_3, 5, 1, 1, 1)
        self.param_enable_5 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_5.setObjectName("param_enable_5")
        self.fit_params.addWidget(self.param_enable_5, 7, 1, 1, 1)
        self.param_14 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_14.setDecimals(6)
        self.param_14.setMaximum(99999999.0)
        self.param_14.setObjectName("param_14")
        self.fit_params.addWidget(self.param_14, 16, 0, 1, 1)
        self.param_enable_13 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_13.setObjectName("param_enable_13")
        self.fit_params.addWidget(self.param_enable_13, 15, 1, 1, 1)
        self.param_enable_10 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_10.setObjectName("param_enable_10")
        self.fit_params.addWidget(self.param_enable_10, 12, 1, 1, 1)
        self.param_enable_11 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_11.setObjectName("param_enable_11")
        self.fit_params.addWidget(self.param_enable_11, 13, 1, 1, 1)
        self.param_enable_7 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.param_enable_7.setObjectName("param_enable_7")
        self.fit_params.addWidget(self.param_enable_7, 9, 1, 1, 1)
        self.param_0 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_0.setDecimals(6)
        self.param_0.setMaximum(99999999.0)
        self.param_0.setObjectName("param_0")
        self.fit_params.addWidget(self.param_0, 2, 0, 1, 1)
        self.param_label_10 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.param_label_10.setFont(font)
        self.param_label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.param_label_10.setObjectName("param_label_10")
        self.fit_params.addWidget(self.param_label_10, 12, 2, 1, 1)
        self.param_13 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_13.setDecimals(6)
        self.param_13.setMaximum(99999999.0)
        self.param_13.setObjectName("param_13")
        self.fit_params.addWidget(self.param_13, 15, 0, 1, 1)
        self.param_8 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_8.setDecimals(6)
        self.param_8.setMaximum(99999999.0)
        self.param_8.setObjectName("param_8")
        self.fit_params.addWidget(self.param_8, 10, 0, 1, 1)
        self.param_6 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_6.setDecimals(6)
        self.param_6.setMaximum(99999999.0)
        self.param_6.setObjectName("param_6")
        self.fit_params.addWidget(self.param_6, 8, 0, 1, 1)
        self.param_7 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_7.setDecimals(6)
        self.param_7.setMaximum(99999999.0)
        self.param_7.setObjectName("param_7")
        self.fit_params.addWidget(self.param_7, 9, 0, 1, 1)
        self.param_9 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_9.setDecimals(6)
        self.param_9.setMaximum(99999999.0)
        self.param_9.setObjectName("param_9")
        self.fit_params.addWidget(self.param_9, 11, 0, 1, 1)
        self.param_10 = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.param_10.setDecimals(6)
        self.param_10.setMaximum(99999999.0)
        self.param_10.setObjectName("param_10")
        self.fit_params.addWidget(self.param_10, 12, 0, 1, 1)
        self.mplwindow = QtGui.QWidget(self.centralWidget)
        self.mplwindow.setGeometry(QtCore.QRect(610, 20, 801, 541))
        self.mplwindow.setObjectName("mplwindow")
        self.verticalLayout = QtGui.QVBoxLayout(self.mplwindow)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mplvl = QtGui.QVBoxLayout()
        self.mplvl.setObjectName("mplvl")
        self.verticalLayout.addLayout(self.mplvl)
        self.gridLayoutWidget_2 = QtGui.QWidget(self.centralWidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 570, 501, 82))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.fitting_settings = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.fitting_settings.setContentsMargins(0, 0, 0, 0)
        self.fitting_settings.setObjectName("fitting_settings")
        self.iterations_label = QtGui.QLabel(self.gridLayoutWidget_2)
        self.iterations_label.setObjectName("iterations_label")
        self.fitting_settings.addWidget(self.iterations_label, 1, 2, 1, 1)
        self.theta_min_value = QtGui.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.theta_min_value.setMaximum(180.0)
        self.theta_min_value.setObjectName("theta_min_value")
        self.fitting_settings.addWidget(self.theta_min_value, 2, 0, 1, 1)
        self.theta_min_label = QtGui.QLabel(self.gridLayoutWidget_2)
        self.theta_min_label.setObjectName("theta_min_label")
        self.fitting_settings.addWidget(self.theta_min_label, 1, 0, 1, 1)
        self.theta_max_label = QtGui.QLabel(self.gridLayoutWidget_2)
        self.theta_max_label.setObjectName("theta_max_label")
        self.fitting_settings.addWidget(self.theta_max_label, 1, 1, 1, 1)
        self.iterations = QtGui.QSpinBox(self.gridLayoutWidget_2)
        self.iterations.setMinimum(1)
        self.iterations.setMaximum(999999999)
        self.iterations.setObjectName("iterations")
        self.fitting_settings.addWidget(self.iterations, 2, 2, 1, 1)
        self.theta_max_value = QtGui.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.theta_max_value.setMaximum(180.0)
        self.theta_max_value.setObjectName("theta_max_value")
        self.fitting_settings.addWidget(self.theta_max_value, 2, 1, 1, 1)
        self.fitting_settings_label = QtGui.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.fitting_settings_label.setFont(font)
        self.fitting_settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.fitting_settings_label.setObjectName("fitting_settings_label")
        self.fitting_settings.addWidget(self.fitting_settings_label, 0, 0, 1, 3)
        self.gridLayoutWidget_3 = QtGui.QWidget(self.centralWidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(20, 680, 501, 151))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.diffract_settings = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.diffract_settings.setContentsMargins(0, 0, 0, 0)
        self.diffract_settings.setObjectName("diffract_settings")
        self.wavelength_label = QtGui.QLabel(self.gridLayoutWidget_3)
        self.wavelength_label.setObjectName("wavelength_label")
        self.diffract_settings.addWidget(self.wavelength_label, 1, 0, 1, 1)
        self.sample_depth = QtGui.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.sample_depth.setMaximum(1000000000.0)
        self.sample_depth.setObjectName("sample_depth")
        self.diffract_settings.addWidget(self.sample_depth, 2, 1, 1, 1)
        self.wavelength = QtGui.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.wavelength.setEnabled(True)
        self.wavelength.setDecimals(5)
        self.wavelength.setMaximum(1000000000.0)
        self.wavelength.setObjectName("wavelength")
        self.diffract_settings.addWidget(self.wavelength, 2, 0, 1, 1)
        self.diffract_settings_label = QtGui.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.diffract_settings_label.setFont(font)
        self.diffract_settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.diffract_settings_label.setObjectName("diffract_settings_label")
        self.diffract_settings.addWidget(self.diffract_settings_label, 0, 0, 1, 3)
        self.sample_depth_label = QtGui.QLabel(self.gridLayoutWidget_3)
        self.sample_depth_label.setObjectName("sample_depth_label")
        self.diffract_settings.addWidget(self.sample_depth_label, 1, 1, 1, 1)
        self.sample_width_label = QtGui.QLabel(self.gridLayoutWidget_3)
        self.sample_width_label.setObjectName("sample_width_label")
        self.diffract_settings.addWidget(self.sample_width_label, 1, 2, 1, 1)
        self.goniometer_radius_label = QtGui.QLabel(self.gridLayoutWidget_3)
        self.goniometer_radius_label.setObjectName("goniometer_radius_label")
        self.diffract_settings.addWidget(self.goniometer_radius_label, 3, 0, 1, 1)
        self.sample_width = QtGui.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.sample_width.setMaximum(1000000000.0)
        self.sample_width.setObjectName("sample_width")
        self.diffract_settings.addWidget(self.sample_width, 2, 2, 1, 1)
        self.goniometer_radius = QtGui.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.goniometer_radius.setMaximum(1000000000.0)
        self.goniometer_radius.setObjectName("goniometer_radius")
        self.diffract_settings.addWidget(self.goniometer_radius, 4, 0, 1, 1)
        self.sample_density_label = QtGui.QLabel(self.gridLayoutWidget_3)
        self.sample_density_label.setObjectName("sample_density_label")
        self.diffract_settings.addWidget(self.sample_density_label, 3, 2, 1, 1)
        self.beam_width_label = QtGui.QLabel(self.gridLayoutWidget_3)
        self.beam_width_label.setObjectName("beam_width_label")
        self.diffract_settings.addWidget(self.beam_width_label, 3, 1, 1, 1)
        self.beam_width = QtGui.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.beam_width.setMaximum(1000000000.0)
        self.beam_width.setObjectName("beam_width")
        self.diffract_settings.addWidget(self.beam_width, 4, 1, 1, 1)
        self.sample_density = QtGui.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.sample_density.setMaximum(1.0)
        self.sample_density.setSingleStep(0.01)
        self.sample_density.setObjectName("sample_density")
        self.diffract_settings.addWidget(self.sample_density, 4, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1473, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuImport = QtGui.QMenu(self.menuFile)
        self.menuImport.setObjectName("menuImport")
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName("menuExport")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menu_open_xrd_pattern = QtGui.QAction(MainWindow)
        self.menu_open_xrd_pattern.setObjectName("menu_open_xrd_pattern")
        self.menu_import_carboninp = QtGui.QAction(MainWindow)
        self.menu_import_carboninp.setObjectName("menu_import_carboninp")
        self.actionDiffractometer_Settings = QtGui.QAction(MainWindow)
        self.actionDiffractometer_Settings.setObjectName("actionDiffractometer_Settings")
        self.menu_export_diffsettings = QtGui.QAction(MainWindow)
        self.menu_export_diffsettings.setObjectName("menu_export_diffsettings")
        self.menu_import_diffsettings = QtGui.QAction(MainWindow)
        self.menu_import_diffsettings.setObjectName("menu_import_diffsettings")
        self.menuImport.addAction(self.menu_import_carboninp)
        self.menuImport.addAction(self.menu_import_diffsettings)
        self.menuExport.addAction(self.menu_export_diffsettings)
        self.menuFile.addAction(self.menu_open_xrd_pattern)
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Fitting Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_3.setText(QtGui.QApplication.translate("MainWindow", "Background S^2", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_1.setText(QtGui.QApplication.translate("MainWindow", "Background Constant", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_9.setText(QtGui.QApplication.translate("MainWindow", "La, Coherence Length", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_15.setText(QtGui.QApplication.translate("MainWindow", "Pt, Probability of 3R Stacking", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_17.setText(QtGui.QApplication.translate("MainWindow", "PO, Preferential Orientation Factor", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_14.setText(QtGui.QApplication.translate("MainWindow", "Pr, Probability of Random Stacking", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_12.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_8.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_15.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_0.setText(QtGui.QApplication.translate("MainWindow", "Scale Factor (a.u.)", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_14.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_17.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_16.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_0.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_9.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_11.setText(QtGui.QApplication.translate("MainWindow", "SM, Width of M Distribution", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_12.setText(QtGui.QApplication.translate("MainWindow", "DAB, In plane strain", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_13.setText(QtGui.QApplication.translate("MainWindow", "del, Inter Plane Strain", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_4.setText(QtGui.QApplication.translate("MainWindow", "Background S^3", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_7.setText(QtGui.QApplication.translate("MainWindow", "A, In Plane Cell Constant (Angstrom)", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_5.setText(QtGui.QApplication.translate("MainWindow", "Background S^4", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_8.setText(QtGui.QApplication.translate("MainWindow", "d002, Interlayer Spacing (Angstrom)", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_16.setText(QtGui.QApplication.translate("MainWindow", "Debye Waller Temperature Factor, (Angstrom^2)", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_6.setText(QtGui.QApplication.translate("MainWindow", "Background 1/S", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_2.setText(QtGui.QApplication.translate("MainWindow", "Background S", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_6.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_1.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_2.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_4.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_3.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_5.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_13.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_10.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_11.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_enable_7.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.param_label_10.setText(QtGui.QApplication.translate("MainWindow", "M, Number of Layers", None, QtGui.QApplication.UnicodeUTF8))
        self.iterations_label.setText(QtGui.QApplication.translate("MainWindow", "Iterations", None, QtGui.QApplication.UnicodeUTF8))
        self.theta_min_label.setText(QtGui.QApplication.translate("MainWindow", "Theta Min", None, QtGui.QApplication.UnicodeUTF8))
        self.theta_max_label.setText(QtGui.QApplication.translate("MainWindow", "Theta Max", None, QtGui.QApplication.UnicodeUTF8))
        self.fitting_settings_label.setText(QtGui.QApplication.translate("MainWindow", "Fitting Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.wavelength_label.setText(QtGui.QApplication.translate("MainWindow", "Wavelength (Angstrom)", None, QtGui.QApplication.UnicodeUTF8))
        self.diffract_settings_label.setText(QtGui.QApplication.translate("MainWindow", "Diffractometer Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.sample_depth_label.setText(QtGui.QApplication.translate("MainWindow", "Sample Depth (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.sample_width_label.setText(QtGui.QApplication.translate("MainWindow", "Sample Width (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.goniometer_radius_label.setText(QtGui.QApplication.translate("MainWindow", "Goniometer Radius (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.sample_density_label.setText(QtGui.QApplication.translate("MainWindow", "Sample Density Fraction", None, QtGui.QApplication.UnicodeUTF8))
        self.beam_width_label.setText(QtGui.QApplication.translate("MainWindow", "Beam Width (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuImport.setTitle(QtGui.QApplication.translate("MainWindow", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.menuExport.setTitle(QtGui.QApplication.translate("MainWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_open_xrd_pattern.setText(QtGui.QApplication.translate("MainWindow", "Open XRD Pattern", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_import_carboninp.setText(QtGui.QApplication.translate("MainWindow", "From CARBON.INP", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDiffractometer_Settings.setText(QtGui.QApplication.translate("MainWindow", "Diffractometer Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_export_diffsettings.setText(QtGui.QApplication.translate("MainWindow", "Diffractometer Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_import_diffsettings.setText(QtGui.QApplication.translate("MainWindow", "Diffractometer Settings", None, QtGui.QApplication.UnicodeUTF8))

