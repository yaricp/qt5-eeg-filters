# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqtgraph.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.listBandwidths = QtWidgets.QListWidget(self.centralwidget)
        self.listBandwidths.setEnabled(True)
        self.listBandwidths.setGeometry(QtCore.QRect(890, 50, 81, 391))
        self.listBandwidths.setObjectName("listBandwidths")
        self.buttonOpen = QtWidgets.QPushButton(self.centralwidget)
        self.buttonOpen.setGeometry(QtCore.QRect(20, 10, 83, 31))
        self.buttonOpen.setObjectName("buttonOpen")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(890, 450, 81, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        #TODO: не хватает подписей к полям редактирования
        self.lineEditMaxStart = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditMaxStart.setGeometry(QtCore.QRect(300, 15, 60, 20))
        self.lineEditMaxStart.setObjectName("lineEditMaxStart")
        self.lineEditMaxEnd = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditMaxEnd.setGeometry(QtCore.QRect(370, 15, 60, 20))
        self.lineEditMaxEnd.setObjectName("lineEditMaxEnd")
        self.lineEditMinStart = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditMinStart.setGeometry(QtCore.QRect(535, 15, 60, 20))
        self.lineEditMinStart.setObjectName("lineEditMinStart")
        self.lineEditMinEnd = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditMinEnd.setGeometry(QtCore.QRect(605, 15, 60, 20))
        self.lineEditMinEnd.setObjectName("lineEditMinEnd")
        self.buttonAdd = QtWidgets.QPushButton(self.centralwidget)
        self.buttonAdd.setGeometry(QtCore.QRect(890, 490, 81, 31))
        self.buttonAdd.setObjectName("buttonAdd")

        self.buttonVisibleRegion = QtWidgets.QPushButton(self.centralwidget)
        self.buttonVisibleRegion .setGeometry(QtCore.QRect(440, 10, 83, 31))
        self.buttonVisibleRegion .setObjectName("buttonVisibleRegion ")

        self.buttonSave = QtWidgets.QPushButton(self.centralwidget)
        self.buttonSave.setGeometry(QtCore.QRect(112, 10, 81, 31))
        self.buttonSave.setObjectName("buttonSave")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 50, 861, 471))
        self.widget.setObjectName("widget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 525, 830, 31))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setProperty("visible", 0)
        self.progressBar.setObjectName("progressBar")
        self.slider1 = QtWidgets.QSlider(QtCore.Qt.Vertical, self.centralwidget)
        self.slider1.setGeometry(QtCore.QRect(860, 50, 20, 391))
        
        self.slider1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider1.setTickInterval(1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 994, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionsave = QtWidgets.QAction(MainWindow)
        self.actionsave.setObjectName("actionsave")
        self.actionsave_as = QtWidgets.QAction(MainWindow)
        self.actionsave_as.setObjectName("actionsave_as")
        self.retranslateUi(MainWindow)
        self.listBandwidths.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EEG-Filters"))
        self.buttonOpen.setText(_translate("MainWindow", "Open"))
        self.buttonAdd.setText(_translate("MainWindow", "Add"))
        self.buttonVisibleRegion.setText(_translate("MainWindow", "HideRegions"))
        self.buttonSave.setText(_translate("MainWindow", "Save"))
        self.actionopen.setText(_translate("MainWindow", "open"))
        self.actionsave.setText(_translate("MainWindow", "save"))
        self.actionsave_as.setText(_translate("MainWindow", "save as"))
