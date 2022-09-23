import unittest

import numpy as np
from pycubexr.classes.metric_values import MetricValues


class TestOverflowDetection(unittest.TestCase):

    def test_subtract_int_16_8(self):
        type_ = np.int16
        a = np.arange(np.iinfo(type_).min, np.iinfo(type_).max, dtype=type_)
        b = np.full_like(a, 1, dtype=np.int8)
        b = MetricValues._detect_negative_overflow(a, b)
        self.assertSequenceEqual([1] * (np.iinfo(type_).max - np.iinfo(type_).min), b.tolist())
        res = a - b
        self.assertSequenceEqual(list(range(np.iinfo(type_).min - 1, np.iinfo(type_).max - 1)), res.tolist())

    def test_subtract_int_64_8(self):
        type_ = np.int64
        a = np.arange(np.iinfo(type_).min, np.iinfo(type_).min + 10000, dtype=type_)
        b = np.full_like(a, 1, dtype=np.int8)
        b = MetricValues._detect_negative_overflow(a, b)
        self.assertSequenceEqual([0] + [1] * (10000 - 1), b.tolist())
        res = a - b
        self.assertSequenceEqual(
            [np.iinfo(type_).min] + list(range(np.iinfo(type_).min, np.iinfo(type_).min + 10000 - 1)), res.tolist())

    def test_subtract_int_64_16(self):
        type_ = np.int64
        a = np.arange(np.iinfo(type_).min, np.iinfo(type_).min + 1000, dtype=type_)
        b = np.full_like(a, 100, dtype=np.int16)
        b = MetricValues._detect_negative_overflow(a, b)
        self.assertSequenceEqual(list(range(0, 100)) + [100] * (1000 - 100), b.tolist())
        res = a - b
        self.assertSequenceEqual(
            [np.iinfo(type_).min] * 100 + list(range(np.iinfo(type_).min, np.iinfo(type_).min + 1000 - 100)),
            res.tolist())

    def test_subtract_zero_int_64_16(self):
        type_ = np.int64
        a = np.arange(np.iinfo(type_).min, np.iinfo(type_).min + 1000, dtype=type_)
        b = np.zeros_like(a, dtype=np.int16)
        b = MetricValues._detect_negative_overflow(a, b)
        self.assertSequenceEqual([0] * (1000), b.tolist())
        res = a - b
        self.assertSequenceEqual(a.tolist(), res.tolist())

    def test_subtract_negative_int_64_16(self):
        type_ = np.int64
        a = np.arange(np.iinfo(type_).max - 1000, np.iinfo(type_).max + 1, dtype=type_)
        b = np.full_like(a, -100, dtype=np.int16)
        b = MetricValues._detect_negative_overflow(a, b)
        self.assertSequenceEqual([-100] * (1000 - 100) + list(range(-100, 1)), b.tolist())
        res = a - b
        self.assertSequenceEqual(
            list(range(np.iinfo(type_).max - 1000 + 100, np.iinfo(type_).max)) + [np.iinfo(type_).max] * 101,
            res.tolist())
