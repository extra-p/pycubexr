from pycubexr.classes import Metric


class MissingMetricError(Exception):
    def __init__(self, metric: Metric):
        self.metric = metric
        super().__init__('The cubex file does NOT contain an index and/or data for the metric ({})'.format(metric))


class CorruptIndexError(Exception):
    def __init__(self, message='Corrupt index.'):
        super().__init__(message)


class InvalidConversionInstructionError(Exception):
    def __init__(self, message="Received invalid conversion instruction. "
                               "convert_to_exclusive and convert_to_inclusive must not be True at the same time."):
        super().__init__(message)
