# The San Jacinto Fault Zone velocity model (sjfz)

<a href="https://github.com/sceccode/sjfz.git"><img src="https://github.com/sceccode/sjfz/wiki/images/sjfz_logo.png"></a>

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![GitHub repo size](https://img.shields.io/github/repo-size/sceccode/sjfz)
[![sjfz-ci Actions Status](https://github.com/SCECcode/sjfz/workflows/sjfz-ci/badge.svg)](https://github.com/SCECcode/sjfz/actions)
[![sjfz-ucvm-ci Actions Status](https://github.com/SCECcode/sjfz/workflows/sjfz-ucvm-ci/badge.svg)](https://github.com/SCECcode/sjfz/actions)

The San Jacinto Fault Zone velocity model

## Installation

This package is intended to be installed as part of the UCVM framework,
version 25.x or higher. 

## Contact the authors

If you would like to contact the authors regarding this software,
please e-mail software@scec.org. Note this e-mail address should
be used for questions regarding the software itself (e.g. how
do I link the library properly?). Questions regarding the model's
science (e.g. on what paper is the SJFZ based?) should be directed
to the model's authors, located in the AUTHORS file.

## To build in standalone mode

To install this package on your computer, please run the following commands:

<pre>
  aclocal
  autoconf
  automake --add-missing
  ./configure --prefix=/dir/to/install
  make
  make install
</pre>


### sjfz_query

ASCII query interface(C api) accepts points from stdin with format (lat, lon, dep (m)) and write
data material p roperties to stdout.
