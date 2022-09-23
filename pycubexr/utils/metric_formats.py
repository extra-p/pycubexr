import numpy

METRIC_FORMATS = {
    'CHAR': numpy.uint8,
    'COMPLEX': numpy.complex128,
    'DOUBLE': numpy.float64,
    'FLOAT': numpy.float64,  # Is defined as float 64
    # 'HISTOGRAM': lambda n: str(int(n)) + 'd',
    'INT': numpy.int32,
    'INT16': numpy.int16,
    'INT32': numpy.int32,
    'INT64': numpy.int64,
    'INT8': numpy.int8,
    'INTEGER': numpy.int64,
    'MAXDOUBLE': numpy.float64,
    'MINDOUBLE': numpy.float64,
    'NDOUBLES': lambda n: (numpy.float64, (n,)),
    'RATE': [('main', numpy.float64), ('time', numpy.float64)],
    # 'SCALE_FUNC': 'P',
    'SHORT INT': numpy.int16,
    'SIGNED INT': numpy.int32,
    'SIGNED INTEGER': numpy.int64,
    'SIGNED SHORT INT': numpy.int16,
    'TAU_ATOMIC': [('n', numpy.uint32), ('min', numpy.float64), ('max', numpy.float64), ('sum', numpy.float64),
                   ('sum2', numpy.float64)],  # TODO check if uint32 is correct
    'UINT16': numpy.uint16,
    'UINT32': numpy.uint32,
    'UINT64': numpy.uint64,
    'UINT8': numpy.uint8,
    'UNSIGNED INT': numpy.uint32,
    'UNSIGNED INTEGER': numpy.uint64,
    'UNSIGNED SHORT INT': numpy.uint16,
}
