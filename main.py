#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main file of QT GUI."""

import collections
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

from eeg_filters import upload as eeg_filters_upload
from eeg_filters.filters import make_filter, search_max_min
from eeg_filters.export import export_curves, export_extremums
from settings import *


class MainWindow(QMainWindow, ui.Ui_MainWindow):

    """Main windows of programm."""

    def __init__(self: dict) -> None:
        """initialization and prepare data."""
        super().__init__()
        self.setupUi(self)

        self.config = collections.namedtuple("Settings", [
            "time_measuring",
            "filter_order",
            "ripple",
            "max_start_search",
            "max_end_search",
            "min_start_search",
            "min_end_search",
            "bandwidths",
            "max_iter_value",
            "max_step_iter",
            "default_step_iter",
            "iter_value",
        ])

        self.settings = collections.namedtuple("Config", [
            "source_filepath",
            "target_dirpath",
            "dict_bandwidth_data",
            "dict_extremums_data",
            "dict_showed_extremums",
            "total_count",
            "fs",
            "list_times",
            "list_data",
            "tick_times",
        ])

        config = self.config
        config.time_measuring = 0  # TODO:  unused
        config.filter_order = FILTER_ORDER
        config.ripple = RIPPLE
        config.max_start_search = MAX_START_SEARCH
        config.max_end_search = MAX_END_SEARCH
        config.min_start_search = MIN_START_SEARCH
        config.min_end_search = MIN_END_SEARCH
        config.bandwidths = BANDWIDTHS
        config.max_iter_value = MAX_ITER_VALUE
        config.max_step_iter = MAX_STEP_ITER
        config.default_step_iter = DEFAULT_STEP_ITER
        config.iter_value = MAX_ITER_VALUE * DEFAULT_STEP_ITER / MAX_STEP_ITER

        settings = self.settings
        settings.source_filepath = ''
        settings.target_dirpath = ''
        settings.dict_bandwidth_data = {}
        settings.dict_extremums_data = {}
        settings.dict_showed_extremums = {}
        settings.total_count = 0
        settings.fs = None
        settings.list_times = []
        settings.list_data = []
        settings.tick_times = 0

        self.lineEditMaxStart.setText(str(self.config.max_start_search))
        self.lineEditMaxEnd.setText(str(self.config.max_end_search))
        self.lineEditMinStart.setText(str(self.config.min_start_search))
        self.lineEditMinEnd.setText(str(self.config.min_end_search))
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

        self.listBandwidths.addItems(
            ['%s' % b for b in self.config.bandwidths])
        self.listBandwidths.itemClicked.connect(self.bandwidths_activated)

        self.graph = pg.PlotWidget(self.widget)
        self.graph.setGeometry(QtCore.QRect(0, 0, 830, 475))
        self.graph.setBackground('w')

        self.range_search_maxmums = pg.LinearRegionItem(
            [self.config.max_start_search, self.config.max_end_search])
        self.range_search_maxmums.setBrush(
            QtGui.QBrush(QtGui.QColor(0, 0, 255, 50))
        )
        self.range_search_maxmums.sigRegionChangeFinished.connect(
            self.change_range_search_extremums
        )

        self.range_search_minimums = pg.LinearRegionItem(
            [self.config.min_start_search, self.config.min_end_search])
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

        self.buttonOpen.clicked.connect(self.show_dialog_open)
        self.buttonAdd.clicked.connect(self.add_new_bandwidth)
        self.buttonSave.clicked.connect(self.save_button_pressed)

        self.slider1.setMinimum(0)
        self.slider1.setMaximum(self.config.max_step_iter)
        self.slider1.setValue(self.config.default_step_iter)
        self.slider1.valueChanged.connect(self.change_value_slider)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_file_button)
        file_menu.addAction(save_file_button)
        file_menu.addAction(close_file_button)

    def __clear_extremums(self: dict) -> None:
        """ Clear dict of extremums."""

        self.settings.dict_extremums_data = {
            'max': {},
            'min': {}
        }

    def bandwidths_activated(self: dict, item: dict) -> bool:
        """handler change bandwidth.
        Returns - True if ok.
        """
        if item.text() == 'source' and not self.config.source_filepath:
            self.show_dialog_open()
            return True

        self.show_graphic_filtered()
        return True

    def show_graphic_filtered(self: dict) -> bool:
        """draw plot of filtered data.
        Returns - True if ok.
        """
        if self.settings.total_count == 0:
            return False

        index = self.listBandwidths.currentRow()
        bandwidth = self.config.bandwidths[index]
        self.dict_max_for_iter = {}
        if not '%s' % bandwidth in self.settings.dict_bandwidth_data.keys():
            self.calc_add_bandwidth(bandwidth)

        delta = 0
        dict_data = self.settings.dict_bandwidth_data['%s' % bandwidth]
        count = 0
        for row in dict_data.values():
            delta -= self.config.iter_value  # + last_max_value
            y = row + delta
            graph_item = self.graph.getPlotItem().dataItems[count]
            graph_item.setData(self.settings.tick_times,  y,)
            count += 1

        self.show_graphic_extremums()
        return True

    def show_graphic_extremums(self: dict) -> bool:
        """draw plot of extremums.
        Returns - True if ok.
        """
        if self.settings.total_count == 0:
            return False
        index = self.listBandwidths.currentRow()
        bandwidth = self.config.bandwidths[index]
        self.range_search_maxmums.setRegion([
            float(self.lineEditMaxStart.text()),
            float(self.lineEditMaxEnd.text())
        ])
        self.range_search_minimums.setRegion([
            float(self.lineEditMinStart.text()),
            float(self.lineEditMinEnd.text())
        ])
        if not '%s' % bandwidth in self.settings.dict_extremums_data:
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
        if self.settings.total_count == 0 or not self.settings.dict_showed_extremums:
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
        if self.settings.total_count == 0 or not self.settings.dict_showed_extremums:
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
        index = self.listBandwidths.currentRow()
        bandwidth = self.config.bandwidths[index]
        self.calc_add_extremums(bandwidth, ext)
        dict_data = self.settings.dict_extremums_data[ext]['%s' % bandwidth]
        showed_extremums = self.settings.dict_showed_extremums[ext]
        for time_stamp, row in dict_data.items():
            delta -= self.config.iter_value  # + last_max_value
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
        dict_data = self.settings.dict_bandwidth_data['%s' % bandwidth]
        dict_extremums = self.settings.dict_extremums_data[ext]
        dict_data_extremums = {}

        for time_stamp, row in dict_data.items():
            dict_data_extremums.update({
                time_stamp: search_max_min(
                    self.settings.tick_times,
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
        for key_curv, row in zip(self.settings.list_times, self.settings.list_data):
            filtred_data = make_filter(
                row,
                bandwidth,
                self.settings.fs,
                self.config.filter_order,
                self.config.ripple
            )
            dict_curves_filtred.update({key_curv: filtred_data})
        self.settings.dict_bandwidth_data.update({
            '%s' % bandwidth: dict_curves_filtred
        })
        return True

    def add_new_bandwidth(self: dict) -> None:
        """handler event pressed button add bandwidth."""
        text = self.lineEdit_3.text()
        self.listBandwidths.addItem(text)
        splitted_text = text.split(',')
        value = [
            int(splitted_text[0].replace('[', '')),
            int(splitted_text[1].replace(']', '').replace(' ', ''))
        ]
        self.config.bandwidths.append(value)
        self.lineEdit_3.clear()

    def change_value_slider(self: dict) -> bool:
        """Handler event change value slider.
        Returns - True if ok.
        """
        self.config.iter_value = (
            self.slider1.value()
            * self.config.max_iter_value
            / self.config.max_step_iter
        )
        QApplication.processEvents()
        self.show_graphic_filtered()
        return True

    def show_dialog_open(self: dict) -> bool:
        """Show dialog window.
        Returns - True if ok.
        """
        self.config.source_filepath = self.file_dialog_open.getOpenFileName(
            self,
            'Open source file',
            './')[0]
        if not self.config.source_filepath:
            return False
        item = self.listBandwidths.item(0)
        item.setSelected(True)
        self.listBandwidths.setCurrentItem(item)
        self.prepare_data()
        return True

    def prepare_data(self: dict) -> bool:
        """Prepare data and plot after load data.
        Returns - True if ok.
        """
        if not self.config.source_filepath:
            return False

        self.settings.dict_bandwidth_data = {}
        self.__clear_extremums()
        (
            self.settings.fs,
            self.settings.list_times,
            self.settings.tick_times,
            self.settings.list_data
        ) = eeg_filters_upload.prepare_data(self.config.source_filepath)
        self.settings.total_count = len(self.settings.list_times)
        if self.settings.total_count == 0:
            return False
        dict_curves_filtred = {}
        count = 0
        flag_new = False
        self.listBandwidths.setHidden(1)
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 1)
        pen2 = pg.mkPen(color=(255, 0, 0), width=15, style=QtCore.Qt.DashLine)
        if not self.graph.getPlotItem().dataItems:
            flag_new = True
        for time_stamp, row in zip(self.settings.list_times, self.settings.list_data):
            count += 1
            progress = count*50/self.settings.total_count
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
            for time_stamp in self.settings.list_times:
                count += 1
                progress = count*50/self.settings.total_count
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
            self.settings.dict_showed_extremums.update({
                'max': maximums,
                'min': minimums
            })
        self.settings.dict_bandwidth_data.update(
            {'source': dict_curves_filtred})
        self.show_graphic_filtered()
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 0)
        self.listBandwidths.setHidden(0)

        return True

    def save_button_pressed(self: dict) -> bool:
        """handler event save button pressed.
        Returns - True if ok.
        """
        if not self.settings.target_dirpath:
            self.settings.target_dirpath = self.file_dialog_save.getExistingDirectory(
                self,
                'Save filtered data',
                './')
        if not self.settings.target_dirpath:
            return False
        QApplication.processEvents()
        self.export_data()
        return True

    def export_data(self: dict) -> None:
        """Export curves and extremums in files.
        Returns - None.
        """

        value = self.settings.dict_bandwidth_data[self.config.bandwidths[0]]
        rows = value[self.settings.list_times[0]]
        count_rows = len(rows)
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 1)
        self.listBandwidths.setHidden(1)
        count = 0
        total_count = len(self.config.bandwidths)
        for bandwidth, dict_data in self.settings.dict_bandwidth_data.items():
            if bandwidth != 'source':
                count += 1
                progress = count*100/total_count
                self.progressBar.setValue(progress)
                QApplication.processEvents()
                export_curves(
                    self.config.source_filepath,
                    self.settings.target_dirpath,
                    bandwidth,
                    dict_data,
                    count_rows=count_rows
                )
                dict_extremums_export = {}
                for (key_max, row_max), (key_min, row_min) in zip(
                    self.settings.dict_extremums_data['max'][bandwidth].items(
                    ),
                    self.settings.dict_extremums_data['min'][bandwidth].items()
                ):
                    if key_max != key_min:
                        print('key_max: ', key_max)
                        print('key_min: ', key_min)
                    dict_extremums_export.update({
                        key_max: (row_max, row_min)})

                export_extremums(
                    self.settings.target_dirpath,
                    bandwidth,
                    dict_extremums_export
                )
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 0)
        self.listBandwidths.setHidden(0)

    def close_button_pressed(self: dict) -> None:
        """Handler event pressed close button.
        Returns: None.
        """
        if self.settings.dict_bandwidth_data:
            self.save_button_pressed()
        QApplication.quit()


if __name__ == '__main__':
    from sys import argv, exit
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    exit(app.exec_())
