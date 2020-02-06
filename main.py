#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main file of QT GUI."""

import pyqtgraph as pg

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
                            QMainWindow,
                            QAction,
                            QFileDialog,
                            QApplication
                            )

import ui

from eeg_filters.upload import prepare_data
from eeg_filters.filters import make_filter, search_max_min
from eeg_filters.export import export_curves, export_extremums
from settings import *


class MainWindow(QMainWindow, ui.Ui_MainWindow):

    """Main windows of programm."""

    def __init__(self: dict) -> None:
        """initialization and prepare data."""
        super().__init__()
        self.setupUi(self)

        self.time_measuring = 0
        self.order = ORDER
        self.rp = RP
        self.max_start_search = MAX_START_SEARCH
        self.max_end_search = MAX_END_SEARCH
        self.min_start_search = MIN_START_SEARCH
        self.min_end_search = MIN_END_SEARCH
        self.bandwidths = BANDWIDTHS
        self.max_iter_value = MAX_ITER_VALUE
        self.max_step_iter = MAX_STEP_ITER
        self.default_step_iter = DEFAULT_STEP_ITER
        self.iter_value = (
                            MAX_ITER_VALUE
                            * DEFAULT_STEP_ITER
                            / MAX_STEP_ITER
                            )

        self.source_filepath = ''
        self.target_dirpath = ''
        self.dict_bandwidth_data = {}
        self.dict_extremums_data = {}
        self.dict_showed_extremums = {}
        self.total_count = 0
        self.fs = None
        self.list_times = []
        self.list_data = []
        self.tick_times = 0

        self.lineEditMaxStart.setText(str(self.max_start_search))
        self.lineEditMaxEnd.setText(str(self.max_end_search))
        self.lineEditMinStart.setText(str(self.min_start_search))
        self.lineEditMinEnd.setText(str(self.min_end_search))
        self.lineEditMaxStart.returnPressed.connect(
                self.change_text_line_extremums_edits
                )
        self.lineEditMaxEnd.returnPressed.connect(
                self.change_text_line_extremums_edits
                )
        self.lineEditMinStart.returnPressed.connect(
                self.change_text_line_extremums_edits
                )
        self.lineEditMinEnd.returnPressed.connect(
                self.change_text_line_extremums_edits
                )

        self.progressBar.setMaximum(100)

        self.listWidget.addItems(['%s' % b for b in self.bandwidths])
        self.listWidget.itemClicked.connect(self.list_item_activated)

        self.graph = pg.PlotWidget(self.widget)
        self.graph.setGeometry(QtCore.QRect(0, 0, 830, 475))
        self.graph.setBackground('w')

        self.range_search_maxmums = pg.LinearRegionItem(
                [self.max_start_search, self.max_end_search])
        self.range_search_maxmums.setBrush(
                QtGui.QBrush(QtGui.QColor(0, 0, 255, 50))
                )
        self.range_search_maxmums.sigRegionChangeFinished.connect(
                self.change_range_search_extremums
                )

        self.range_search_minimums = pg.LinearRegionItem(
                [self.min_start_search, self.min_end_search])
        self.range_search_minimums.setBrush(
                QtGui.QBrush(QtGui.QColor(0, 0, 50, 50))
                )
        self.range_search_minimums.sigRegionChangeFinished.connect(
                self.change_range_search_extremums
                )

        open_file_button = QAction(QIcon('open.png'), 'Open', self)
        open_file_button.setShortcut('Ctrl+O')
        open_file_button.setStatusTip('Open Source File')
        open_file_button.triggered.connect(self.show_dialog_open)

        save_file_button = QAction(QIcon('save.png'), 'Save', self)
        save_file_button.setShortcut('Ctrl+S')
        save_file_button.setStatusTip('Save Filtered Data')
        save_file_button.triggered.connect(self.save_button_pressed)

        close_file_button = QAction(QIcon('close.png'), 'Close', self)
        close_file_button.setShortcut('Ctrl+X')
        close_file_button.setStatusTip('Close')
        close_file_button.triggered.connect(self.close_button_pressed)

        self.file_dialog_open = QFileDialog()
        self.file_dialog_open.setFileMode(0)
        self.file_dialog_save = QFileDialog()
        self.file_dialog_save.setFileMode(4)

        self.pushButton.clicked.connect(self.show_dialog_open)
        self.pushButton_3.clicked.connect(self.add_new_bandwidth)
        self.pushButton_4.clicked.connect(self.save_button_pressed)

        self.slider1.setMinimum(0)
        self.slider1.setMaximum(self.max_step_iter)
        self.slider1.setValue(self.default_step_iter)
        self.slider1.valueChanged.connect(self.change_value_slider)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_file_button)
        file_menu.addAction(save_file_button)
        file_menu.addAction(close_file_button)

    def __clear_extremums(self: dict) -> None:
        """ Clear dict of extremums."""

        self.dict_extremums_data = {
            'max': {},
            'min': {}
            }

    def list_item_activated(self: dict, item: dict) -> bool:
        """handler change bandwidth.
        Returns - True if ok.
        """
        if item.text() == 'source' and not self.source_filepath:
            self.show_dialog_open()
            return True
        self.show_graphic_filtered()
        return True

    def show_graphic_filtered(self: dict) -> bool:
        """draw plot of filtered data.
        Returns - True if ok.
        """
        if self.total_count == 0:
            return False
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        self.dict_max_for_iter = {}
        if not '%s' % bandwidth in self.dict_bandwidth_data.keys():
            self.calc_add_bandwidth(bandwidth)
        delta = 0
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        count = 0
        for row in dict_data.values():
            delta -= self.iter_value  # + last_max_value
            y = row + delta
            graph_item = self.graph.getPlotItem().dataItems[count]
            graph_item.setData(self.tick_times,  y,)
            count += 1
        self.show_graphic_extremums()
        return True

    def show_graphic_extremums(self: dict) -> bool:
        """draw plot of extremums.
        Returns - True if ok.
        """
        if self.total_count == 0:
            return False
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        self.range_search_maxmums.setRegion([
                float(self.lineEditMaxStart.text()),
                float(self.lineEditMaxEnd.text())
                ])
        self.range_search_minimums.setRegion([
                float(self.lineEditMinStart.text()),
                float(self.lineEditMinEnd.text())
                ])
        if not '%s' % bandwidth in self.dict_extremums_data:
            self.calc_add_extremums(bandwidth, 'max')
            self.calc_add_extremums(bandwidth, 'min')
        self.graph.addItem(self.range_search_maxmums)
        self.reshow_extremums('max')
        self.graph.addItem(self.range_search_minimums)
        self.reshow_extremums('min')
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 0)
        return True

    def change_text_line_extremums_edits(self: dict) -> bool:
        """
        Handler event change text search extremums.

        Returns - True if ok.

        """
        if self.total_count == 0 or not self.dict_showed_extremums:
            return False
        self.range_search_maxmums.setRegion([
                float(self.lineEditMaxStart.text()),
                float(self.lineEditMaxEnd.text())
                ])
        self.reshow_extremums('max')
        self.range_search_minimums.setRegion([
                float(self.lineEditMinStart.text()),
                float(self.lineEditMinEnd.text())
                ])
        self.reshow_extremums('min')
        return True

    def change_range_search_extremums(self: dict) -> bool:
        """
        Handler event change region search extremums.

        Returns - True if ok.

        """
        if self.total_count == 0 or not self.dict_showed_extremums:
            return False
        self.lineEditMaxStart.setText(
                str(round(self.range_search_maxmums.getRegion()[0], 5))
                )
        self.lineEditMaxEnd.setText(
                str(round(self.range_search_maxmums.getRegion()[1], 5)))
        self.reshow_extremums('max')
        self.lineEditMinStart.setText(
                str(round(self.range_search_minimums.getRegion()[0], 5))
                )
        self.lineEditMinEnd.setText(
                str(round(self.range_search_minimums.getRegion()[1], 5)))
        self.reshow_extremums('min')
        return True

    def reshow_extremums(self: dict, ext: str) -> bool:
        """draw plot of extremums.
        Returns - True if ok.
        """
        delta = 0
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        self.calc_add_extremums(bandwidth, ext)
        dict_data = self.dict_extremums_data[ext]['%s' % bandwidth]
        showed_extremums = self.dict_showed_extremums[ext]
        for time_stamp, row in dict_data.items():
            delta -= self.iter_value  # + last_max_value
            time_extremum = row[0]
            value_extremum = row[1] + delta
            showed_extremum = showed_extremums[time_stamp]
            showed_extremum.setData([time_extremum, ], [value_extremum, ])
            showed_extremums.update({ext: {time_stamp: showed_extremum}})
        return True

    def calc_add_extremums(
                            self: dict,
                            bandwidth: list,
                            ext: str
                            ) -> bool:
        """Calculate extremums on curvey.
        Returns - True if ok.
        """
        range_search = self.range_search_maxmums
        if ext == 'min':
            range_search = self.range_search_minimums
        where_find = range_search.getRegion()
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        dict_extremums = self.dict_extremums_data[ext]
        dict_data_extremums = {}

        for time_stamp, row in dict_data.items():

            dict_data_extremums.update({
                time_stamp: search_max_min(
                        self.tick_times,
                        row,
                        where_find,
                        ext
                        )
                })
        dict_extremums.update({'%s' % bandwidth: dict_data_extremums})
        return True

    def calc_add_bandwidth(self: dict, bandwidth: list) -> bool:
        """Make filter of curves.
        Returns - True if ok.
        """
        dict_curves_filtred = {}
        for key_curv, row in zip(self.list_times, self.list_data):
            filtred_data = make_filter(
                                row,
                                bandwidth,
                                self.fs,
                                self.order,
                                self.rp
                                )
            dict_curves_filtred.update({key_curv: filtred_data})
        self.dict_bandwidth_data.update({
                '%s' % bandwidth: dict_curves_filtred
                })
        return True

    def add_new_bandwidth(self: dict) -> None:
        """handler event pressed button add bandwidth."""
        text = self.lineEdit_3.text()
        self.listWidget.addItem(text)
        splitted_text = text.split(',')
        value = [
                int(splitted_text[0].replace('[', '')),
                int(splitted_text[1].replace(']', '').replace(' ', ''))
                ]
        self.bandwidths.append(value)
        self.lineEdit_3.clear()

    def change_value_slider(self: dict) -> bool:
        """Handler event change value slider.
        Returns - True if ok.
        """
        self.iter_value = (
                self.slider1.value()
                * self.max_iter_value
                / self.max_step_iter
                )
        QApplication.processEvents()
        self.show_graphic_filtered()
        return True

    def show_dialog_open(self: dict) -> bool:
        """Show dialog window.
        Returns - True if ok.
        """
        self.source_filepath = self.file_dialog_open.getOpenFileName(
                                                    self,
                                                    'Open source file',
                                                    './')[0]
        if not self.source_filepath:
            return False
        item = self.listWidget.item(0)
        item.setSelected(True)
        self.listWidget.setCurrentItem(item)
        self.prepare_data()
        return True

    def prepare_data(self: dict) -> bool:
        """Prepare data and plot after load data.
        Returns - True if ok.
        """
        if not self.source_filepath:
            return False
        self.dict_bandwidth_data = {}
        self.__clear_extremums()
        (
            self.fs,
            self.list_times,
            self.tick_times,
            self.list_data
        ) = prepare_data(self.source_filepath)
        self.total_count = len(self.list_times)
        if self.total_count == 0:
            return False
        dict_curves_filtred = {}
        count = 0
        flag_new = False
        self.listWidget.setHidden(1)
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 1)
        pen2 = pg.mkPen(color=(255, 0, 0), width=15, style=QtCore.Qt.DashLine)
        if not self.graph.getPlotItem().dataItems:
            flag_new = True
        for time_stamp, row in zip(self.list_times, self.list_data):
            count += 1
            progress = count*50/self.total_count
            self.progressBar.setValue(progress)
            QApplication.processEvents()
            dict_curves_filtred.update({time_stamp: row})
            #  prepare graph
            if flag_new:
                self.graph.plot(
                        name=time_stamp
                        )
        if flag_new:
            maximums = {}
            minimums = {}
            for time_stamp in self.list_times:
                count += 1
                progress = count*50/self.total_count
                self.progressBar.setValue(progress)
                QApplication.processEvents()
                showed_max = self.graph.plot(
                        [0, 0],
                        [0, 0],
                        name='max_%s' % time_stamp,
                        symbol='o',
                        pen=pen2,
                        symbolSize=5,
                        symbolBrush=('r')
                        )
                showed_min = self.graph.plot(
                        [0, 0],
                        [0, 0],
                        name='min_%s' % time_stamp,
                        symbol='o',
                        pen=pen2,
                        symbolSize=5,
                        symbolBrush=('b')
                        )
                maximums.update({time_stamp: showed_max})
                minimums.update({time_stamp: showed_min})
            self.dict_showed_extremums.update({
                            'max': maximums,
                            'min': minimums
                        })
        self.dict_bandwidth_data.update({'source': dict_curves_filtred})
        self.show_graphic_filtered()
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 0)
        self.listWidget.setHidden(0)

        return True

    def save_button_pressed(self: dict) -> bool:
        """handler event save button pressed.
        Returns - True if ok.
        """
        if not self.target_dirpath:
            self.target_dirpath = self.file_dialog_save.getExistingDirectory(
                                    self,
                                    'Save filtered data',
                                    './')
        if not self.target_dirpath:
            return False
        QApplication.processEvents()
        self.export_data()
        return True

    def export_data(self: dict) -> None:
        """Export curves and extremums in files.
        Returns - None.
        """

        value = self.dict_bandwidth_data[self.bandwidths[0]]
        rows = value[self.list_times[0]]
        count_rows = len(rows)
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 1)
        self.listWidget.setHidden(1)
        count = 0
        total_count = len(self.bandwidths)
        for bandwidth, dict_data in self.dict_bandwidth_data.items():
            if bandwidth != 'source':
                count += 1
                progress = count*100/total_count
                self.progressBar.setValue(progress)
                QApplication.processEvents()
                export_curves(
                    self.source_filepath,
                    self.target_dirpath,
                    bandwidth,
                    dict_data,
                    count_rows=count_rows
                    )
                dict_extremums_export = {}
                for (key_max, row_max), (key_min, row_min) in zip(
                    self.dict_extremums_data['max'][bandwidth].items(),
                    self.dict_extremums_data['min'][bandwidth].items()
                            ):
                    if key_max != key_min:
                        print('key_max: ', key_max)
                        print('key_min: ', key_min)
                    dict_extremums_export.update({
                        key_max: (row_max, row_min)})

                export_extremums(
                        self.target_dirpath,
                        bandwidth,
                        dict_extremums_export
                        )
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 0)
        self.listWidget.setHidden(0)

    def close_button_pressed(self: dict) -> None:
        """Handler event pressed close button.
        Returns: None.
        """
        if self.dict_bandwidth_data:
            self.save_button_pressed()
        QApplication.quit()


if __name__ == '__main__':
    from sys import argv, exit
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    exit(app.exec_())
