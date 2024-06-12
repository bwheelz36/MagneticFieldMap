# Topas magnetic field prep

This code allows the import, analysis and output of magnetic field maps.
Extensible base classes are provided to enable the addition of new import/ export formats.

The main use case and the impetus for development was to generate mapped field data in a format
that [topas](https://www.topasmc.org/) would accept. But the architecture should allow for further analysis methods
to be added as needed.

## examples

see examples folder

## installation

this code is not hosted on pypi, but you can install by 

1. cloning this repository
2. doing `pip install .` (preferable inside a virtual environment) or `poetry install`
