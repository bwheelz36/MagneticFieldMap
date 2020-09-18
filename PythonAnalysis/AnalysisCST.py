import os,sys
import numpy as np
sys.path.append('.')  # make sure python knows to look in the current folder
from TopasBfieldAnalysis import MagneticFieldMap

CSTfileIN = '../Data/ScanningField.txt'  # original data
OperaFileIn = '../Data/ScanningField_Opera.TABLE'  # data converted to opera format. this is read in topas
TopasFileIn = '../Data/TopasFieldsExport'  # data from topas

MF = MagneticFieldMap(CSTfile=None, TopasCompareFile=TopasFileIn, OperaFile=OperaFileIn)
MF.ReadOperaData()  # you can read in CSTfile with MF.
MF.ReadTopasData()
# MF.CompareCSTFieldsToTopasFields()
# MF.CSTversusTopasPlots()

# check some individual points (also pretty slow):
# note that I have chosen these points as they all exist in the topas data (which is pretty sparse), so interpolation error should not be an
# issue
x = [-24, 0, 24]
y = [-12, 0, 12]
z = [-156, 0, 156]
[X, Y, Z] = np.meshgrid(x, y, z)
X = X.flatten()
Y = Y.flatten()
Z = Z.flatten()

MF.CheckXYZpoints(X, Y, Z)