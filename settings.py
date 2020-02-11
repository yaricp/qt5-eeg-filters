# -*- coding: utf-8 -*-

"""Settings for program."""

DEFAULT_STEP_ITER = 25
MAX_ITER_VALUE = 0.005
MAX_STEP_ITER = 50
ORDER = 3               # order for filter
RP = 3                  #  for Chebyshev filter
MAX_START_SEARCH = 0.08
MAX_END_SEARCH = 0.1
MIN_START_SEARCH = 0.18
MIN_END_SEARCH = 0.2
BANDWIDTHS = [
                'source',
                [1, 100],
                [5, 100],
                [10, 100],
                [15, 100],
                [20, 100],
                [1, 200],
                [5, 200],
                [10, 200],
                [15, 200],
                [20, 200],
                [1, 300],
                [5, 300],
                [10, 300],
                [15, 300],
                [20, 300],
                [1, 500],
                [5, 500],
                [10, 500],
                [15, 500],
                [20, 500]
            ]
