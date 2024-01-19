import os

from eeg_filters import upload as eeg_filters_upload
from eeg_filters.filters import make_filter, search_max_min
from eeg_filters.export import export_curves, export_extremums

from views import ViewGraph
from models import Config, ModelData

from passband_searcher import (
    PassbandSearcher, export_data as ep_export_data
)


class Controller:

    def __init__(
        self, config: Config, model: ModelData, view: ViewGraph
    ):
        self.model = model
        self.view = view
        self.config = config
        self.counter_proc = 0
        self.counter_factor = 100

    def calc_add_extremums(self, bandwidth: list, ext: str) -> bool:
        """
        Calculate extremums on curves.
        It use package eeg-filters and function search_max_min().
        Returns - True if ok.
        """
        range_search = self.view.range_search_maxmums
        if ext == 'min':
            range_search = self.view.range_search_minimums
        where_find = range_search.getRegion()
        dict_data = self.model.dict_bandwidth_data['%s' % bandwidth]
        dict_extremums = self.model.dict_extremums_data[ext]
        dict_data_extremums = {}

        for time_stamp, row in dict_data.items():

            dict_data_extremums.update({
                time_stamp: search_max_min(
                    self.model.tick_times,
                    row,
                    where_find,
                    ext
                )
            })
            self.counter_proc += 1
            progress = self.counter_proc * self.counter_factor / self.model.total_count
            self.view.set_progress_value(progress)

        dict_extremums.update({'%s' % bandwidth: dict_data_extremums})
        return True

    def calc_add_bandwidth(self, bandwidth: list) -> bool:
        """
        Make filter of curves.
        It use package eeg-filters and function make_filter.
        Returns - True if ok.
        """
        dict_curves_filtred = {}
        for key_curv, row in zip(
            self.model.list_times, self.model.list_data
        ):
            filtred_data = make_filter(
                row,
                bandwidth,
                self.config.fs,
                self.config.filter_order,
                self.config.ripple
            )
            dict_curves_filtred.update({key_curv: filtred_data})
            self.counter_proc += 1
            progress = self.counter_proc * self.counter_factor / self.model.total_count
            self.view.set_progress_value(progress)

        self.model.dict_bandwidth_data.update({
            '%s' % bandwidth: dict_curves_filtred
        })
        return True

    def prepare_data(self) -> bool:
        """Prepare data and plot after load data.
        Returns - True if ok.
        """
        if not self.config.source_filepath:
            return False

        self.model.dict_bandwidth_data = {}
        self.model.clear_extremums()
        (
            self.config.fs,
            self.model.list_times,
            self.model.tick_times,
            self.model.list_data
        ) = eeg_filters_upload.prepare_data(self.config.source_filepath)
        self.model.total_count = len(self.model.list_times)
        if self.model.total_count == 0:
            return False
        dict_curves_filtred = {}
        flag_new = False
        if self.view.is_graph_empty():
            flag_new = True
        for time_stamp, row in zip(self.model.list_times, self.model.list_data):
            self.counter_proc += 1
            progress = self.counter_proc * self.counter_factor / self.model.total_count
            self.view.set_progress_value(progress)
            dict_curves_filtred.update({time_stamp: row})

            #  prepare graph
            if flag_new:
                # create new plots for curves
                self.view.create_graph(time_stamp)
                self.view.add_checkbox(self.counter_proc, time_stamp)

        if flag_new:
            self.view.add_ranges_extremums()
        if flag_new:
            maximums = {}
            minimums = {}
            for time_stamp in self.model.list_times:
                self.counter_proc += 1
                progress = self.counter_proc * self.counter_factor / self.model.total_count
                self.view.set_progress_value(progress)
                # create new points on graphic for extremums
                (showed_max, showed_min) = self.view.add_point_extremums(time_stamp)

                maximums.update({time_stamp: showed_max})
                minimums.update({time_stamp: showed_min})
            # save new extremums in model
            self.model.dict_showed_extremums.update({
                'max': maximums,
                'min': minimums
            })
        self.model.dict_bandwidth_data.update(
            {'source': dict_curves_filtred})

    def get_data_show_graphics(self):
        """Get all data for plots and call functions for show plots."""
        index = self.view.listBandwidths.currentRow()
        bandwidth = self.config.bandwidths[index]

        if not '%s' % bandwidth in self.model.dict_bandwidth_data.keys():
            self.calc_add_bandwidth(bandwidth)

        # show filtered curves and save curves into draggable points
        self.view.show_graphic_filtered(
            self.model.dict_bandwidth_data['%s' % bandwidth],
            self.model.dict_showed_extremums["max"],
            self.model.dict_showed_extremums["min"],
            self.model.tick_times,
            self.model.total_count
        )
        self.calc_and_show_extremums(bandwidth)

    def calc_and_show_extremums(self, bandwidth=None):
        """
        Calculate extremums points in regions.
        Call function for show plots.
        """
        if not bandwidth:
            index = self.view.listBandwidths.currentRow()
            bandwidth = self.config.bandwidths[index]
        if not '%s' % bandwidth in self.model.dict_extremums_data:
            self.calc_add_extremums(bandwidth, 'max')
            self.calc_add_extremums(bandwidth, 'min')

        # show range where needs find extremums
        self.view.show_range_extremums(self.model.total_count)
        # show points of extremums
        for ext in ("max", "min"):
            dict_data = self.model.dict_extremums_data[ext]['%s' % bandwidth]
            showed_extremums = self.model.dict_showed_extremums[ext]
            self.view.reshow_extremums(
                dict_data,
                showed_extremums,
                (ext, '%s' % bandwidth)
            )

    def export_data(self) -> None:
        """
        Export curves and extremums in files.
        Returns - None.
        """

        value = self.model.dict_bandwidth_data[self.config.bandwidths[0]]
        rows = value[self.model.list_times[0]]
        count_rows = len(rows)

        total_count = len(self.config.bandwidths)
        for bandwidth, dict_data in self.model.dict_bandwidth_data.items():
            if bandwidth != 'source':
                self.counter_proc += 1
                progress = self.counter_proc * self.counter_factor / total_count
                self.view.set_progress_value(progress)
                export_curves(
                    self.config.source_filepath,
                    self.config.target_dirpath,
                    bandwidth,
                    dict_data,
                    count_rows=count_rows
                )
                dict_extremums_export = {}
                for (key_max, row_max), (key_min, row_min) in zip(
                    self.model.dict_extremums_data['max'][bandwidth].items(),
                    self.model.dict_extremums_data['min'][bandwidth].items()
                ):
                    dict_extremums_export.update({
                        key_max: (row_max, row_min)
                    })

                max_search_range, min_search_range = self.view.get_ranges_extremums()
                times_ranges = (max_search_range, min_search_range)
                export_extremums(
                    self.config.source_filepath,
                    self.config.target_dirpath,
                    bandwidth,
                    dict_extremums_export,
                    times_ranges
                )

    def change_extremum_data(self, time, value, *args):
        """
        Save changed value of extremum point when user move this point by curve.
        """
        model = self.model.dict_extremums_data
        model[args[0]][args[1]][args[2]] = (time, value)

    def start_ep_passband_search(self) -> None:
        """
        Starts EP bassband search
        """
        # self.model.selector_filter_borders
        pbs = PassbandSearcher(
            curves=self.model.changed_curves.values(),
            tick_times=self.model.tick_times,
            fsr=self.config.fs,
            max_search_range=self.view.range_search_maxmums.getRegion(),
            min_search_range=self.view.range_search_minimums.getRegion(),
            filter_high_limit_range=(
                self.view.lineEditHFRL.text(),
                self.view.lineEditHFRH.text()
            ),
            step_high_filter=self.view.lineEditHFS.text(),
            filter_low_limit_range=(
                self.view.lineEditLFRL.text(),
                self.view.lineEditLFRH.text()
            ),
            step_low_filter=self.view.lineEditLFS.text(),
            type_mean="average",
            cheb_filter_order=self.config.filter_order,
            cheb_ripple=self.config.ripple
        )
        print("Start!!!")
        result = pbs.start()
        print("Result:", result)
        return result
        
    def ep_selector_export_data(self) -> None:
        """
        calls method save of ep_bandpass_filter_selector
        """
        bandpass = self.model.ep_found_bandpass
        heatmap = self.model.ep_heatmap
        target_dirpath = self.config.target_dirpath
        target_filepath = os.path.join(
            target_dirpath,
            f"optimal_filter_{'_'.join([str(x) for x in bandpass])}.csv"
        )
        result = ep_export_data(
            target_filepath,
            bandpass,
            heatmap
        )
        return result