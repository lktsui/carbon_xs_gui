# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\untitled\text_file_viewer.ui'
#
# Created: Tue Mar 14 14:47:24 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 548)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 531))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_display = QtGui.QPlainTextEdit(self.verticalLayoutWidget)
        self.text_display.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.text_display.setReadOnly(True)
        self.text_display.setObjectName("text_display")
        self.verticalLayout.addWidget(self.text_display)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.header_lines_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.header_lines_label.setObjectName("header_lines_label")
        self.horizontalLayout_2.addWidget(self.header_lines_label)
        self.header_lines = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.header_lines.setMaximum(1000000000)
        self.header_lines.setObjectName("header_lines")
        self.horizontalLayout_2.addWidget(self.header_lines)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.separator_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.separator_label.setObjectName("separator_label")
        self.horizontalLayout_3.addWidget(self.separator_label)
        self.separator_selector = QtGui.QComboBox(self.verticalLayoutWidget)
        self.separator_selector.setObjectName("separator_selector")
        self.separator_selector.addItem("")
        self.separator_selector.addItem("")
        self.horizontalLayout_3.addWidget(self.separator_selector)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout.addWidget(self.ok_button)
        self.cancel_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.header_lines_label.setText(QtGui.QApplication.translate("Dialog", "Header Lines", None, QtGui.QApplication.UnicodeUTF8))
        self.separator_label.setText(QtGui.QApplication.translate("Dialog", "Data Separator", None, QtGui.QApplication.UnicodeUTF8))
        self.separator_selector.setItemText(0, QtGui.QApplication.translate("Dialog", "Whitespace (Space, Tab)", None, QtGui.QApplication.UnicodeUTF8))
        self.separator_selector.setItemText(1, QtGui.QApplication.translate("Dialog", "Comma (,)", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_button.setText(QtGui.QApplication.translate("Dialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_button.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

