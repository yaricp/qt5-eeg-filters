
from settings import (
    FILTER_ORDER, RIPPLE, MAX_START_SEARCH, MAX_END_SEARCH,
    MIN_START_SEARCH, MIN_END_SEARCH, BANDWIDTHS,
    MAX_ITER_VALUE, MAX_STEP_ITER, DEFAULT_STEP_ITER,
    LFRL, LFRH, LFS, HFRL, HFRH, HFS
)


class Config:
    """ Class implement configs of application. """
    time_measuring = 0  # TODO:  unused
    filter_order: int = FILTER_ORDER
    ripple: int = RIPPLE
    max_start_search: float = MAX_START_SEARCH
    max_end_search: float = MAX_END_SEARCH
    min_start_search: float = MIN_START_SEARCH
    min_end_search: float = MIN_END_SEARCH
    bandwidths = BANDWIDTHS
    max_iter_value: float = MAX_ITER_VALUE
    max_step_iter: int = MAX_STEP_ITER
    default_step_iter: int = DEFAULT_STEP_ITER
    iter_value: float = MAX_ITER_VALUE * DEFAULT_STEP_ITER / MAX_STEP_ITER
    source_filepath: str = ''
    target_dirpath: str = ''
    fs = 0

    # for ep_passband_filter_selector

    lfrl: int = LFRL
    lfrh: int = LFRH
    lfs: int = LFS
    hfrl: int = HFRL
    hfrh: int = HFRH
    hfs: int = HFS


class ModelData:
    """ Class implement data of curves, bandwidth of filter and points. """
    dict_bandwidth_data = {}
    dict_extremums_data = {}
    dict_showed_extremums = {}
    total_count: int = 0

    list_times = []
    list_data = []
    tick_times = []
    check_box_list = []

    prev_path_open: str = ""
    prev_path_export: str = ""

    # for ep_passband_filter_selector
    changed_curves = {}
    ep_found_bandpass = []
    ep_heatmap = {}

    p2p_coeff_variants = []
    p2p_coeff_parameters = {}
    cur_var_coeff_variants = []
    cur_var_coeff_parameters = {}
    p2p_coeff_variant = ""
    cur_var_coeff_variant = ""
    base_region = ()

    hfrh = 0
    hfrl = 0
    hfs = 0
    lfrl = 0
    lfrh = 0
    lfs = 0

    def clear_extremums(self) -> None:
        """ Clear dict of extremums."""

        self.dict_extremums_data = {
            "max": {}, "min": {}
        }
