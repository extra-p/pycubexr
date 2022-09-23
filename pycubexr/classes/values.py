import copy
import sys
from abc import abstractmethod, ABC
from numbers import Real, Number

from typing import List, Dict, Callable, Union, Sequence, Any, cast, Iterable

import numpy as np


class CubeValues:

    def __init__(self, values):
        self._values: np.ArrayLike = values

    def __add__(self, other):
        if isinstance(other, type(self)):
            return type(self)(self._values + other._values)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, type(self)):
            return type(self)(self._values - other._values)
        else:
            return NotImplemented

    def __repr__(self):
        return f"{type(self).__name__}({self._values})"

    def __len__(self):
        return len(self._values)

    def __getitem__(self, item):
        return type(self)(self._values[item])

    def sum(self):
        return type(self)(np.sum(self._values))

    def mean(self):
        return type(self)(np.mean(self._values))

    def astype(self, type):
        return self._values.astype(type)

    def copy(self):
        return type(self)(self._values.copy())


class MinMaxValues(CubeValues, ABC):

    @classmethod
    @abstractmethod
    def agg_command(cls, a, b, out=None):
        pass

    def _check(self, other):
        if all(other._values == 0):
            return self
        if not isinstance(other, type(self)):
            return NotImplemented
        else:
            return None

    def __add__(self, other):
        other_values = self._check(other)
        if other_values is not None:
            return other_values
        return type(self)(self.agg_command(self._values, other._values))

    def __sub__(self, other):
        other_values = self._check(other)
        if other_values is not None:
            return other_values
        return type(self)(self.agg_command(self._values, other._values))

    def __iadd__(self, other):
        other_values = self._check(other)
        if other_values is not None:
            return other_values
        self.agg_command(self._values, other._values, out=self._values)
        return self

    def __isub__(self, other):
        other_values = self._check(other)
        if other_values is not None:
            return other_values
        self.agg_command(self._values, other._values, out=self._values)
        return self


class MinValues(MinMaxValues):
    agg_command = np.minimum

    def sum(self):
        return MinValues(self._values.min())

    def mean(self):
        return MinValues(self._values.min())


class MaxValues(MinMaxValues):
    agg_command = np.maximum

    def sum(self):
        return MaxValues(self._values.max())

    def mean(self):
        return MaxValues(self._values.max())


class ComplexValues(CubeValues):

    def astype(self, type):
        if type != complex:
            return np.absolute(self._values).astype(type)
        return self._values.astype(type)


class TauAtomicValues(CubeValues):
    def astype(self, type):
        raise NotImplementedError()


class RateValues(CubeValues):

    def astype(self, type):
        raise NotImplementedError()


# class HistogramValue(BaseValue):
#     def __init__(self, value):
#         if isinstance(value, HistogramValue):
#             self.min, self.max = value.min, value.max
#             self.values = copy.copy(value.values)
#         else:
#             self.min, self.max = value[0:2]
#             self.values = value[2:]
#
#     @property
#     def n(self):
#         return len(self.values)
#
#     def sub(self, other):
#         return self
#
#     def neutral(self):
#         return HistogramValue(
#             [-math.inf, math.inf]
#         )
#
#     def add(self, other):
#         return HistogramValue(
#             [min(self.min, other.min), max(self.max, other.max)] +
#             self.values + other.values
#         )


VALUE_MAPPING: Dict[str, Callable[[Union[Sequence[Any], Any]], Any]] = {
    'MAXDOUBLE': MaxValues,
    'MINDOUBLE': MinValues,
    'COMPLEX': ComplexValues,
    'TAU_ATOMIC': TauAtomicValues,
    'RATE': RateValues,
    # 'NDOUBLES': NValues,
    # 'HISTOGRAM': HistogramValue
}

# def _determine_max_uint64_for_double():
#     for i in range(0xFFFF_FFFF_FFFF_FFFF, 0, -1):
#         if int(float(i)) < int(float(0xFFFF_FFFF_FFFF_FFFF)):
#             # print(f"{i:x}")
#             return i

MAX_UINT64_DOUBLE = 0xFFFF_FFFF_FFFF_FBFF  # Maximal UINT64 that can be cast to double and back without exceeding UINT64


def convert_type(type_: str, parameters: tuple, values: Iterable[Union[tuple, Real]],
                 allow_full_uint64_values: bool = False) -> List[Union[CubeValues, Real]]:
    if type_ in VALUE_MAPPING:
        val_cls = VALUE_MAPPING[type_]
        # if 'type_params' in signature(val_cls).parameters:
        #     # noinspection PyArgumentList
        #     return [val_cls(v, type_params=parameters) for v in values]
        # else:
        return val_cls(values)
    elif isinstance(values, np.ndarray):
        if not allow_full_uint64_values and type_ == 'UINT64' or type_ == 'UNSIGNED INTEGER':
            if any(values > MAX_UINT64_DOUBLE):
                # simulates undefined behavior when casting uint64_t to double to uint64_t in cubelib
                values = np.require(values, requirements='W')
                values[values > MAX_UINT64_DOUBLE] = 0
        return values
    elif not allow_full_uint64_values and type_ == 'UINT64' or type_ == 'UNSIGNED INTEGER':
        # simulates undefined behavior when casting uint64_t to double to uint64_t in cubelib
        return [0 if value > MAX_UINT64_DOUBLE else value for value in values]
    else:

        return list(values)
