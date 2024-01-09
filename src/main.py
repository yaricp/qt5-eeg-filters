#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main file of QT GUI."""
from PyQt5.QtWidgets import QApplication

from models import Config, ModelData
from handlers import Handler
from controllers import Controller
from views import ViewGraph


class MainWindow:

    """Main windows of program."""

    def __init__(self) -> None:
        """initialization and prepare data."""

        self.config = Config()
        self.model = ModelData()
        self.view = ViewGraph(self.config, main=self)
        self.controller = Controller(self.config, self.model, self.view)
        self.handler = Handler(self.config, self.model, self.view, self.controller)
        self.view.resized.connect(self.handler.reshow_elements_after_resize_main_window)
        self.view.bandwidths_clicked_event.connect(self.handler.bandwidths_activated)
        self.view.maximums_region_changed_event.connect(
            self.handler.change_range_search_extremums
        )
        self.view.minimums_region_changed_event.connect(
            self.handler.change_range_search_extremums
        )
        self.view.edit_max_start_changed_event.connect(
            self.handler.change_text_line_extremums_edits
        )
        self.view.edit_max_end_changed_event.connect(
            self.handler.change_text_line_extremums_edits
        )
        self.view.edit_min_start_changed_event.connect(
            self.handler.change_text_line_extremums_edits
        )
        self.view.edit_min_end_changed_event.connect(
            self.handler.change_text_line_extremums_edits
        )
        self.view.menu_open_file_event.connect(self.handler.show_dialog_open)
        self.view.open_clicked_event.connect(self.handler.show_dialog_open)
        self.view.menu_save_file_event.connect(self.handler.save_button_pressed)
        self.view.save_clicked_event.connect(self.handler.save_button_pressed)
        self.view.menu_close_file_event.connect(self.handler.close_button_pressed)
        self.view.add_clicked_event.connect(self.handler.add_new_bandwidth)
        self.view.value_changed_event.connect(self.handler.change_value_slider)
        self.view.toggle_visible_regions_event.connect(self.handler.hide_show_regions)
        self.view.start_ep_passband_search_event.connect(self.handler.start_ep_passband_search)


if __name__ == '__main__':
    from sys import argv, exit
    app = QApplication(argv)
    win = MainWindow()
    win.view.show()
    exit(app.exec_())
