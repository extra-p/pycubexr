from pycubex_parser.classes import Metric


class MissingMetricError(Exception):
    def __init__(self, metric: Metric):
        self.metric = metric
        super().__init__(f'The cubex file does NOT contain an index and/or data for the metric ({metric})')


class CorruptIndexError(Exception):
    def __init__(self, message='Corrupt index.'):
        super().__init__(message)
