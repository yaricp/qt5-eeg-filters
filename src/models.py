
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


class ModelData:
    """ Class implement data of curves, bandwidth of filter and points. """
    dict_bandwidth_data = {}
    dict_extremums_data = {}
    dict_showed_extremums = {}
    total_count = 0

    list_times = []
    list_data = []
    tick_times = 0

    # for ep_passband_filter_selector
    changed_curves = {}
    selector_filter_borders = {}
    # selector_range_search_extremums = {}

    def clear_extremums(self) -> None:
        """ Clear dict of extremums."""

        self.dict_extremums_data = {
            'max': {},
            'min': {}
        }
