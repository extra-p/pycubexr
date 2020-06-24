# pyCubexR

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pycubexr?style=plastic)](https://badge.fury.io/py/pycubexr)
[![PyPI version](https://badge.fury.io/py/pycubexr.png)](https://badge.fury.io/py/pycubexr)
[![PyPI - License](https://img.shields.io/pypi/l/pycubexr?style=plastic)](https://badge.fury.io/py/pycubexr)

pyCubexR is a Python package for reading the [Cube4](https://www.scalasca.org/scalasca/software/cube-4.x/download.html) (.cubex) file format. Cube is used as a performance report explorer for Scalasca and Score-P. It is used as a generic tool for displaying a multi-dimensional performance space consisting of the dimensions (i) performance metric, (ii) call path, and (iii) system resource. Each dimension can be represented as a tree, where non-leaf nodes of the tree can be collapsed or expanded to achieve the desired level of granularity. The Cube4 (.cubex) data format is provided for Cube files produced with the [Score-P](https://www.vi-hps.org/projects/score-p) performance instrumentation and measurement infrastructure or the [Scalasca version 2.x](https://www.scalasca.org/scalasca/software/scalasca-2.x/download.html) trace analyzer (and other compatible tools). 

For question regarding pyCubeR please send a message to <extra-p@lists.parallel.informatik.tu-darmstadt.de>.

## Installation

To install the current release:

```
$ pip install pycubexr
```

## Usage

```python
from pycubexr import CubexParser

cubex_file_path = "some/profile.cubex"
with CubexParser(cubex_file_path) as cubex:
    for metric in cubex.get_metrics():
        metric_values = cubex.get_metric_values(metric=metric)
        cnode = cubex.get_cnode(metric_values.cnode_indices[0])
        region = cubex.get_region(cnode)
        cnode_values = metric_values.cnode_values(cnode.id)
```

## License

[BSD 3-Clause "New" or "Revised" License](LICENSE)
