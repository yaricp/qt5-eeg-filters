
from settings import *


class Config:
    """ Class implement configs of application. """
    time_measuring = 0  # TODO:  unused
    filter_order = FILTER_ORDER
    ripple = RIPPLE
    max_start_search = MAX_START_SEARCH
    max_end_search = MAX_END_SEARCH
    min_start_search = MIN_START_SEARCH
    min_end_search = MIN_END_SEARCH
    bandwidths = BANDWIDTHS
    max_iter_value = MAX_ITER_VALUE
    max_step_iter = MAX_STEP_ITER
    default_step_iter = DEFAULT_STEP_ITER
    iter_value = MAX_ITER_VALUE * DEFAULT_STEP_ITER / MAX_STEP_ITER
    source_filepath = ''
    target_dirpath = ''
    fs = None

    # for ep_passband_filter_selector

    lfrl = LFRL
    lfrh = LFRH
    lfs = LFS
    hfrl = HFRL
    hfrh = HFRH
    hfs = HFS


class ModelData:
    """ Class implement data of curves, bandwidth of filter and points. """
    dict_bandwidth_data = {}
    dict_extremums_data = {}
    dict_showed_extremums = {}
    total_count = 0

    list_times = []
    list_data = []
    tick_times = 0
    check_box_list = []

    prev_path_open = ""
    prev_path_export = ""

    # for ep_passband_filter_selector
    changed_curves = {}
    ep_found_bandpass = []
    ep_heatmap = {}


    def clear_extremums(self) -> None:
        """ Clear dict of extremums."""

        self.dict_extremums_data = {
            'max': {},
            'min': {}
        }
