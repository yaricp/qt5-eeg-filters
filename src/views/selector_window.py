from loguru import logger
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
)


class SelectorWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    closed = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        _translate = QtCore.QCoreApplication.translate
        self.setObjectName("SelectorWindow")
        self.parent = parent
        start_size = 500, 500
        self.resize(*start_size)
        start_poz = (
            int(self.parent.x() + self.parent.width()/2 - self.width()/2),
            int(self.parent.y() + 100)
        )
        self.setGeometry(*start_poz, *start_size)
        self.setWindowTitle(_translate(
            "SelectorWindow", "EP Bandpass Filter Selector"
        ))
        self.destroyed.connect(self.parent.on_selector_window_destroy)

        self.graph = pg.GraphicsLayoutWidget()

        self.view_box = pg.ViewBox()

        self.plot = pg.PlotItem()
        self.plot.setLabel(axis='left', text='Y-axis')
        self.plot.setLabel(axis='bottom', text='X-axis')
        self.heatmap = pg.ImageView(view=self.plot)
        self.heat_vbox = self.heatmap.getView()

        self.layout = QVBoxLayout()
        self.label = QLabel("Selector Window")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.heatmap)
        self.setLayout(self.layout)

        self.buttonSave = QPushButton()
        self.buttonSave.setGeometry(
            self.parent.main_top_margin,
            self.parent.main_left_margin,
            self.parent.top_buttons_width,
            self.parent.top_buttons_height
        )
        self.buttonSave.setObjectName("buttonSave")
        self.buttonSave.setText(
            _translate("SelectorWindow", "Export data")
        )
        self.buttonSave.clicked.connect(self.save_event_handler)
        self.layout.addWidget(self.buttonSave)

    @pyqtSlot()
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def draw_heatmap(self, heatmap_data):
        """
        Draws heatmap of ep selector
        """
        logger.info("start draw_heatmap")
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

        self.heatmap.setImage(np.asarray(image_data))
        colors = [
            (0, 0, 0), (4, 5, 61), (84, 42, 55), (15, 87, 60),
            (208, 17, 141), (255, 255, 255)
        ]
        cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
        self.heatmap.setColorMap(cmap)

        found_bond = self.parent.main_window.model.ep_found_bandpass
        self.label.setText(f"Found filter: {str(found_bond)}")

        x_axis_labels = [list(
            zip(range(len(low_borders)), low_borders)
        )]
        y_axis_labels = [list(
            zip(range(len(high_borders)), high_borders)
        )]

        xax = self.plot.getAxis('bottom')
        xax.setTicks(x_axis_labels)
        yax = self.plot.getAxis('left')
        yax.setTicks(y_axis_labels)

        self.heatmap.move(
            self.buttonSave.x(),
            self.buttonSave.y() + self.buttonSave.height() + 10
        )

    def save_event_handler(self):
        """
        Handler for event save data of ep_bandpass_filter_selector
        """
        if not self.parent.main_window.config.target_dirpath:
            self.parent.main_window.config.target_dirpath = (
                self.parent.get_target_file_name()
            )
        if not self.parent.main_window.config.target_dirpath:
            return False
        self.parent.main_window.controller.ep_selector_export_data()
        return True
