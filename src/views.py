import numpy as np
from functools import partial
# from loguru import logger
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Slot, Signal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QMainWindow,
    QApplication,
    QAction,
    QFileDialog,
    QLineEdit,
    QCheckBox,
    QPushButton
)

import ui
from qt5_waiting_spinner import QtWaitingSpinner


pg.setConfigOptions(antialias=True)
pen2 = pg.mkPen(color=(255, 0, 0), width=15, style=QtCore.Qt.DashLine)


class ViewGraph(QMainWindow, ui.Ui_MainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self, config, main=None) -> None:

        super().__init__()
        self.setupUi(self)

        self.main_window = main
        self.selector_window = None
        self.iter_value = config.iter_value
        self.max_start_search = config.max_start_search
        self.max_end_search = config.max_end_search
        self.min_start_search = config.min_start_search
        self.min_end_search = config.min_end_search
        self.max_step_iter = config.max_step_iter
        self.default_step_iter = config.default_step_iter
        self.bandwidths = config.bandwidths
        self.lineEditMaxStart.setText(str(self.max_start_search))
        self.lineEditMaxEnd.setText(str(self.max_end_search))
        self.lineEditMinStart.setText(str(self.min_start_search))
        self.lineEditMinEnd.setText(str(self.min_end_search))
        self.edit_max_start_changed_event = self.lineEditMaxStart.returnPressed
        self.edit_max_end_changed_event = self.lineEditMaxEnd.returnPressed
        self.edit_min_start_changed_event = self.lineEditMinStart.returnPressed
        self.edit_min_end_changed_event = self.lineEditMinEnd.returnPressed
        self.count_checkboxes = 0

        self.spinner = QtWaitingSpinner(self, False, False)
        self.spinner.setLineLength(2 / 6 * self.top_buttons_height)
        self.spinner.setInnerRadius(1 / 6 * self.top_buttons_height)
        self.spinner.start()
        self.spinner.hide()


        self.progressBar.setMaximum(100)
        self.listBandwidths.addItems(
            ['%s' % b for b in self.bandwidths]
        )
        
        self.bandwidths_clicked_event = self.listBandwidths.itemClicked
        self.range_search_maxmums = pg.LinearRegionItem(
            [self.max_start_search, self.max_end_search]
        )
        self.range_search_maxmums.setBrush(
            QtGui.QBrush(QtGui.QColor(0, 0, 255, 50))
        )
        self.maximums_region_changed_event = self.range_search_maxmums.sigRegionChangeFinished

        self.range_search_minimums = pg.LinearRegionItem(
            [self.min_start_search, self.min_end_search]
        )
        self.range_search_minimums.setBrush(
            QtGui.QBrush(QtGui.QColor(0, 0, 50, 50))
        )
        self.minimums_region_changed_event = self.range_search_minimums.sigRegionChangeFinished

        open_file_button = QAction(QIcon('open.png'), 'Open', self)
        open_file_button.setShortcut('Ctrl+O')
        open_file_button.setStatusTip('Open Source File')
        self.menu_open_file_event = open_file_button.triggered

        save_file_button = QAction(QIcon('save.png'), 'Save', self)
        save_file_button.setShortcut('Ctrl+S')
        save_file_button.setStatusTip('Save Filtered Data')
        self.menu_save_file_event = save_file_button.triggered

        close_file_button = QAction(QIcon('close.png'), 'Close', self)
        close_file_button.setShortcut('Ctrl+X')
        close_file_button.setStatusTip('Close')
        self.menu_close_file_event = close_file_button.triggered

        self.file_dialog_open = QFileDialog()
        self.file_dialog_open.setFileMode(0)
        self.file_dialog_save = QFileDialog()
        self.file_dialog_save.setFileMode(4)

        self.selected_item = QtGui.QBrush(QtGui.QColor(0, 0, 255, 50))

        self.open_clicked_event = self.buttonOpen.clicked
        self.add_clicked_event = self.buttonAdd.clicked
        self.save_clicked_event = self.buttonSave.clicked
        self.toggle_visible_regions_event = self.buttonVisibleRegion.clicked
        self.start_ep_passband_search_event = self.buttonStartSearch.clicked

        self.slider1.setMinimum(0)
        self.slider1.setMaximum(self.max_step_iter)
        self.slider1.setValue(self.default_step_iter)
        self.value_changed_event = self.slider1.valueChanged

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_file_button)
        file_menu.addAction(save_file_button)
        file_menu.addAction(close_file_button)

        self.lineEditHFRH.setText(str(config.hfrh))
        self.lineEditHFRL.setText(str(config.hfrl))
        self.lineEditHFS.setText(str(config.hfs))
        self.lineEditLFRL.setText(str(config.lfrl))
        self.lineEditLFRH.setText(str(config.lfrh))
        self.lineEditLFS.setText(str(config.lfs))

    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(ViewGraph, self).resizeEvent(event)

    def create_selector_window(self):
        """
        Creates a new window for results of EP Bandpass filter selector.
        """

        self.selector_window = SelectorWindow(self)
        self.selector_window.closed.connect(
            self.on_selector_window_destroy
        )

    def on_selector_window_destroy(self):
        """
        Sets Enabled to True when selector windows closed.
        """
        self.setEnabled(True)

    def show_graphic_filtered(
            self,
            dict_data,
            showed_maxs,
            showed_mins,
            tick_times,
            total_count
    ) -> bool:
        """
        Draw plot of filtered data.
        Returns - True if ok.
        """
        if total_count == 0:
            return False

        delta = 0
        count = 0
        for time_stamp, row in dict_data.items():
            delta -= self.iter_value  # + last_max_value
            y = row + delta
            graph_item = self.graph.getPlotItem().dataItems[count]
            # just set curves for draggable points for move it this curve
            showed_maxs[time_stamp].set_curve(tick_times, y)
            showed_mins[time_stamp].set_curve(tick_times, y)
            graph_item.setData(tick_times,  y,)
            count += 1

        return True

    def show_range_extremums(self, total_count) -> bool:
        """
        Draw regions where will search maximums and minimums of curves.
        Returns - True if ok.
        """
        # logger.debug("start show graph extrem")
        if total_count == 0:
            return False
        self.range_search_maxmums.setRegion([
            float(self.lineEditMaxStart.text()),
            float(self.lineEditMaxEnd.text())
        ])
        self.range_search_minimums.setRegion([
            float(self.lineEditMinStart.text()),
            float(self.lineEditMinEnd.text())
        ])

        return True

    def reshow_extremums(
            self,
            dict_data,
            showed_extremums,
            params
    ) -> bool:
        """
        Draw point of maximums and minimums of curves in showed regions.
        Returns - True if ok.
        """
        delta = 0
        for time_stamp, row in dict_data.items():
            delta -= self.iter_value  # + last_max_value
            time_extremum = row[0]
            value_extremum = row[1] + delta
            showed_extremum = showed_extremums[time_stamp]
            # set model for save value of point when user change it manually
            showed_extremum.model_params = params + (time_stamp,)
            showed_extremum.setData(
                pos=np.array([[time_extremum, value_extremum]])
                )

        return True

    def show_progress_bar(self):
        """Show progress bar and hide section of bandwidths."""
        self.listBandwidths.setHidden(1)
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 1)

    def hide_progress_bar(self):
        """Hide progress bar and show section of bandwidths."""
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 0)
        self.listBandwidths.setHidden(0)

    def is_graph_empty(self):
        """Check is Graph empty."""
        if not self.graph.getPlotItem().dataItems:
            return True
        return False

    def set_progress_value(self, value):
        """Set value of progress of process."""
        self.progressBar.setValue(value)
        QApplication.processEvents()

    def add_ranges_extremums(self):
        """Add regions for search extremums."""
        self.graph.addItem(self.range_search_maxmums)
        self.graph.addItem(self.range_search_minimums)
        pass

    def create_graph(self, time_stamp):
        """Create new plot for new curve."""
        plot = self.graph.plot(
            name=time_stamp, clickable=True
        )
        plot.sigClicked.connect(
            self.plot_clicked
        )

    def plot_clicked(self) -> None:
        """

        """
        print("Curve Clicked!!!")

    def add_checkbox(self, number: int, datetime: str) -> None:
        """
        Adds checkbox for change curve.
        """
        check_box = QCheckBox(
            "ckbx"+str(self.count_checkboxes),
            self.centralwidget
        )
        check_box.setObjectName(
            "ckbx"+str(self.count_checkboxes)
        )
        check_box_pos = (
            self.main_left_margin,
            (
                self.main_top_margin
                + self.top_buttons_height
                + 5
                + self.count_checkboxes * 12
            )
        )
        check_box_size = (
            self.left_checkboxes_width,
            self.left_checkboxes_height
        )
        check_box.setGeometry(
            *check_box_pos, *check_box_size
        )
        check_box.setText(datetime)
        check_box.stateChanged.connect(
            partial(
                self.main_window.handler.curve_clicked,
                check_box
            )
        )
        check_box.show()
        self.main_window.model.check_box_list.append(check_box)
        self.count_checkboxes += 1

    def get_ranges_extremums(self):
        """Get values of bounds of regions for search extremums."""
        max_search_range = [round(x, 4) for x in self.range_search_maxmums.getRegion()]
        min_search_range = [round(x, 4) for x in self.range_search_minimums.getRegion()]
        return max_search_range, min_search_range

    def add_point_extremums(self, time_stamp):
        """Add new draggable points to the main graph."""

        from points import DraggablePoint

        showed_max = DraggablePoint()
        showed_max.controller = self.main_window.controller
        showed_max.setData(
            pos=np.array([[0, 0]]),
            name='max_%s' % time_stamp,
            symbol='o',
            pen=pen2,
            symbolSize=10,
            symbolBrush='r'
        )
        self.graph.addItem(showed_max)

        showed_min = DraggablePoint()
        showed_min.controller = self.main_window.controller
        showed_min.setData(
            pos=np.array([[0, 0]]),
            name='max_%s' % time_stamp,
            symbol='o',
            pen=pen2,
            symbolSize=1,
            symbolBrush='b'
        )
        self.graph.addItem(showed_min)

        return showed_max, showed_min

    def get_source_file_name(self):
        """Get name of source file."""
        return self.file_dialog_open.getOpenFileName(
            self,
            'Open source file',
            './')[0]

    def get_target_file_name(self):
        """Get name of target file."""
        return self.file_dialog_save.getExistingDirectory(
            self,
            'Save filtered data',
            './')

    @Slot()
    def get_selector_result(self):
        """
        Gets result and show new window with graph.
        """
        bandpass = self.main_window.model.ep_found_bandpass
        heatmap = self.main_window.model.ep_heatmap
        print("bandpass: ", bandpass)
        index_item = 0
        for item in self.bandwidths:
            print("item: ", item)
            if list(bandpass) == item:
                print("index_item: ", index_item)
                self.listBandwidths.item(index_item).setBackground(
                    self.selected_item
                )
                break
            index_item += 1
        self.spinner.hide()
        self.create_selector_window()
        self.selector_window.draw_heatmap(heatmap)
        self.selector_window.show()


class SelectorWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    closed = Signal()

    def __init__(self, parent):
        super().__init__()
        _translate = QtCore.QCoreApplication.translate
        self.setObjectName("SelectorWindow")
        self.parent = parent
        start_size = 400, 400
        self.resize(*start_size)
        start_poz = (
            self.parent.x() + self.parent.width()/2 - self.width()/2,
            self.parent.y() + self.parent.height()/2 - self.height()/2
        )
        self.setGeometry(*start_poz, *start_size)
        self.setWindowTitle(_translate(
            "SelectorWindow", "EP Bandpass Filter Selector"
        ))
        self.destroyed.connect(self.parent.on_selector_window_destroy)

        self.layout = QVBoxLayout()
        self.label = QLabel("Selector Window")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.buttonSave = QPushButton(self)
        self.buttonSave.setGeometry(
            self.parent.main_top_margin,
            self.parent.main_left_margin,
            self.parent.top_buttons_width * 2,
            self.parent.top_buttons_height
        )
        self.buttonSave.setObjectName("buttonSave")
        self.buttonSave.setText(
            _translate("SelectorWindow", "Export data")
        )
        self.buttonSave.clicked.connect(self.save_event_handler)
    
    @Slot()
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def draw_heatmap(self, heatmap_data):
        """
        Draws heatmap of ep selector
        """
        prev_data = []
        image_data = []
        low_borders = []
        min_value = 0
        max_value = 0
        high_borders = heatmap_data[0][1:]
        for row in heatmap_data[1:]:
            low_borders.append(row[0])
            min_value = min(min_value, min(row[1:]))
            max_value = max(max_value, max(row[1:]))
            prev_data.append(row[1:])

        delta = max_value - min_value
        print("prev_data:", prev_data)
        for row in prev_data:
            image_row = []
            for value in row:
                image_row.append(
                    (delta - (value - min_value)) / delta
                )
            image_data.append(np.asarray(image_row))

        graphWidget = pg.ImageView()
    
        graphWidget.setImage(np.asarray(image_data))
        colors = [
            (0, 0, 0),(4, 5, 61),(84, 42, 55),(15, 87, 60),
            (208, 17, 141),(255, 255, 255)
        ]
        cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
        graphWidget.setColorMap(cmap)
    
        self.layout.addWidget(graphWidget)

    def save_event_handler(self):
        """
        Handler for event save data of ep_bandpass_filter_selector
        """
        if not self.parent.main_window.config.target_dirpath:
            self.parent.main_window.config.target_dirpath = self.parent.get_target_file_name()
        if not self.parent.main_window.config.target_dirpath:
            return False
        self.parent.main_window.controller.ep_selector_export_data()
        return True