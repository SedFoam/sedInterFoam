sedInterFoam
=======

[![Release](https://img.shields.io/badge/release-2406-blue.svg)](http://github.com/SedFoam/sedInterFoam)
[![OpenFOAM v24xx](https://img.shields.io/badge/OpenFOAM-v24xx-brightgreen.svg)](https://openfoam.com/)

This repository provides the sedInterFoam solver (for ESI 2406 openfoam version)

Status
------

The sedInterFoam solver is in development.

Pull requests are encouraged!

Features
--------
A three-dimensional two-phase flow solver with resolution of a free surface, sedInterFoam, has been developed for sediment transport applications. The solver is extended from sedFoam, itself extended from twoPhaseEulerFoam available in the 2.1.0 release of the open-source CFD (computational fluid dynamics) toolbox OpenFOAM.

waves2Foam library needs to be installed to compile sedInterFoam (don't hesitate to follow the recipe of Continuous Integration : .github/workflows/build.yml)

Installation
------------

```bash
cd $WM_PROJECT_USER_DIR
git clone --recurse-submodules https://github.com/mathieu7an/sedInterFoam sedInterFoam
cd sedInterFoam
./Allwclean
./Allwmake
```

Developers
----------

*   Antoine Mathieu
*   Cyrille Bonamy
*   Yeulwoo Kim
*   Tian-Jian Hsu
*   Julien Chauchat

Acknowledgements
----------------

[OpenFOAM](https://www.openfoam.com) is the free, open source CFD
software developed primarily by OpenCFD Ltd since 2004.
The OpenFOAM trademark is owned by OpenCFD Ltd.

