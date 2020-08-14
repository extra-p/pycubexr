from abc import abstractmethod, ABC
from typing import List, Dict, Type


class BaseValue(ABC):
    @abstractmethod
    def add(self, other):
        pass

    @abstractmethod
    def sub(self, other):
        pass

    @abstractmethod
    def neutral(self):
        pass

    def __iadd__(self, other):
        return self.__add__(other)

    def __isub__(self, other):
        return self.__sub__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        other = self._check(other)
        if other is None:
            return NotImplemented
        return self.add(other)

    def __sub__(self, other):
        other = self._check(other)
        if other is None:
            return NotImplemented
        return self.sub(other)

    def _check(self, other):
        if not isinstance(other, type(self)):
            if other == 0:
                return self.neutral()
            return None
        return other

    def try_convert(self):
        return self


class MinMaxValue(BaseValue, ABC):
    def __init__(self, value):
        if isinstance(value, MinMaxValue):
            self.value = value.value
        else:
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

    def try_convert(self):
        return self.value


class MinValue(MinMaxValue):
    def add(self, other):
        return MinValue(min(self, other))

    def sub(self, other):
        return MinValue(max(self, other))


class MaxValue(MinMaxValue):
    def add(self, other):
        return MaxValue(max(self, other))

    def sub(self, other):
        return MaxValue(min(self, other))


VALUE_MAPPING: Dict[str, Type] = {
    'MAXDOUBLE': MaxValue,
    'MINDOUBLE': MinValue,
}


def convert_type(type, values) -> List:
    if type in VALUE_MAPPING:
        val_cls = VALUE_MAPPING[type]
        return [val_cls(v) for v in values]
    else:
        return list(values)
