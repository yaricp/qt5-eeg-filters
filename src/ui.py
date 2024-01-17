# -*- coding: utf-8 -*-
from loguru import logger
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")

        self.main_right_margin = 5
        self.main_left_margin = 5
        self.main_top_margin = 5
        self.main_bottom_margin = 35

        self.bandwidth_area_width = 76
        self.top_buttons_width = 83
        self.top_buttons_height = 31
        self.left_checkboxes_width = 73
        self.left_checkboxes_height = 12
        self.slider1_size = 18

        self.progress_bar_height = 25

        self.progressBar = QtWidgets.QProgressBar(
            self.centralwidget
        )
        self.progressBar.setProperty("value", 100)
        self.progressBar.setProperty("visible", 1)
        self.progressBar.setObjectName("progressBar")

        self.buttonAdd = QtWidgets.QPushButton(
            self.centralwidget
        )
        self.buttonAdd.setObjectName("buttonAdd")
        
        self.newBandwidthField = QtWidgets.QLineEdit(
            self.centralwidget
        )
        self.newBandwidthField.setObjectName("newBandwidthField")
        
        self.listBandwidths = QtWidgets.QListWidget(
            self.centralwidget
        )
        self.listBandwidths.setEnabled(True)
        self.listBandwidths.setObjectName("listBandwidths")
        
        self.slider1 = QtWidgets.QSlider(
            QtCore.Qt.Vertical, self.centralwidget
        )
        self.slider1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider1.setTickInterval(1)

        self.graph = pg.PlotWidget(self.centralwidget)
        self.graph.setBackground('w')

        self.check_box_all = QtWidgets.QCheckBox("ckbxall", self.centralwidget)
        self.check_box_all.setObjectName("ckbxall")
        
        self.check_box_all.setText("all")
        
        self.buttonOpen = QtWidgets.QPushButton(
            self.centralwidget
        )
        self.buttonOpen.setObjectName("buttonOpen")

        self.buttonSave = QtWidgets.QPushButton(
            self.centralwidget
        )
        self.buttonSave.setObjectName("buttonSave")

        #TODO: не хватает подписей к полям редактирования
        self.lineEditMaxStart = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditMaxStart.setObjectName("lineEditMaxStart")
        
        self.lineEditMaxEnd = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditMaxEnd.setObjectName("lineEditMaxEnd")
        
        self.lineEditMinStart = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditMinStart.setObjectName("lineEditMinStart")
        
        self.lineEditMinEnd = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditMinEnd.setObjectName("lineEditMinEnd")

        self.buttonVisibleRegion = QtWidgets.QPushButton(self.centralwidget)
        self.buttonVisibleRegion.setObjectName("buttonVisibleRegion")

        self.buttonStartSearch = QtWidgets.QPushButton(self.centralwidget)
        self.buttonStartSearch.setObjectName("buttonStartSearch")

        self.lineEditHFRH = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditHFRH.setObjectName("lineEditHFRH")

        self.lineEditHFRL = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditHFRL.setObjectName("lineEditHFRL")

        self.lineEditHFS = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditHFS.setObjectName("lineEditHFS")

        self.lineEditLFRH = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditLFRH.setObjectName("lineEditLFRH")

        self.lineEditLFRL = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditLFRL.setObjectName("lineEditLFRL")

        self.lineEditLFS = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditLFS.setObjectName("lineEditLFS")
        
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
        self.buttonStartSearch.setText(_translate("MainWindow", "StartSearch"))
        self.buttonSave.setText(_translate("MainWindow", "Save"))
        self.actionopen.setText(_translate("MainWindow", "open"))
        self.actionsave.setText(_translate("MainWindow", "save"))
        self.actionsave_as.setText(_translate("MainWindow", "save as"))
