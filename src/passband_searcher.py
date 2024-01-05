from itertool import combinations

from eeg_filters.filters import make_filter, search_max_min


class PassbandSearcher:

    def __init__(
        self,
        curves: list, 
        filter_borders: dict,
        step: intб
        check_average: bool,
        check_square: bool
    ) -> None:
        """
        Initializations of process
        """
        self.filter_low_borders = filter_borders["low"]
        self.filter_high_borders = filter_borders["high"]
        self.step = step
        self.curves = curves
        self.check_average = check_average
        self.check_square = check_square
        self.filter_by_optimum = {}
        self.optimums = []
        self.delta = self.get_delta()

    def get_delta(self):
        """
        Gets delta for integrals
        """
        return 10

    def get_reproduct(self, lb: int, hb: int) -> float:
        """
        Gets reproducibility of filtered curves
        """
        integrals = []
        for curve1, curve2 in combinations(
            self.curves, 2
        ):
            filtred_curve1 = make_filter(
                curve1,
                (lb, hb),
                self.config.fs,
                self.config.filter_order,
                self.config.ripple
            )
            
            filtred_curve2 = make_filter(
                curve2,
                (lb, hb),
                self.config.fs,
                self.config.filter_order,
                self.config.ripple
            )

            integral = self.get_integral(
                filtered_curve1, filtered_curve2
            )
            integrals.append(integral)

        if self.check_average:
            ave_integral = mean(integrals)
        elif self.check_square:
            ave_integral = self.get_square_mean(integrals)
        return ave_integral

    def get_delta_extremum(self) -> float:
        """
        Gets average delta extremums
        """
        deltas = []
        for curve in self.curves:
            max, min = search_max_min(
                self.model.tick_times,
                curve,
                where_find,
                ext
            )
            deltas.append(max - min)
        return mean(deltas)

    def get_integral(self, curve1, curve2) -> float:
        """
        Gets integral abs difference of curves
        """
        return 0

    def start(self) -> tuple:
        """
        Starts main circle
        """

        for lb in range(
            self.filter_low_borders[0],
            self.filter_low_borders[1],
            self.step
        ):
            for hb in range(
                self.filter_high_borders[0],
                self.filter_high_borders[1],
                self.step
            ):
                reproduct =  self.get_reproduct(lb, hb)
                delta_extrmums = self.get_delta_extremum()
                optimum = (reproduct + self.delta)/ delta_extrmums
                self.optimums.append(optimum)
                self.filter_by_optimum[optimum] = (lb, hb)
        result_optimum = max(optimums)
        return self.filter_by_optimum[result_optimum]