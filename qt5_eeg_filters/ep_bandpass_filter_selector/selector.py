import csv
import numpy as np
from itertools import combinations
from loguru import logger

from eeg_filters.filters import make_filter, search_max_min


class PassbandSelector:
    """
    Class to implement the selection of a bandpass filter.
    """

    def __init__(
        self,
        curves: list,
        tick_times: list,
        fsr: int,
        max_search_range: tuple,
        min_search_range: tuple,
        **kwargs,
    ) -> None:
        """
        Initialization of an item.
        """

        logger.info(f"kwargs: {kwargs}")
        self.filter_low_limit_range = 1, 30
        self.step_low_filter = 1
        self.filter_high_limit_range = 100, 500
        self.step_high_filter = 10
        self.type_mean = "average"
        self.cheb_filter_order = 3
        self.cheb_ripple = 3
        self.p2p_coeff_variant = "p2p_abs"
        self.curve_variability_coeff_variant = "curve_variability"
        
        self.p2p_coeff_functions = {
            "p2p_abs": self.p2p_abs_coeff,
            "p2p_rel": self.p2p_coeff_by_base_region
        }
        self.p2p_coeff_functions_parameters = {
            "p2p_rel": [
                {
                    "name": "base_region",
                    "type": "tuple",
                    "value": "0.01, 0.03"
                }
            ],
            "p2p_abs": []
        }
        self.curve_variability_coeff_functions = {
            "curve_variability": self.get_curve_cvc,
            "peak_variability": self.get_peak_cvc
        }
        self.curve_variability_coeff_functions_parameters = {
            "curve_variability": [],
            "peak_variability": []
        }

        self.curves = curves
        self.tick_times = tick_times
        self.frequency_sample_rate = int(fsr)
        self.max_search_range = max_search_range
        self.min_search_range = min_search_range

        self.base_region = self.get_default_base_region()

        if "p2p_coeff_variant" in kwargs and kwargs["p2p_coeff_variant"] != "":
            self.p2p_coeff_variant = kwargs["p2p_coeff_variant"]
        if (
            "cur_var_coeff_variant" in kwargs
            and kwargs["cur_var_coeff_variant"] != ""
        ):
            self.curve_variability_coeff_variant = kwargs[
                "cur_var_coeff_variant"
            ]
        if "base_region" in kwargs and kwargs["base_region"] != ():
            self.base_region = kwargs["base_region"]
        if "fllr" in kwargs:
            self.filter_low_limit_range = kwargs["fllr"]
        if "filter_low_limit_range" in kwargs:
            self.filter_low_limit_range = kwargs["filter_low_limit_range"]
        self.filter_low_limit_range = [
            int(x) for x in self.filter_low_limit_range
        ]
        if "fhlr" in kwargs:
            self.filter_high_limit_range = kwargs["fhlr"]
        if "filter_high_limit_range" in kwargs:
            self.filter_high_limit_range = kwargs["filter_high_limit_range"]
        self.filter_high_limit_range = [
            int(x) for x in self.filter_high_limit_range
        ]
        if "slf" in kwargs:
            self.step_low_filter = kwargs["slf"]
        if "step_low_filter" in kwargs:
            self.step_low_filter = kwargs["step_low_filter"]
        self.step_low_filter = int(self.step_low_filter)
        if "shf" in kwargs:
            self.step_high_filter = kwargs["shf"]
        if "step_high_filter" in kwargs:
            self.step_high_filter = kwargs["step_high_filter"]
        self.step_high_filter = int(self.step_high_filter)
        if "tm" in kwargs:
            self.type_mean = kwargs["tm"]
        if "type_mean" in kwargs:
            self.type_mean = kwargs["type_mean"]
        if "chfo" in kwargs:
            self.cheb_filter_order = kwargs["chfo"]
        if "cheb_filter_order" in kwargs:
            self.cheb_filter_order = kwargs["cheb_filter_order"]
        self.cheb_filter_order = int(self.cheb_filter_order)
        if "chr" in kwargs:
            self.cheb_ripple = kwargs["chr"]
        if "cheb_ripple" in kwargs:
            self.cheb_ripple = kwargs["cheb_ripple"]
        self.cheb_ripple = int(self.cheb_ripple)

        self.get_p2p_coeff = self.p2p_coeff_functions[
            self.p2p_coeff_variant
        ]
        self.get_curve_var_coeff = self.curve_variability_coeff_functions[
            self.curve_variability_coeff_variant
        ]

        logger.info(f"self.get_p2p_coeff: {self.get_p2p_coeff}")
        logger.info(f"self.get_curve_var_coeff: {self.get_curve_var_coeff}")
        logger.info(
            f"TYPE: {type(self.filter_low_limit_range[0])}"
        )
        logger.info(f": {self.filter_low_limit_range[0]}")

        self.filtered_curves = []
        self.filter_by_optimum = {}
        self.optimums = []
        self.optimum_matrix = {}

    def get_default_base_region(self) -> tuple:
        """Gets default base region"""
        min_time_extremums = min(
            self.max_search_range[0], self.min_search_range[0]
        )
        min_time = min_time_extremums / 3
        max_time = min_time_extremums * 2 / 3
        return (min_time, max_time)

    def get_curve_cvc(
        self, filtered_curves: list, av_amp_pn: float = 0
    ) -> float:
        """
        Calculates the average reproducibility of the filtered curves.

        Parameters:
            filtered_curves(list): List of filtered curves.

        Returns:
            (float): The average reproducibility.
        """
        logger.info("start get_reproduct")
        integrals = []
        for curve1, curve2 in combinations(filtered_curves, 2):
            integral = self.get_integral(curve1, curve2)
            integrals.append(integral)
        if self.type_mean == "average":
            try:
                ave_integral = sum(integrals) / len(integrals)
            except Exception as err:
                logger.error(f"Error: {err}")
        # elif self.check_square:
        #     ave_integral = self.get_square_mean(integrals)
        return ave_integral

    def get_peak_cvc(
        self, filtered_curves: list
    ) -> float:
        """get reproduct by peaks CVC"""
        av_lat_p_list = []
        av_lat_n_list = []
        av_amp_pn_cvc_list = []
        for curve in filtered_curves:
            curve_max = search_max_min(
                self.tick_times, curve, self.max_search_range, "max"
            )
            curve_min = search_max_min(
                self.tick_times, curve, self.min_search_range, "min"
            )
            av_lat_p_list.append(curve_max[0])
            av_lat_n_list.append(curve_min[0])
            av_amp_pn_cvc_list.append(curve_max[1] - curve_min[1])
        av_lat_p = sum(av_lat_p_list) / len(filtered_curves)
        av_lat_n = sum(av_lat_n_list) / len(filtered_curves)
        av_amp_cvc_pn = sum(av_amp_pn_cvc_list) / len(filtered_curves)
        dev_sum_list = []
        for curve in filtered_curves:
            curve_max = search_max_min(
                self.tick_times, curve, self.max_search_range, "max"
            )
            curve_min = search_max_min(
                self.tick_times, curve, self.min_search_range, "min"
            )
            lat_p = curve_max[0]
            lat_n = curve_min[0]
            amp_pn = abs(curve_max[1] - curve_min[1])
            dev_lat_p = 100 * abs(lat_p - av_lat_p) / av_lat_p
            dev_lat_n = 100 * abs(lat_n - av_lat_n) / av_lat_n
            dev_amp_pn = 100 * abs(amp_pn - av_amp_cvc_pn) / av_amp_cvc_pn
            dev_sum = abs(dev_lat_p) + abs(dev_lat_n) + abs(dev_amp_pn)
            dev_sum_list.append(dev_sum)
        psc = sum(dev_sum_list) / len(filtered_curves)
        return psc

    def p2p_abs_coeff(self, filtered_curves: list) -> float:
        """
        Calculates the average difference in extrema for the list
        of filtered curves.

        Parameters:
            filtered_curves(list): List of the filtered curves.

        Returns:
            (float): The average difference in extrema.
        """
        amp_pn_list = []
        for curve in filtered_curves:
            curve_max = search_max_min(
                self.tick_times, curve, self.max_search_range, "max"
            )
            curve_min = search_max_min(
                self.tick_times, curve, self.min_search_range, "min"
            )
            amp_pn_list.append(curve_max[1] - curve_min[1])
        try:
            av_amp_pn = sum(amp_pn_list) / len(amp_pn_list)
        except Exception as err:
            logger.error(f"Error: {err}")
        return av_amp_pn

    def p2p_coeff_by_base_region(
        self, filtered_curves: list
    ) -> float:
        """get p2p by main region"""
        logger.info("start p2p_coeff_by_base_region")
        coeff_rel = []
        for curve in filtered_curves:
            curve_max = search_max_min(
                self.tick_times, curve, self.max_search_range, "max"
            )
            curve_min = search_max_min(
                self.tick_times, curve, self.min_search_range, "min"
            )
            delta_abs = curve_max[1] - curve_min[1]

            base_max = search_max_min(
                self.tick_times, curve, self.base_region, "max"
            )
            base_min = search_max_min(
                self.tick_times, curve, self.base_region, "min"
            )
            delta_base = base_max[1] - base_min[1]

            coeff_rel.append(delta_abs / delta_base)

        try:
            result = sum(coeff_rel) / len(coeff_rel)
        except Exception as err:
            logger.error(f"Error: {err}")
        return result

    def get_integral(self, curve1: list, curve2: list) -> float:
        """
        Calculates the integral of the absolute difference of curves.

        Parameters:
            curve1(list): List of values from the first curve.
            curve2(list): List of values from the second curve.

        Returns:
            (float): The value of the integral of the absolute difference.
        """
        return np.trapz(np.absolute(np.subtract(curve1, curve2)))

    def filter_curves(self, lb: int, hb: int) -> list:
        """
        Filters curves using the eeg_filters library.

        Parameters:
            lb(int): The low border of the bandpass filter.
            hb(int): The high border of the pandpass filter.

        Returns:
            (list): list of values from the filtered curve.
        """
        # logger.info("start filter_curves")
        # logger.info(f"self.frequency_sample_rate: {self.frequency_sample_rate}")
        # logger.info(f"self.cheb_filter_order: {self.cheb_filter_order}")
        # logger.info(f"self.cheb_ripple: {self.cheb_ripple}")
        filtered_curves = []
        for curve in self.curves:
            filtered_curve = make_filter(
                curve,
                [lb, hb],
                self.frequency_sample_rate,
                self.cheb_filter_order,
                self.cheb_ripple,
            )
            filtered_curves.append(filtered_curve)
        return filtered_curves

    def start(self) -> tuple:
        """
        Initiates the main process of selecting the optimal bandpass filter.
        """
        logger.info("start start")
        heatmap_data = []
        head_row = []
        head_row_created = False
        for lb in range(
            self.filter_low_limit_range[0],
            self.filter_low_limit_range[1] + self.step_low_filter,
            self.step_low_filter,
        ):
            logger.info(f"lb: {lb}")
            data_row = []
            for hb in range(
                self.filter_high_limit_range[0],
                self.filter_high_limit_range[1] + self.step_high_filter,
                self.step_high_filter,
            ):
                logger.info(f"hb: {hb}")
                if not head_row_created:
                    head_row.append(hb)
                filtered_curves = self.filter_curves(lb, hb)
                av_amp_pn = self.get_p2p_coeff(filtered_curves)
                cvc = self.get_curve_var_coeff(filtered_curves)
                optimality_coefficient = av_amp_pn / cvc
                data_row.append(optimality_coefficient)
                self.optimums.append(optimality_coefficient)
                self.filter_by_optimum[optimality_coefficient] = (lb, hb)
            if not head_row_created:
                heatmap_data.append(["-"] + head_row)
                head_row_created = True
            heatmap_data.append([lb] + data_row)
        result_optimum = max(self.optimums)
        return (self.filter_by_optimum[result_optimum], heatmap_data)


def export_data(filepath: str, bandpass: list, data: list) -> None:
    """
    Exports data to file.

    Parameters:
        filepath(str): The path to the file for export data.
        bandpass(list): List of values of the selected bandpass filter.
        data(list): List of values of the optimality parameters.
    """
    with open(filepath, "a", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(bandpass)
        writer.writerows(data)

    return True
