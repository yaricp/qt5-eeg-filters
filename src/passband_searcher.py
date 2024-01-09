import numpy as np
from itertools import combinations

from eeg_filters.filters import make_filter, search_max_min


class PassbandSearcher:

    def __init__(
        self,
        curves: list,
        filter_borders: dict,
        tick_times: list,
        where_search_extremums: list,
        check_average: bool,
        check_square: bool,
        config_filter: dict
    ) -> None:
        """
        Initializations of process
        """
        self.filter_low_borders = filter_borders["low"]
        self.filter_low_step = filter_borders["low"][2]
        self.filter_high_borders = filter_borders["high"]
        self.filter_high_step = filter_borders["high"][2]
        self.curves = curves
        self.tick_times = tick_times
        self.where_search_extremums = where_search_extremums
        self.check_average = check_average
        self.check_square = check_square
        
        self.filtered_curves = []
        self.filter_by_optimum = {}
        self.optimums = []
        self.delta = self.get_delta()
        self.config = config_filter

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
            integrals.append(integral)

        if self.check_average:
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
                self.where_search_extremums,
                "max"
            )
            curve_min = search_max_min(
                self.tick_times,
                curve,
                self.where_search_extremums,
                "min"
            )
            deltas.append(curve_max - curve_min)
        return sum(deltas) / len(deltas)

    def get_integral(self, curve1, curve2) -> float:
        """
        Gets integral abs difference of curves
        """
        return np.trapz(np.absolute(np.subtract(curve1, curve2)))

    def filter_curves(self, lb: int, hb: int):
        """
        Filters curves
        """
        filtered_curves = []
        for curve in self.curves:
            filtered_curve = make_filter(
                curve,
                (lb, hb),
                self.config.fs,
                self.config.filter_order,
                self.config.ripple
            )
            filtered_curves.append(filtered_curve)
        return filtered_curves

    def start(self) -> tuple:
        """
        Starts main circle
        """

        for lb in range(
            self.filter_low_borders[0],
            self.filter_low_borders[1],
            self.filter_low_step
        ):
            for hb in range(
                self.filter_high_borders[0],
                self.filter_high_borders[1],
                self.filter_high_step
            ):
                filtered_curves = self.filter_curves(lb, hb)
                reproduct =  self.get_reproduct(filtered_curves)
                delta_extrmums = self.get_delta_extremum(filtered_curves)
                optimum = (reproduct + self.delta) / delta_extrmums
                self.optimums.append(optimum)
                self.filter_by_optimum[optimum] = (lb, hb)
        result_optimum = max(self.optimums)
        return self.filter_by_optimum[result_optimum]