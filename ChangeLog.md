Released version 2.0
====================

- Uses NumPy to accelerate parsing and calculation.
- **Breaking change:** returns data as NumPy arrays


- Includes a fix to read CUBE files written by CubeWriter 4.8 that sometimes come with incorrect checksums.
- Includes a bugfix, that switches the paramaters of `convert_to_inclusive` and `convert_to_exclusive` in the `value`
  and `mean` function of `MetricValues`, so that the names and the functions match.  
  The new and also correct signatures are now:  
  `mean(self, cnode: CNode, convert_to_exclusive: bool = False, convert_to_inclusive: bool = False)`  
  `value(self, cnode: CNode, convert_to_exclusive: bool = False, convert_to_inclusive: bool = False)`

Released version 1.2.2
======================

Includes a bugfix, that switches the paramaters of `convert_to_inclusive` and `convert_to_exclusive` in the `value`
and `mean` function of `MetricValues`, so that the names and the functions match.

The new and also correct signatures are now:
`mean(self, cnode: CNode, convert_to_exclusive: bool = False, convert_to_inclusive: bool = False)`
`value(self, cnode: CNode, convert_to_exclusive: bool = False, convert_to_inclusive: bool = False)`

Released version 1.2.1
======================

- Includes a fix to read CUBE files written by CubeWriter 4.8 that sometimes come with incorrect checksums.

Released version 1.2
====================

Includes some bug fixes and the following new features:

- Support for Python 3.9 and 3.10
- CNode parameters
- File/module information

Released version 1.1
====================

- Includes some bug fixes and optimizations, such as improved memory usage and performance.
- Added su

Released version 1.0
====================

- First official release of pyCubexR Python package to read the Cube4 (.cubex) file format.
