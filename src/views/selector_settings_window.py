from loguru import logger

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit
)


class SelectorSettingsWindow(QWidget):
    """
    Window with EP Selector settings
    """
    closed = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        _translate = QtCore.QCoreApplication.translate
        self.setObjectName("EPSettingsWindow")
        self.parent = parent

        self.combo_box1_options = list(
            self.parent.main_window.model.p2p_coeff_variants
        )
        self.p2p_coeff_variant = (
            self.parent.main_window.model.p2p_coeff_variant
        )
        index_combo_box1_default = self.combo_box1_options.index(
            self.parent.main_window.model.p2p_coeff_variant
        )
        self.curve_var_variant = (
            self.parent.main_window.model.cur_var_coeff_variant
        )
        self.combo_box2_options = list(
            self.parent.main_window.model.cur_var_coeff_variants
        )
        index_combo_box2_default = self.combo_box2_options.index(
            self.parent.main_window.model.cur_var_coeff_variant
        )

        start_size = 400, 400
        self.resize(*start_size)
        start_poz = (
            int(self.parent.x() + self.parent.width()/2 - self.width()/2),
            int(self.parent.y() + 100)
        )
        self.setGeometry(*start_poz, *start_size)
        self.setWindowTitle(_translate(
            "SelectorSettingsWindow", "EP Settings"
        ))
        self.destroyed.connect(
            self.parent.on_selector_window_destroy
        )

        self.centralwidget = QWidget(self)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")

        self.labelLFRL = QLabel(self.centralwidget)
        self.labelLFRL.setText("LFRL")
        labelLFRL_geo = (
            10, 10, 200, 20
        )
        self.labelLFRL.setGeometry(*labelLFRL_geo)

        self.lineEditLFRL = QLineEdit(self.centralwidget)
        self.lineEditLFRL.setObjectName("lineEditLFRL")
        self.lineEditLFRL.setText(
            str(self.parent.main_window.model.lfrl)
        )
        lineEditLFRL_geo = (
            205, 10, 100, 20
        )
        self.lineEditLFRL.setGeometry(*lineEditLFRL_geo)

        self.labelLFRH = QLabel(self.centralwidget)
        self.labelLFRH.setText("LFRH")
        labelLFRH_geo = (
            10, lineEditLFRL_geo[1] + lineEditLFRL_geo[3] + 10,
            200, 20
        )
        self.labelLFRH.setGeometry(*labelLFRH_geo)

        self.lineEditLFRH = QLineEdit(self.centralwidget)
        self.lineEditLFRH.setObjectName("lineEditLFRH")
        self.lineEditLFRH.setText(
            str(self.parent.main_window.model.lfrh)
        )
        lineEditLFRH_geo = (
            205, lineEditLFRL_geo[1] + lineEditLFRL_geo[3] + 10,
            100, 20
        )
        self.lineEditLFRH.setGeometry(*lineEditLFRH_geo)

        self.labelLFS = QLabel(self.centralwidget)
        self.labelLFS.setText("LFS")
        labelLFS_geo = (
            10, lineEditLFRH_geo[1] + lineEditLFRH_geo[3] + 10,
            200, 20
        )
        self.labelLFS.setGeometry(*labelLFS_geo)

        self.lineEditLFS = QLineEdit(self.centralwidget)
        self.lineEditLFS.setObjectName("lineEditLFS")
        self.lineEditLFS.setText(
            str(self.parent.main_window.model.lfs)
        )
        lineEditLFS_geo = (
            205, lineEditLFRH_geo[1] + lineEditLFRH_geo[3] + 10,
            100, 20
        )
        self.lineEditLFS.setGeometry(*lineEditLFS_geo)

        self.labelHFRL = QLabel(self.centralwidget)
        self.labelHFRL.setText("HFRL")
        labelHFRL_geo = (
            10, lineEditLFS_geo[1] + lineEditLFS_geo[3] + 10,
            200, 20
        )
        self.labelHFRL.setGeometry(*labelHFRL_geo)

        self.lineEditHFRL = QLineEdit(self.centralwidget)
        self.lineEditHFRL.setObjectName("lineEditHFRL")
        self.lineEditHFRL.setText(
            str(self.parent.main_window.model.hfrl)
        )
        lineEditHFRL_geo = (
            205, lineEditLFS_geo[1] + lineEditLFS_geo[3] + 10,
            100, 20
        )
        self.lineEditHFRL.setGeometry(*lineEditHFRL_geo)

        self.labelHFRH = QLabel(self.centralwidget)
        self.labelHFRH.setText("HFRH")
        labelHFRH_geo = (
            10, lineEditHFRL_geo[1] + lineEditHFRL_geo[3] + 10,
            200, 20
        )
        self.labelHFRH.setGeometry(*labelHFRH_geo)

        self.lineEditHFRH = QLineEdit(self.centralwidget)
        self.lineEditHFRH.setObjectName("lineEditHFRH")
        self.lineEditHFRH.setText(
            str(self.parent.main_window.model.hfrh)
        )
        lineEditLFRL_geo = (
            205, lineEditHFRL_geo[1] + lineEditHFRL_geo[3] + 10,
            100, 20
        )
        self.lineEditHFRH.setGeometry(*lineEditLFRL_geo)

        self.labelHFS = QLabel(self.centralwidget)
        self.labelHFS.setText("HFS")
        labelHFS_geo = (
            10, lineEditLFRL_geo[1] + lineEditLFRL_geo[3] + 10,
            200, 20
        )
        self.labelHFS.setGeometry(*labelHFS_geo)

        self.lineEditHFS = QLineEdit(self.centralwidget)
        self.lineEditHFS.setObjectName("lineEditHFS")
        self.lineEditHFS.setText(
            str(self.parent.main_window.model.hfs)
        )
        lineEditHFS_geo = (
            205, lineEditLFRL_geo[1] + lineEditLFRL_geo[3] + 10,
            100, 20
        )
        self.lineEditHFS.setGeometry(*lineEditHFS_geo)

        self.label_combo_box1 = QLabel(self.centralwidget)
        self.label_combo_box1.setText("P2P Coeff Variant")
        label_combo_box1_geo = (
            10, lineEditHFS_geo[1] + lineEditHFS_geo[3] + 10,
            200, 20
        )
        self.label_combo_box1.setGeometry(*label_combo_box1_geo)

        self.combo_box1 = QComboBox(self.centralwidget)
        self.combo_box1.addItems(self.combo_box1_options)
        self.combo_box1.setCurrentIndex(index_combo_box1_default)
        self.combo_box1.currentIndexChanged.connect(
            self.on_combo_box1_selection_change
        )
        self.combo_box1_geo = (
            200, lineEditHFS_geo[1] + lineEditHFS_geo[3] + 10,
            120, 20
        )
        self.combo_box1.setGeometry(*self.combo_box1_geo)

        parameter_geo = self.combo_box1_geo
        for item in self.parent.main_window.model.p2p_coeff_parameters[
            self.p2p_coeff_variant
        ]:
            label_parameter = QLabel(self.centralwidget)
            label_parameter.setObjectName(f"label_{item['name']}")
            label_parameter.setText(item["name"])
            label_geo = (
                10, parameter_geo[1] + parameter_geo[3] + 10,
                200, 20
            )
            label_parameter.setGeometry(*label_geo)
            parameter = QLineEdit(self.centralwidget)
            parameter.setObjectName(item["name"])
            parameter.setText(item["value"])
            parameter_geo = (
                205, parameter_geo[1] + parameter_geo[3] + 10,
                100, 20
            )
            parameter.setGeometry(*parameter_geo)

        self.label_combo_box2 = QLabel(self.centralwidget)
        self.label_combo_box2.setText("Curve Variability Variant")
        label_combo_box2_geo = (
            10,
            (
                self.combo_box1_geo[1]
                + self.combo_box1_geo[3]
                + (30 * self.get_rows_parameters()) + 10
            ),
            200, 20
        )
        self.label_combo_box2.setGeometry(*label_combo_box2_geo)

        self.combo_box2 = QComboBox(self.centralwidget)
        self.combo_box2.addItems(self.combo_box2_options)
        self.combo_box2.setCurrentIndex(index_combo_box2_default)
        self.combo_box2.currentIndexChanged.connect(
            self.on_combo_box2_selection_change
        )
        self.combo_box2_geo = (
            200, label_combo_box2_geo[1],
            120, 20
        )
        self.combo_box2.setGeometry(*self.combo_box2_geo)

        parameter_geo = self.combo_box2_geo
        for item in self.parent.main_window.model.cur_var_coeff_parameters[
            self.curve_var_variant
        ]:
            label_parameter = QLabel(self.centralwidget)
            label_parameter.setObjectName(f"label_{item['name']}")
            label_parameter.setText(item["name"])
            label_geo = (
                10, parameter_geo[1] + parameter_geo[3] + 10,
                200, 20
            )
            label_parameter.setGeometry(*label_geo)
            parameter = QLineEdit(self.centralwidget)
            parameter.setObjectName(item["name"])
            parameter.setText(item["value"])
            parameter_geo = (
                205, parameter_geo[1] + parameter_geo[3] + 10,
                100, 20
            )
            parameter.setGeometry(*parameter_geo)

        self.buttonSave = QPushButton(self.centralwidget)
        self.buttonSave.setGeometry(
            self.parent.main_top_margin,
            self.parent.main_left_margin,
            self.parent.top_buttons_width,
            self.parent.top_buttons_height
        )
        self.buttonSave.setObjectName("buttonSave")
        self.buttonSave.setText(
            _translate("SelectorSettingsWindow", "Save")
        )
        self.buttonSave.clicked.connect(self.save_event_handler)
        buttonSave_geo = (
            start_size[0] - 10 - 200, start_size[1] - 10 - 30,
            200, 30
        )
        self.buttonSave.setGeometry(*buttonSave_geo)

    def get_rows_parameters(self) -> int:
        """Gets count rows parameters"""
        logger.info("start get_rows_parameters")
        count = 0
        for item in self.parent.main_window.model.p2p_coeff_parameters.values():
            count = max(count, len(item))
        logger.info(f"count: {count}")
        return count

    def on_combo_box1_selection_change(self, index):
        selected_option = self.combo_box1.currentText()
        self.p2p_coeff_variant = selected_option
        parameter_geo = self.combo_box1_geo
        for variant in self.parent.main_window.model.p2p_coeff_variants:
            if selected_option == variant:
                for item in self.parent.main_window.model.p2p_coeff_parameters[
                   variant
                ]:
                    logger.info(f"item: {item}")
                    label_parameter = QLabel(self.centralwidget)
                    label_parameter.setObjectName(f"label_{item['name']}")
                    label_parameter.setText(item["name"])
                    label_geo = (
                        10, parameter_geo[1] + parameter_geo[3] + 10,
                        200, 20
                    )
                    label_parameter.setGeometry(*label_geo)
                    label_parameter.show()
                    parameter = QLineEdit(self.centralwidget)
                    parameter.setObjectName(item["name"])
                    parameter.setText(item["value"])
                    parameter_geo = (
                        205, parameter_geo[1] + parameter_geo[3] + 10,
                        100, 20
                    )
                    parameter.setGeometry(*parameter_geo)
                    parameter.show()
            else:
                for item in self.parent.main_window.model.p2p_coeff_parameters[
                   variant
                ]:
                    q_line = self.findChild(QLineEdit, item["name"])
                    q_line.deleteLater()
                    q_label = self.findChild(
                        QLabel, f"label_{item['name']}"
                    )
                    q_label.deleteLater()

    def on_combo_box2_selection_change(self, index):
        selected_option = self.combo_box2.currentText()
        self.curve_var_variant = selected_option
        parameter_geo = self.combo_box2_geo
        for variant in self.parent.main_window.model.cur_var_coeff_variants:
            if selected_option == variant:
                for item in self.parent.main_window.model.cur_var_coeff_parameters[
                   variant
                ]:
                    logger.info(f"item: {item}")
                    label_parameter = QLabel(self.centralwidget)
                    label_parameter.setObjectName(f"label_{item['name']}")
                    label_parameter.setText(item["name"])
                    label_geo = (
                        10, parameter_geo[1] + parameter_geo[3] + 10,
                        200, 20
                    )
                    label_parameter.setGeometry(*label_geo)
                    label_parameter.show()
                    parameter = QLineEdit(self.centralwidget)
                    parameter.setObjectName(item["name"])
                    parameter.setText(item["value"])
                    parameter_geo = (
                        205, parameter_geo[1] + parameter_geo[3] + 10,
                        100, 20
                    )
                    parameter.setGeometry(*parameter_geo)
                    parameter.show()
            else:
                for item in self.parent.main_window.model.cur_var_coeff_parameters[
                   variant
                ]:
                    q_line = self.findChild(QLineEdit, item["name"])
                    q_line.deleteLater()
                    q_label = self.findChild(
                        QLabel, f"label_{item['name']}"
                    )
                    q_label.deleteLater()
        print(f'Selected: {selected_option}')

    @pyqtSlot()
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    @pyqtSlot()
    def save_event_handler(self):
        """
        Handler for event save settings of EP
        """
        self.parent.main_window.model.p2p_coeff_variant = (
            self.p2p_coeff_variant
        )
        self.parent.main_window.model.cur_var_coeff_variant = (
            self.curve_var_variant
        )
        self.parent.main_window.model.hfrh = int(self.lineEditHFRH.text())
        self.parent.main_window.model.hfrl = int(self.lineEditHFRL.text())
        self.parent.main_window.model.hfs = int(self.lineEditHFS.text())
        self.parent.main_window.model.lfrl = int(self.lineEditLFRL.text())
        self.parent.main_window.model.lfrh = int(self.lineEditLFRH.text())
        self.parent.main_window.model.lfs = int(self.lineEditLFS.text())

        for item in self.parent.main_window.model.p2p_coeff_parameters[
            self.p2p_coeff_variant
        ]:
            logger.info(f"p2p_item_name: {item['name']}")
            object = self.findChild(QLineEdit, item["name"])
            if object:
                item["value"] = object.text()

        for item in self.parent.main_window.model.cur_var_coeff_parameters[
            self.curve_var_variant
        ]:
            logger.info(f"cur_var_item_name: {item['name']}")
            object = self.findChild(QLineEdit, item["name"])
            if object:
                item["value"] = object.text()

        self.closed.emit()
        self.close()
