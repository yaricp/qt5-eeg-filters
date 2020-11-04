# -*- coding: utf-8 -*-
from loguru import logger
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.graph_right_align = 170
        self.graph_bottom_align = 125
        self.graph_pos = 20, 50
        self.graph_height = MainWindow.height() - self.graph_bottom_align
        self.graph_width = MainWindow.width() - self.graph_right_align
        self.graph = pg.PlotWidget(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(*self.graph_pos, self.graph_width, self.graph_height))      #0, 0, 830, 475
        self.graph.setBackground('w')

        self.listBandwidths = QtWidgets.QListWidget(self.centralwidget)
        self.listBandwidths.setEnabled(True)
        self.listBandwidths_size = 81, 391
        self.listBandwidths_right_align = 110
        self.listBandwidths_top_align = 50
        self.listBandwidths_pos = (
            MainWindow.width() - self.listBandwidths_right_align,
            self.listBandwidths_top_align
        )
        self.listBandwidths.setGeometry(QtCore.QRect(*self.listBandwidths_pos, *self.listBandwidths_size))
        self.listBandwidths.setObjectName("listBandwidths")
        self.buttonAdd = QtWidgets.QPushButton(self.centralwidget)
        self.buttonAdd_size = 81, 31
        self.buttonAdd_right_align = 110
        self.buttonAdd_top_align = 490
        self.buttonAdd_pos = (
            MainWindow.width() - self.buttonAdd_right_align,
            self.buttonAdd_top_align
        )
        self.buttonAdd.setGeometry(QtCore.QRect(*self.buttonAdd_pos, *self.buttonAdd_size))
        self.buttonAdd.setObjectName("buttonAdd")
        self.newBandwidthField = QtWidgets.QLineEdit(self.centralwidget)
        self.newBandwidthField_size = 81, 31
        self.newBandwidthField_right_align = 110
        self.newBandwidthField_top_align = 450
        self.newBandwidthField_pos = (
            MainWindow.width() - self.newBandwidthField_right_align,
            self.newBandwidthField_top_align
        )
        self.newBandwidthField.setGeometry(QtCore.QRect(*self.newBandwidthField_pos, *self.newBandwidthField_size))
        self.newBandwidthField.setObjectName("newBandwidthField")
        self.slider1 = QtWidgets.QSlider(QtCore.Qt.Vertical, self.centralwidget)
        self.slider1_size = 20, self.graph_height
        self.slider1_right_align = 140
        self.slider1_top_align = 50
        self.slider1_pos = (
            MainWindow.width() - self.slider1_right_align,
            self.slider1_top_align
        )
        self.slider1.setGeometry(QtCore.QRect(*self.slider1_pos, *self.slider1_size))
        self.slider1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider1.setTickInterval(1)

        self.buttonOpen = QtWidgets.QPushButton(self.centralwidget)
        self.buttonOpen_size = 83, 31
        self.buttonOpen_pos = 20, 10
        self.buttonOpen.setGeometry(QtCore.QRect(*self.buttonOpen_pos, *self.buttonOpen_size))
        self.buttonOpen.setObjectName("buttonOpen")

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


        self.buttonVisibleRegion = QtWidgets.QPushButton(self.centralwidget)
        self.buttonVisibleRegion .setGeometry(QtCore.QRect(440, 10, 83, 31))
        self.buttonVisibleRegion .setObjectName("buttonVisibleRegion ")

        self.buttonSave = QtWidgets.QPushButton(self.centralwidget)
        self.buttonSave.setGeometry(QtCore.QRect(112, 10, 81, 31))
        self.buttonSave.setObjectName("buttonSave")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_height = 25
        self.progressBar_size = self.graph.width(), self.progressBar_height
        self.progressBar_left = 20
        self.progressBar_poz_bottom_align = 70
        self.progressBar_pos = (
            self.progressBar_left,
            MainWindow.height() - self.progressBar_poz_bottom_align
        )
        self.progressBar.setGeometry(QtCore.QRect(*self.progressBar_pos, *self.progressBar_size))
        self.progressBar.setProperty("value", 100)
        self.progressBar.setProperty("visible", 1)
        self.progressBar.setObjectName("progressBar")


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
