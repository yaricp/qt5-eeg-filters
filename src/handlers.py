import time

from loguru import logger
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import (
    Qt, QThreadPool, QMetaObject, QRunnable
)


class RequestRunnable(QRunnable):
    def __init__(self, handler):
        QRunnable.__init__(self)
        self.handler = handler

    def run(self):
        """
        Starts new threads for selector.
        """
        bandpass, heatmap = self.handler.controller.start_ep_passband_search()
        self.handler.model.ep_found_bandpass = bandpass
        self.handler.model.ep_heatmap = heatmap
        QMetaObject.invokeMethod(
            self.handler.view, "get_selector_result", Qt.QueuedConnection
        )


class Handler:

    def __init__(self, config, model, view, controller):
        self.model = model
        self.config = config
        self.view = view
        self.controller = controller

    def reshow_elements_after_resize_main_window(self) -> None:
        # logger.debug("Start resize windows %s" % self.view.width())
        print("VIEW WIDTH:", self.view.width())
        print("VIEW HEIGHT:", self.view.height())
        progress_bar_pos = (
            self.view.main_left_margin,
            self.view.height() - (
                self.view.progress_bar_height + self.view.main_bottom_margin
            )
        )
        progress_bar_width = self.view.width() - (
            self.view.main_right_margin + self.view.main_left_margin
        )
        progress_bar_size = (
            progress_bar_width, self.view.progress_bar_height
        )
        self.view.progressBar.setGeometry(
            *progress_bar_pos, *progress_bar_size
        )
        
        button_add_passband_size = (
            self.view.bandwidth_area_width, 
            self.view.top_buttons_height
        )
        button_add_passband_pos = (
            self.view.width() - (
                self.view.main_right_margin + self.view.bandwidth_area_width
            ),
            progress_bar_pos[1] - 10 - self.view.top_buttons_height
        )
        self.view.buttonAdd.setGeometry(
            *button_add_passband_pos, *button_add_passband_size
        )
        
        new_bandwidth_field_size = (
            self.view.bandwidth_area_width, self.view.top_buttons_height
        )
        new_bandwidth_field_pos = (
            button_add_passband_pos[0],
            button_add_passband_pos[1] - 5 - self.view.top_buttons_height
        )
        self.view.newBandwidthField.setGeometry(
            *new_bandwidth_field_pos, *new_bandwidth_field_size
        )
        
        list_bandwidths_top_margin = (
            self.view.main_top_margin + self.view.top_buttons_height + 5
        )
        list_bandwidths_size = (
            self.view.bandwidth_area_width,
            new_bandwidth_field_pos[1] - 5 - list_bandwidths_top_margin
        )
        list_bandwidths_pos = (
            button_add_passband_pos[0],
            list_bandwidths_top_margin
        )
        self.view.listBandwidths.setGeometry(
            *list_bandwidths_pos, *list_bandwidths_size
        )
        slider1_size = (
            self.view.slider1_size,
            list_bandwidths_size[1] + 2 * self.view.top_buttons_height + 10
        )
        slider1_pos = (
            list_bandwidths_pos[0] - 5 - slider1_size[0],
            list_bandwidths_top_margin
        )
        self.view.slider1.setGeometry(
            *slider1_pos, *slider1_size
        )
        
        graph_size = (
            slider1_pos[0]
            - 5 
            - self.view.left_checkboxes_width
            - 5
            - self.view.main_left_margin,
            slider1_size[1]
        )
        graph_pos = (
            self.view.main_left_margin + self.view.left_checkboxes_width + 5,
            self.view.main_top_margin + self.view.top_buttons_height + 5
        )
        self.view.graph.setGeometry(
            *graph_pos, *graph_size
        )

        button_open_size = (
            self.view.top_buttons_width, self.view.top_buttons_height
        )
        button_open_pos = (
            self.view.main_left_margin + self.view.left_checkboxes_width + 5,
            self.view.main_top_margin
        )
        self.view.buttonOpen.setGeometry(
            *button_open_pos, *button_open_size
        )

        check_box_all_size = (
            self.view.left_checkboxes_width,
            self.view.left_checkboxes_height
        )
        check_box_all_pos = (
            self.view.main_left_margin,
            (
                self.view.main_top_margin 
                + self.view.top_buttons_height / 2
                - self.view.left_checkboxes_height/2
            )
        )
        
        self.view.check_box_all.setGeometry(
            *check_box_all_pos, *check_box_all_size
        )

        button_save_size = (
            self.view.top_buttons_width, self.view.top_buttons_height
        )
        button_save_pos = (
            button_open_pos[0] + 5 + self.view.top_buttons_width,
            self.view.main_top_margin
        )
        self.view.buttonSave.setGeometry(
            *button_save_pos, *button_save_size
        )

        line_edit_max_start_size = (
            self.view.top_buttons_width / 2, self.view.top_buttons_height
        )
        line_edit_max_start_pos = (
            button_save_pos[0] + button_save_size[0] + 30,
            self.view.main_top_margin
        )
        self.view.lineEditMaxStart.setGeometry(
            *line_edit_max_start_pos,
            *line_edit_max_start_size
        )

        line_edit_max_end_size = (
            self.view.top_buttons_width / 2, self.view.top_buttons_height
        )
        line_edit_max_end_pos = (
            line_edit_max_start_pos[0] + line_edit_max_start_size[0] + 5,
            self.view.main_top_margin
        )
        self.view.lineEditMaxEnd.setGeometry(
            *line_edit_max_end_pos,
            *line_edit_max_end_size
        )

        button_visible_region_size = (
            self.view.top_buttons_width, self.view.top_buttons_height
        )
        button_visible_region_pos = (
            line_edit_max_end_pos[0] + line_edit_max_end_size[0] + 5,
            self.view.main_top_margin
        )
        self.view.buttonVisibleRegion.setGeometry(
            *button_visible_region_pos,
            *button_visible_region_size
        )

        line_edit_min_start_size = (
            self.view.top_buttons_width / 2, self.view.top_buttons_height
        )
        line_edit_min_start_pos = (
            button_visible_region_pos[0] + button_visible_region_size[0] + 5,
            self.view.main_top_margin
        )
        self.view.lineEditMinStart.setGeometry(
            *line_edit_min_start_pos,
            *line_edit_min_start_size
        )

        line_edit_min_end_size = (
            self.view.top_buttons_width / 2, self.view.top_buttons_height
        )
        line_edit_min_end_pos = (
            line_edit_min_start_pos[0] + line_edit_min_start_size[0] + 5,
            self.view.main_top_margin
        )
        self.view.lineEditMinEnd.setGeometry(
            *line_edit_min_end_pos,
            *line_edit_min_end_size
        )

        button_start_search_pos = (
            self.view.width() - (
                self.view.main_left_margin + self.view.top_buttons_width
            ),
            self.view.main_top_margin
        )
        button_start_search_size = (
            self.view.top_buttons_width, self.view.top_buttons_height
        )
        self.view.buttonStartSearch.setGeometry(
            *button_start_search_pos,
            *button_start_search_size
        )

        spinner_size = (
            self.view.top_buttons_height, self.view.top_buttons_height
        )
        spinner_pos = (
            button_start_search_pos[0] - spinner_size[0] - 5,
            self.view.main_top_margin * 2 + spinner_size[1] / 2
        )
        self.view.spinner.setGeometry(*spinner_pos, *spinner_size)

        line_edit_lfs_size = (
            self.view.top_buttons_width / 2, self.view.top_buttons_height
        )
        line_edit_lfs_pos = (
            spinner_pos[0] - line_edit_lfs_size[0] - 5,
            self.view.main_top_margin
        )
        self.view.lineEditHFS.setGeometry(
            *line_edit_lfs_pos,
            *line_edit_lfs_size
        )

        line_edit_lfrl_size = (
            self.view.top_buttons_width / 2, self.view.top_buttons_height
        )
        line_edit_lfrl_pos = (
            line_edit_lfs_pos[0] - line_edit_lfrl_size[0] - 5,
            self.view.main_top_margin
        )
        self.view.lineEditHFRH.setGeometry(
            *line_edit_lfrl_pos,
            *line_edit_lfrl_size
        )

        line_edit_lfrh_size = (
            self.view.top_buttons_width / 2, self.view.top_buttons_height
        )
        line_edit_lfrh_pos = (
            line_edit_lfrl_pos[0] - line_edit_lfrh_size[0] - 5,
            self.view.main_top_margin
        )
        self.view.lineEditHFRL.setGeometry(
            *line_edit_lfrh_pos,
            *line_edit_lfrh_size
        )

        line_edit_hfs_size = (
            self.view.top_buttons_width / 2, self.view.top_buttons_height
        )
        line_edit_hfs_pos = (
            line_edit_lfrh_pos[0] - line_edit_hfs_size[0] - 30,
            self.view.main_top_margin
        )
        self.view.lineEditLFS.setGeometry(
            *line_edit_hfs_pos,
            *line_edit_hfs_size
        )

        line_edit_hfrl_size = (
            self.view.top_buttons_width / 2, self.view.top_buttons_height
        )
        line_edit_hfrl_pos = (
            line_edit_hfs_pos[0] - line_edit_hfrl_size[0] - 5,
            self.view.main_top_margin
        )
        self.view.lineEditLFRH.setGeometry(
            *line_edit_hfrl_pos,
            *line_edit_hfrl_size
        )

        line_edit_hfrh_size = (
            self.view.top_buttons_width / 2, self.view.top_buttons_height
        )
        line_edit_hfrh_pos = (
            line_edit_hfrl_pos[0] - line_edit_hfrh_size[0] - 5,
            self.view.main_top_margin
        )
        self.view.lineEditLFRL.setGeometry(
            *line_edit_hfrh_pos,
            *line_edit_hfrh_size
        )

    def bandwidths_activated(self, item) -> None:
        """
        Handler change bandwidth.
        Returns - True if ok.
        """
        if item.text() == 'source' and not self.config.source_filepath:
            self.show_dialog_open()
            return None
        self.view.show_progress_bar()
        self.controller.counter_proc = 0
        self.controller.counter_factor = 50
        self.controller.get_data_show_graphics()
        self.view.hide_progress_bar()

    def change_range_search_extremums(self) -> None:
        """
        Handler event change region search extremums.

        Returns - True if ok.

        """
        if self.model.total_count == 0 or not self.model.dict_showed_extremums:
            return None

        self.view.lineEditMaxStart.setText(
            str(round(self.view.range_search_maxmums.getRegion()[0], 5))
        )
        self.view.lineEditMaxEnd.setText(
            str(round(self.view.range_search_maxmums.getRegion()[1], 5)))

        self.view.lineEditMinStart.setText(
            str(round(self.view.range_search_minimums.getRegion()[0], 5))
        )
        self.view.lineEditMinEnd.setText(
            str(round(self.view.range_search_minimums.getRegion()[1], 5)))
        self.view.show_progress_bar()
        self.controller.counter_proc = 0
        self.controller.counter_factor = 100
        self.controller.calc_and_show_extremums()
        self.view.hide_progress_bar()

    def change_value_slider(self) -> bool:
        """
        Handler event change value slider.
        Returns - True if ok.
        """
        self.view.iter_value = (
                self.view.slider1.value()
                * self.config.max_iter_value
                / self.config.max_step_iter
        )
        QApplication.processEvents()
        self.view.show_progress_bar()
        self.controller.counter_proc = 0
        self.controller.counter_factor = 50
        self.controller.get_data_show_graphics()
        self.view.hide_progress_bar()
        return True

    def show_dialog_open(self) -> bool:
        """
        Show dialog window.
        Returns - True if ok.
        """
        logger.info("show dialog open")
        self.config.source_filepath, _ = self.view.get_source_file_name()

        filename = self.config.source_filepath.split("/")[-1]
        self.model.prev_path_open = self.config.source_filepath.replace(
            filename, ""
        )

        logger.info(
            f"self.config.source_filepath: {self.config.source_filepath}"
        )

        if not self.config.source_filepath:
            return False
        item = self.view.listBandwidths.item(0)
        item.setSelected(True)
        self.view.listBandwidths.setCurrentItem(item)
        self.view.show_progress_bar()
        self.controller.counter_proc = 0
        self.controller.counter_factor = 25
        self.controller.prepare_data()
        self.controller.get_data_show_graphics()
        self.view.hide_progress_bar()
        return True

    def save_button_pressed(self) -> bool:
        """
        Handler event save button pressed.
        Returns - True if ok.
        """

        if not self.config.target_dirpath:
            self.config.target_dirpath = self.view.get_target_file_name()
        if not self.config.target_dirpath:
            return False

        filename = self.config.target_dirpath.split("/")[-1]
        self.model.prev_path_export = self.config.target_dirpath.replace(
            filename, ""
        )

        QApplication.processEvents()
        self.view.show_progress_bar()
        self.controller.counter_proc = 0
        self.controller.counter_factor = 100
        self.controller.export_data()
        self.view.hide_progress_bar()
        return True

    def hide_show_regions(self):
        """Handler click button for show and hide regions for search extremum."""
        if self.view.range_search_minimums.isVisible():
            self.view.range_search_minimums.setVisible(0)
            self.view.range_search_maxmums.setVisible(0)
            return
        self.view.range_search_minimums.setVisible(1)
        self.view.range_search_maxmums.setVisible(1)

    def close_button_pressed(self) -> None:
        """
        Handler event pressed close button.
        Returns: None.
        """
        if self.model.dict_bandwidth_data:
            self.save_button_pressed()
        QApplication.quit()

    def change_text_line_extremums_edits(self) -> bool:
        """
        Handler event change text search extremums.

        Returns - True if ok.

        """
        if self.model.total_count == 0 or not self.model.dict_showed_extremums:
            return False
        self.view.range_search_maxmums.setRegion([
            float(self.view.lineEditMaxStart.text()),
            float(self.view.lineEditMaxEnd.text())
        ])
        self.view.range_search_minimums.setRegion([
            float(self.view.lineEditMinStart.text()),
            float(self.view.lineEditMinEnd.text())
        ])
        self.view.show_progress_bar()
        self.controller.counter_proc = 0
        self.controller.counter_factor = 100
        self.controller.calc_and_show_extremums()
        self.view.hide_progress_bar()
        return True

    def add_new_bandwidth(self) -> None:
        """Handler event pressed button add bandwidth."""
        text = self.view.newBandwidthField.text()
        self.view.listBandwidths.addItem(text)
        splitted_text = text.split(',')
        value = [
            int(splitted_text[0].replace('[', '')),
            int(splitted_text[1].replace(']', '').replace(' ', ''))
        ]
        self.config.bandwidths.append(value)
        self.view.newBandwidthField.clear()

    def curve_clicked(self, b) -> None:
        """
        Changes dict of changed curves.
        """
        key = b.text()
        index_curve = self.model.list_times.index(key)
        graph_plot_item = self.view.graph.getPlotItem().items[index_curve]
        curve = self.model.dict_bandwidth_data["source"][key]
        if b.isChecked() == True:
            self.model.changed_curves[key] = curve
            graph_plot_item.setPen(color="g", width=3)
        else:
            del self.model.changed_curves[key]
            graph_plot_item.setPen(color=(0,0,0), width=2)
        if len(self.model.changed_curves) >= 2:
            self.view.buttonStartSearch.setEnabled(True)
        else:
            self.view.buttonStartSearch.setEnabled(False)
    
    def select_deselect_all(self) -> None:
        """
        Selects and deselects all checkboxes
        """
        if self.view.check_box_all.isChecked() == True:
            for checkbox in self.model.check_box_list:
                checkbox.setChecked(True)
            self.view.buttonStartSearch.setEnabled(True)
        else:
            for checkbox in self.model.check_box_list:
                checkbox.setChecked(False)
            self.view.buttonStartSearch.setEnabled(False)
    
    def start_ep_passband_search(self) -> None:
        """
        Calls controller method.
        """
        self.view.spinner.show()
        runnable = RequestRunnable(self)
        QThreadPool.globalInstance().start(runnable)
