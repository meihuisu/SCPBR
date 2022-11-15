# The San Jacinto Fault Zone Velocity Model

<a href="https://github.com/sceccode/sjfz.git"><img src="https://github.com/sceccode/sjfz/wiki/images/sjfz_logo.png"></a>

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![GitHub repo size](https://img.shields.io/github/repo-size/sceccode/sjfz)
[![sjfz-ci Actions Status](https://github.com/SCECcode/sjfz/workflows/sjfz-ci/badge.svg)](https://github.com/SCECcode/sjfz/actions)
[![sjfz-ucvm-ci Actions Status](https://github.com/SCECcode/sjfz/workflows/sjfz-ucvm-ci/badge.svg)](https://github.com/SCECcode/sjfz/actions)

## Description

The San Jacinto Fault Zone Velocity Model
2019

## Table of Contents
1. [Software Documentation](https://github.com/SCECcode/sjfz/wiki)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [Credits](#credit)
6. [License](#license)

## Installation

This package is intended to be installed as part of the UCVM framework,
version 22.7.0 or higher. 

This package can also be installed standalone.

$ aclocal
$ autoconf
$ automake --add-missing
$ ./configure --prefix=/dir/to/install
$ make
$ make install

## Usage

### UCVM

As part of [UCVM](https://github.com/SCECcode/ucvm) installation, use 'sjfz' as the model.

### sjfz_query

ASCII query interface(C api) accepts points from stdin with format (lat, lon, dep (m)) and write
data material p roperties to stdout.

## Support
Support for SJFZ is provided by the Southern California Earthquake Center
(SCEC) Research Computing Group.  Users can report issues and feature requests
using SJFZ' github-based issue tracking link below. Developers will also
respond to emails sent to the SCEC software contact listed below.
1. [SJFZ Github Issue Tracker](https://github.com/SCECcode/sjfz/issues)
2. Email Contact: software@scec.usc.edu

## Credits

## Contributing
We welcome contributions to the SJFZ, please contact us at software@scec.usc.edu.

## License
This software is distributed under the BSD 3-Clause open-source license.
Please see the [LICENSE.txt](LICENSE.txt) file for more information.
