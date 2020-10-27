# pyCubexR

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pycubexr?style=plastic)](https://badge.fury.io/py/pycubexr)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/extra-p/pycubexr?style=plastic)
[![PyPI version](https://badge.fury.io/py/pycubexr.png)](https://badge.fury.io/py/pycubexr)
[![PyPI - License](https://img.shields.io/pypi/l/pycubexr?style=plastic)](https://badge.fury.io/py/pycubexr)
![GitHub issues](https://img.shields.io/github/issues/extra-p/pycubexr?style=plastic)
![GitHub pull requests](https://img.shields.io/github/issues-pr/extra-p/pycubexr?style=plastic)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/extra-p/pycubexr/pycubexr?style=plastic)

pyCubexR is a Python package for reading the [Cube4](https://www.scalasca.org/scalasca/software/cube-4.x/download.html) (.cubex) file format. Cube is used as a performance report explorer for Scalasca and Score-P. It is used as a generic tool for displaying a multi-dimensional performance space consisting of the dimensions (i) performance metric, (ii) call path, and (iii) system resource. Each dimension can be represented as a tree, where non-leaf nodes of the tree can be collapsed or expanded to achieve the desired level of granularity. The Cube4 (.cubex) data format is provided for Cube files produced with the [Score-P](https://www.vi-hps.org/projects/score-p) performance instrumentation and measurement infrastructure or the [Scalasca version 2.x](https://www.scalasca.org/scalasca/software/scalasca-2.x/download.html) trace analyzer (and other compatible tools). 

For additional information about the Cube file format and related software, see the [pyCubexR report](./pyCubexR.pdf).

For questions regarding pyCubexR please send a message to <extra-p-support@lists.parallel.informatik.tu-darmstadt.de>.

## Installation

To install the current release, which includes support for Ubuntu and Windows:

```
$ pip install pycubexr
```

To update pyCubexR to the latest version, add `--upgrade` flag to the above commands.

## Usage

The following code provides a minimal example that shows how pyCubexR can be used to read all metrics, callpaths, and measurement values of a .cubex file:

```python
from pycubexr import CubexParser

cubex_file_path = "some/profile.cubex"
with CubexParser(cubex_file_path) as cubex:

    # iterate over all metrics in cubex file
    for metric in cubex.get_metrics():
        metric_values = cubex.get_metric_values(metric=metric)
        
        # return the name of the current metric
        metric_name = metric.name
        
        # iterate over all callpaths in cubex file
        for callpath_id in range(len(metric_values.cnode_indices)):
            cnode = cubex.get_cnode(metric_values.cnode_indices[callpath_id])
            
            # return the current region i.e. callpath
            region = cubex.get_region(cnode)
            
            # return the name of the current region
            region_name = region.name
            
            # return the measurement values for all mpi processes for the current metric and callpath
            cnode_values = metric_values.cnode_values(cnode)
```

Not all .cubex files must contain measurement values for all metrics for each callpath. This is especially true for MPI functions such as MPI_Waitall. In some cases, metrics can be missing. Use the `MissingMetricError` to deal with these exceptions.

```python
from pycubexr import CubexParser
from pycubexr.utils.exceptions import MissingMetricError

cubex_file_path = "some/profile.cubex"
with CubexParser(cubex_file_path) as cubex:

    for metric in cubex.get_metrics():
    
        try:
            metric_values = cubex.get_metric_values(metric=metric)
            
            for callpath_id in range(len(metric_values.cnode_indices)):
                
                cnode = cubex.get_cnode(metric_values.cnode_indices[callpath_id])
                
                # return only a specific number of measurement values for the current metric and callpath
                cnode_values = metric_values.cnode_values(cnode)[:5]
                
                region = cubex.get_region(cnode)
                
                # print the data read from the file
                print('\t' + '-' * 100)
                print(f'\tRegion: {region.name}\n\tMetric: {metric.name}\n\tMetricValues: {cnode_values})')
                
         except MissingMetricError as e:
            # Ignore missing metrics
            pass
```

The call tree of a .cubex file can be displayed with the following code:

```python
from pycubexr import CubexParser

cubex_file_path = "some/profile.cubex"
with CubexParser(cubex_file_path) as cubex:

    # print the call tree of the .cubex file
    cubex.print_calltree() 
```

In special cases, it is also possible that a .cubex file is missing measurement values for some of the callpaths of a metric or that a .cubex file of the same application contains fewer callpaths than another file. These cases need to be handled externally and are not supported by pyCubexR.

## License

[BSD 3-Clause "New" or "Revised" License](LICENSE)
