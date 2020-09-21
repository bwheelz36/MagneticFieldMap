import os,sys
import numpy as np
sys.path.append('.')  # make sure python knows to look in the current folder
from TopasBfieldAnalysis import MagneticFieldMap


OperaFileIn = '../Data/PurgMag3D.TABLE'  # data converted to opera format. this is read in topas
TopasFileIn = '../Data/PurgeMagnetTopasExport'  # data from topas

MF = MagneticFieldMap(CSTfile=None, TopasCompareFile=TopasFileIn, OperaFile=OperaFileIn)
MF.ReadPurgeMagnetOpera()  # you can alternatively read in CST file with MF.ReadCSTdata
MF.ReadTopasData()
MF.CompareCSTFieldsToTopasFields()
MF.CSTversusTopasPlots()

# check some individual points (also pretty slow; adding more points does not slow down further):
# note that I have chosen these points as they all exist in the topas data (which is pretty sparse), so interpolation error should not be an
# issue
X = [0.0629755]
Y = [119.909]
Z = [-226.809]


MF.CheckXYZpoints(X, Y, Z)