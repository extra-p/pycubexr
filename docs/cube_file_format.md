# Cube file format

The [_Cube_ file format](https://www.scalasca.org/software/cube-4.x/download.html), not to be confused with
the [Gaussian CUBE file format](http://paulbourke.net/dataformats/cube/), is a container for performance
measurements.
The _Cube_ file format is defined as part of a greater framework, also called _Cube_. Apart from providing a format for
structuring measured metrics, _Cube_ files also allow for space-efficient storage by
optionally compressing data by using the `*.tar.gz` archive scheme. While there are multiple versions of the _Cube_ file
format, we implemented only a subset of [version 4](https://doi.org/10.1016/j.procs.2015.05.320) as described in this
document.

##### Data stored in _Cube_ files

The main contents of a _Cube_ file are metrics and their measurements. A metric consists of a name, such as _Executing
time_ or _Visits_, and associated measured values.

## Archive structure

_Cube_ files are `*.tar` archives (optionally compressed `*.tar.gz`) with a pre-defined structure. The archive always
contains an `anchor.xml` file describing the performance measurements and providing an index to parse the rest of the
_Cube_ file. Apart from the `anchor.xml` file, the archive also contains the actual metric measurements in a binary
format stored in `*.index` and `*.data` files.

##### Example structure

```
profile.cubex
+- anchor.xml
+- 0.index
+- 0.data
|  ...
+- 10.index
+- 10.data
|  ...
```

### `anchor.xml` file

The `anchor.xml` contains meta-data for the measurements and provide context for analysis. It must always start with a
valid XML header. If the `anchor.xml` file is `gzip`-compressed it is automatically decompressed.
In the following example we see that the XML file consists of different regions these regions are explained in the
following. Note that, most entities in these sections have an ID which is used to reference the entity in other
sections of the XML.

##### Example structure

```xml
<?xml version="1.0" encoding="UTF-8"?>

<cube version="4.4">
 <attr key="Creator" value="Score-P 6.0"/>
 <!-- additional attributes -->
 <metrics>
  <!-- details see below -->
 </metrics>
 <program>
  <!-- details see below -->
 </program>
 <system>
  <!-- details see below -->
 </system>
</cube>
```

#### `<metrics>` section

_Cube_ uses the metric IDs to name the metric data and index files, as shown in
the [example structure](#example-structure). The metric with
ID `0`, for example, results in metric filenames as `0.data` and `0.index`. Another important thing to note is
the `<dtype>`, or data type, of a metric: these data types are needed to parse the actual measurements data files,
`0.data` for example.

We support the following data types:

* CHAR
* COMPLEX
* DOUBLE
* FLOAT
* INT
* INT16
* INT32
* INT64
* INT8
* INTEGER
* MAXDOUBLE
* MINDOUBLE
* SHORT INT
* SIGNED INT
* SIGNED INTEGER
* SIGNED SHORT INT
* UINT16
* UINT32
* UINT64
* UINT8
* UNSIGNED INT
* UNSIGNED INTEGER
* UNSIGNED SHORT INT

The support for these data types is experimental:

* NDOUBLES
* RATE
* TAU_ATOMIC

##### Example

```xml

<metrics>
 <metric id="0" type="EXCLUSIVE">
  <disp_name>Visits</disp_name>
  <uniq_name>visits</uniq_name>
  <dtype>UINT64</dtype>
  <uom>occ</uom>
  <url>@mirror@scorep_metrics-6.0.html#visits</url>
  <descr>Number of visits</descr>
 </metric>
 <metric id="10" type="INCLUSIVE">
  <disp_name>Time</disp_name>
  <uniq_name>time</uniq_name>
  <dtype>DOUBLE</dtype>
  <uom>sec</uom>
  <url>@mirror@scorep_metrics-6.0.html#time</url>
  <descr>Total CPU allocation time</descr>
 </metric>
 <!-- additional metrics -->
</metrics>
 ```

#### `<program>` section

The program section in the XML contains data about the actual program call tree. Here, the `<region>`s
provide a mapping of source code regions, such as functions, to an internal call tree structure, the `<cnode>`s.
A `<cnode>`, on the other hand, signifies an actual call tree node. The `calleeId` references the
corresponding `<region>`. The distinction between `<cnode>` and `<region>` is needed since a function can be called from
different functions, resulting in different
call trees. The regions provide de-duplication here - meaning that a given function must only be described once in a
_region_ instead of for each call tree node . Because the `<cnode>`s signify the call tree of a program, they are
nested. While a `<cnode>` with a given `calleeId` can appear multiple times, the `<cnode>`'s `id` must be unique.
We also support parameters on the cnode but only numeric and string types.

##### Example

```xml

<program>
 <region id="127" mod="/path-to-file/file.cc" begin="2689" end="-1">
  <name>main</name>
  <mangled_name>main</mangled_name>
  <paradigm>compiler</paradigm>
  <role>function</role>
  <url/>
  <descr/>
 </region>
 <region id="250" mod="/path-to-file/file.cc" begin="1389" end="-1">
  <name>CalcElemVolume(double const*, double const*, double const*)</name>
  <mangled_name>_Z14CalcElemVolumePKdS0_S0_</mangled_name>
  <paradigm>compiler</paradigm>
  <role>function</role>
  <url/>
  <descr/>
 </region>
 <!-- additional regions -->

 <cnode id="0" calleeId="2">
  <cnode id="3" calleeId="127">
   <cnode id="7" calleeId="131">
    <cnode id="259" calleeId="250">
     <!-- additional nested call tree nodes -->
    </cnode>
   </cnode>
  </cnode>
  <!-- additional nested call tree nodes -->
 </cnode>
</program>
```

#### `<system>` section

The system section contains information about the machines, processes, and threads that actually executed the
code. Here, a hierarchy can be defined, starting with `<systemtreenode>`s in the root and ending with `<location>`s in
the leaves.

The following figure shows the hierarchy of the `<system>` entries.

```
                    +----------+            +---------+    
                    v          |            v         |    
+----------+    +------------------+    +-----------------+    +------------+
| <system> |--->| <systemtreenode> |--->| <locationgroup> |--->| <location> | 
+----------+    +------------------+    +-----------------+    +------------+
```

Please note measurements are only done at `<location>`s
and that the rest of the `<system>` hierarchy simply provides a mechanism to further structure measurement data.

##### Example

```xml

<system>
 <systemtreenode Id="0">
  <name>machine A</name>
  <class>machine</class>
  <attr key="platform" value="Linux"/>
  <systemtreenode Id="1">
   <name>node A</name>
   <class>node</class>
   <locationgroup Id="0">
    <name>Process</name>
    <rank>0</rank>
    <type>process</type>
    <location Id="0">
     <name>Master thread</name>
     <rank>0</rank>
     <type>thread</type>
    </location>
    <location Id="1">
     <name>OMP thread 1</name>
     <rank>1</rank>
     <type>thread</type>
    </location>
    <!-- additional locations -->
   </locationgroup>
   <!-- additional location groups -->
  </systemtreenode>
 </systemtreenode>
</system>
 ```

### `*.index` metric file

Apart from the `anchor.xml` file, the archive also contains the actual metric measurements in a binary format.
In our example, the archive contains measurements for two metrics with IDs 0 and 10. Through the `anchor.xml` we
can find out the actual names of the metrics with these IDs. Please note that not all metrics defined in
the `anchor.xml` have
corresponding measurements.

As we can see in the following figure, the `*.index` file consists of a header and indices. The header contains the
predefined string `CUBEX.INDEX` to identify the file and provide a sanity check.

##### Header

| UTF-8 text  | Endian check (1 as integer) | Version | Index type | Number of IDs that follow |
|-------------|-----------------------------|---------|------------|---------------------------|
| 11 bytes    | 4 bytes                     | 2 bytes | 1 byte     | 4 bytes                   |
| CUBEX.INDEX | 0x00000001                  | 0x0000  | 0x01       | *N*                       |

##### Indices

| 1st CNode ID | 2nd CNode ID | 3rd CNode ID | ... | *N*-th CNode ID | 
|--------------|--------------|--------------|-----|-----------------|    
| 4 bytes      | 4 bytes      | 4 bytes      | ... | 4 bytes         |

Next, it contains the number 1 encoded as a signed integer. This 1 is useful to check the endianess of the data: when
unpacking the binary 1 into a signed integer, it should equal 1. When it contains a different value, the endianess with
which the value was encoded in the first place is not the same as the endianess of the machine unpacking it - resulting
in wrong values. All subsequent parsed numbers, including the `*.data` files, **MUST** be unpacked using the right
endianess. With a “wrong” endianess, not only the index file will be parsed wrongly but even when the unpacking is
successful, the unpacked measurement data will be wrong in all cases. Next, the `*.index` file contains other control
fields, the version, and index type. The version should correspond to the version defined in `anchor.xml`. The index
type, on the other hand, defines how the index is defined, densely, or sparse. In all our _Cube_ files, even when all
indices were defined, only the sparse index type was used. The last part of the header is the number of elements in the
following list. After the header, the `*.index` file then continues with a list of cnode IDs.

### `*.data` metric file

As we can see in the following table, the `*.data` file also starts with a predefined string. It is either `CUBEX.DATA`
for an uncompressed data file or `ZCUBEX.DATA` for a compressed data file.

#### Uncompressed file

If the file is uncompressed it has the following structure.

##### Header

| UTF-8 text |  
|------------|
| 10 bytes   | 
| CUBEX.DATA | 

##### Data

| 1st Value for 1st CNode ID | ... | *L*-th Value for 1st CNode ID | ... | 1st Value for *N*-th CNode ID | ... | *L*-th Value for *N*-th CNode ID |                       
|----------------------------|-----|-------------------------------|-----|-------------------------------|-----|----------------------------------|                           
| *X* bytes                  | ... | *X* bytes                     | ... | *X* bytes                     | ... | *X* bytes                        |

After the header, the rest of the file contains for each CNode ID the actual measurement values for the metric. To parse
the values, the data type of metric is taken from the `anchor.xml` and its length in bytes *X* is determined. The number
of individual values depends on two factors: (1) the number of cnodes (*N*) as defined in the corresponding `*.index`
file, and (2) the number of locations (*L*) as defined in the `anchor.xml`. The `*.data` file should contain exactly
*N* × *L* values, so one value for each cnode and each location.

#### Compressed file

The compressed file has the following structure.

##### File header

| UTF-8 text  | Number of data headers/segments | 
|-------------|---------------------------------|
| 11 bytes    | 4 bytes                         |
| ZCUBEX.DATA | Must be equal to *N*            |

##### Data headers

| Position of uncompressed data of 1st CNode | Position of compressed data of 1st CNode | Size of compressed data of 1st CNode | ... | Position of uncompressed data of *N*-th CNode | Position of compressed data of *N*-th CNode | Size of compressed data of *N*-th CNode |                       
|--------------------------------------------|------------------------------------------|--------------------------------------|-----|-----------------------------------------------|---------------------------------------------|-----------------------------------------|                           
| 4 bytes                                    | 4 bytes                                  | 4 bytes                              | ... | 4 bytes                                       | 4 bytes                                     | 4 bytes                                 |
|                                            |                                          | *Z*<sub>1</sub>                      |     |                                               |                                             | *Z*<sub>*N*</sub>                       |

##### Data segments

| Compressed data of 1st CNode | ... | Compressed data of *N*-th CNode |                       
|------------------------------|-----|---------------------------------|                           
| *Z*<sub>1</sub> bytes        | ... | *Z*<sub>*N*</sub> bytes         |
|                              |     |                                 |

The `ZCUBEX.DATA` is followed by the _number of data headers/segments_, that are present in this file.
We require that the number of data headers/segments is equal to the number of indices *N*.

The file header is followed by *N* data headers, that describe the position and size of the data segments
In our implementation we ignore the position information, similar to other implementations. Therefore, we require
the order of the data headers to match the order of the data segments. Both must also match the order of the index data
for correct decoding and assignment.

The data segments follow the data headers and each segment has the length specified in the corresponding data header.

The decompression of this file happens as follows: We read all data headers and then in order we decompress all the data
segments into a buffer with the same format as the uncompressed data (with *N* × *L* entries). After that
we read the uncompressed data as described above.

## Acknowledgements

This documentation is partially based on the [report](pyCubexR.pdf) by David Gengenbach about the first version of
pyCubexR.