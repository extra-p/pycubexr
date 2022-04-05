import copy
import sys
from abc import abstractmethod, ABC
from numbers import Real

from typing import List, Dict, Callable, Union, Sequence, Any, cast, Iterable


class BaseValue(ABC):
    @abstractmethod
    def _add(self, other):
        pass

    @abstractmethod
    def _sub(self, other):
        pass

    @abstractmethod
    def neutral(self):
        pass

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        other = self._check(other)
        if other is None:
            return NotImplemented
        return self._add(other)

    def __sub__(self, other):
        other = self._check(other)
        if other is None:
            return NotImplemented
        return self._sub(other)

    def _check(self, other):
        if not isinstance(other, type(self)):
            if other == 0:
                return self.neutral()
            return None
        return other

    @abstractmethod
    def __float__(self):
        pass

    def try_convert(self):
        return self


class ConvertsToRealValue(BaseValue, ABC):

    def __float__(self):
        return float(self.try_convert())

    @abstractmethod
    def try_convert(self):
        pass


class MinMaxValue(ConvertsToRealValue, ABC):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value

    def neutral(self):
        return self

    def __eq__(self, other):
        if self is other:
            return True
        elif isinstance(other, MinMaxValue):
            return self.value == other.value
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, MinMaxValue):
            return self.value < other.value
        else:
            return NotImplemented

    def __repr__(self):
        return f"{type(self).__name__}({self.value})"

    def __float__(self):
        # reimplemented for performance reasons
        return self.value

    def try_convert(self):
        return self.value


class MinValue(MinMaxValue):
    def _add(self, other):
        value = min(self, other)
        if isinstance(value, MinMaxValue):
            value = value.value
        return MinValue(value)

    def _sub(self, other):
        value = max(self, other)
        if isinstance(value, MinMaxValue):
            value = value.value
        return MinValue(value)


class MaxValue(MinMaxValue):
    def _add(self, other):
        value = max(self, other)
        if isinstance(value, MinMaxValue):
            value = value.value
        return MaxValue(value)

    def _sub(self, other):
        value = min(self, other)
        if isinstance(value, MinMaxValue):
            value = value.value
        return MaxValue(value)


class ComplexValue(complex, BaseValue):
    @classmethod
    def __new__(cls, *args, **kwargs) -> 'ComplexValue':
        args = [args[0]] + list(args[1])
        return cast(ComplexValue, super().__new__(*args, **kwargs))

    def __add__(self, other) -> 'ComplexValue':
        return self._add(other)

    def __sub__(self, other) -> 'ComplexValue':
        return self._sub(other)

    def _add(self, other):
        val = complex.__add__(self, other)
        if val is NotImplemented:
            return NotImplemented
        return ComplexValue((val,))

    def _sub(self, other):
        val = complex.__sub__(self, other)
        if val is NotImplemented:
            return NotImplemented
        return ComplexValue((val,))

    def neutral(self):
        return 0

    def __float__(self):
        return abs(self)


class TauAtomicValue(ConvertsToRealValue):
    def __init__(self, value):
        if isinstance(value, TauAtomicValue):
            self.n = value.n
            self.min = MinValue(value.min)
            self.max = MinValue(value.max)
            self.sum = value.sum
            self.sum2 = value.sum2
        else:
            n, min_, max_, sum_, sum2 = value
            self.n = n
            self.min = MinValue(min_)
            self.max = MinValue(max_)
            self.sum = sum_
            self.sum2 = sum2

    def _sub(self, other):
        return TauAtomicValue((
            self.n - other.n,
            self.min - other.min,
            self.max - other.max,
            self.sum - other.sum,
            self.sum2 - other.sum2,
        ))

    def neutral(self):
        return TauAtomicValue((
            0,
            self.min,
            self.max,
            0,
            0,
        ))

    def _add(self, other):
        return TauAtomicValue((
            self.n + other.n,
            self.min + other.min,
            self.max + other.max,
            self.sum + other.sum,
            self.sum2 + other.sum2,
        ))

    def try_convert(self):
        if self.n == 0:
            return self.sum / (self.n + 1e-256)
        else:
            return self.sum / self.n


class RateValue(ConvertsToRealValue):
    def __init__(self, value):
        if isinstance(value, RateValue):
            self.main = value.main
            self.duration = value.duration
        else:
            self.main, self.duration = value

    def _sub(self, other):
        return RateValue((
            self.main - other.main,
            self.duration - other.duration
        ))

    def neutral(self):
        return RateValue((0, 0))

    def _add(self, other):
        return TauAtomicValue((
            self.main + other.main,
            self.duration + other.duration
        ))

    def try_convert(self):
        if self.duration == 0:
            return sys.float_info.max if self.main > 0 else -sys.float_info.max
        else:
            return self.main / self.duration


class NValue(ConvertsToRealValue):
    def __init__(self, value):
        if isinstance(value, NValue):
            self.values = copy.copy(value.values)
        else:
            self.values = value

    @property
    def n(self):
        return len(self.values)

    def _sub(self, other):
        assert self.n == other.n
        return NValue(
            [x - y for x, y in zip(self.values, other.values)]
        )

    def neutral(self):
        return NValue(
            [0] * self.n
        )

    def _add(self, other):
        assert self.n == other.n
        return NValue(
            [x + y for x, y in zip(self.values, other.values)]
        )

    def try_convert(self):
        return sum(self.values)


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
    'MAXDOUBLE': MaxValue,
    'MINDOUBLE': MinValue,
    'COMPLEX': ComplexValue,
    'TAU_ATOMIC': TauAtomicValue,
    'RATE': RateValue,
    'NDOUBLES': NValue,
    # 'HISTOGRAM': HistogramValue
}

# def _determine_max_uint64_for_double():
#     for i in range(0xFFFF_FFFF_FFFF_FFFF, 0, -1):
#         if int(float(i)) < int(float(0xFFFF_FFFF_FFFF_FFFF)):
#             # print(f"{i:x}")
#             return i

MAX_UINT64_DOUBLE = 0xFFFF_FFFF_FFFF_FBFF  # Maximal UINT64 that can be cast to double and back without exceeding UINT64


def convert_type(type_: str, parameters: tuple, values: Iterable[Union[tuple, Real]],
                 allow_full_uint64_values: bool = False) -> List[Union[BaseValue, Real]]:
    if type_ in VALUE_MAPPING:
        val_cls = VALUE_MAPPING[type_]
        # if 'type_params' in signature(val_cls).parameters:
        #     # noinspection PyArgumentList
        #     return [val_cls(v, type_params=parameters) for v in values]
        # else:
        return list(map(val_cls, values))
    elif isinstance(values, List):
        if not allow_full_uint64_values and type_ == 'UINT64' or type_ == 'UNSIGNED INTEGER':
            # simulates undefined behavior when casting uint64_t to double to uint64_t in cubelib
            for i in range(len(values)):
                if values[i] > MAX_UINT64_DOUBLE:
                    values[i] = 0
        return values
    elif not allow_full_uint64_values and type_ == 'UINT64' or type_ == 'UNSIGNED INTEGER':
        # simulates undefined behavior when casting uint64_t to double to uint64_t in cubelib
        return [0 if value > MAX_UINT64_DOUBLE else value for value in values]
    else:
        return list(values)
