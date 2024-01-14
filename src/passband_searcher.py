import numpy as np
from itertools import combinations

from eeg_filters.filters import make_filter, search_max_min


class PassbandSearcher:

    def __init__(
        self,
        curves: list,
        tick_times: list,
        fsr: int,
        max_search_range: tuple,
        min_search_range: tuple,
        **kwargs
    ) -> None:
        """
        Initializations of process
        """
        self.filter_low_limit_range = 1, 30
        self.step_low_filter = 1
        self.filter_high_limit_range = 100, 500
        self.step_high_filter = 10
        self.type_mean = "average"
        self.cheb_filter_order = 3
        self.cheb_ripple = 3

        self.curves = curves
        self.tick_times = tick_times
        self.frequency_sample_rate = fsr
        self.max_search_range = max_search_range
        self.min_search_range = min_search_range

        if "fllr" in kwargs:
            self.filter_low_limit_range = kwargs["fllr"]
        if "filter_low_limit_range" in kwargs:
            self.filter_low_limit_range = kwargs["filter_low_limit_range"]
        self.filter_low_limit_range = [int(x) for x in self.filter_low_limit_range]
        if "fhlr" in kwargs:
            self.filter_high_limit_range = kwargs["fhlr"]
        if "filter_high_limit_range" in kwargs:
            self.filter_high_limit_range = kwargs["filter_high_limit_range"]            
        self.filter_high_limit_range = [int(x) for x in self.filter_high_limit_range]
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
        
        print("TYPE: ", type(self.filter_low_limit_range[0]))

        self.filtered_curves = []
        self.filter_by_optimum = {}
        self.optimums = []
        self.optimum_matrix = {}
        self.delta = self.get_delta()

    def get_delta(self):
        """
        Gets delta for integrals
        """
        return 10

    def get_reproduct(self, filtered_curves: list) -> float:
        """
        Gets reproducibility of filtered curves
        """
        integrals = []
        for curve1, curve2 in combinations(filtered_curves, 2):
            integral = self.get_integral(curve1, curve2)
            print("integral:", integral)
            integrals.append(integral)

        if self.type_mean == "average":
            ave_integral = sum(integrals) / len(integrals)
        # elif self.check_square:
        #     ave_integral = self.get_square_mean(integrals)
        return ave_integral

    def get_delta_extremum(self, filtered_curves: list) -> float:
        """
        Gets average delta extremums
        """
        deltas = []
        for curve in filtered_curves:
            curve_max = search_max_min(
                self.tick_times,
                curve,
                self.max_search_range,
                "max"
            )
            curve_min = search_max_min(
                self.tick_times,
                curve,
                self.min_search_range,
                "min"
            )
            print("max: ", curve_max)
            print("min: ", curve_min)
            deltas.append(curve_max[1] - curve_min[1])
        return sum(deltas) / len(deltas)

    def get_integral(self, curve1, curve2) -> float:
        """
        Gets integral abs difference of curves
        """
        return np.trapz(np.absolute(np.subtract(curve1, curve2)))

    def filter_curves(self, lb: int, hb: int) -> list:
        """
        Filters curves
        """
        filtered_curves = []
        for curve in self.curves:
            filtered_curve = make_filter(
                curve,
                (lb, hb),
                self.frequency_sample_rate,
                self.cheb_filter_order,
                self.cheb_ripple
            )
            filtered_curves.append(filtered_curve)
        return filtered_curves

    def start(self) -> tuple:
        """
        Starts main circle
        """
        print(self.filter_low_limit_range)
        print(self.step_low_filter)
        print(self.filter_high_limit_range)
        print(self.step_high_filter)
        for lb in range(
            self.filter_low_limit_range[0],
            self.filter_low_limit_range[1],
            self.step_low_filter
        ):
            for hb in range(
                self.filter_high_limit_range[0],
                self.filter_high_limit_range[1],
                self.step_high_filter
            ):
                print("lb, hb:",lb, hb)
                filtered_curves = self.filter_curves(lb, hb)
                reproduct =  self.get_reproduct(filtered_curves)
                delta_extrmums = self.get_delta_extremum(filtered_curves)
                optimum = reproduct / delta_extrmums
                self.optimum_matrix[lb] = { hb: optimum }
                self.optimums.append(optimum)
                self.filter_by_optimum[optimum] = (lb, hb)
        result_optimum = min(self.optimums)
        return self.filter_by_optimum[result_optimum]