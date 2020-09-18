import os,sys
import numpy as np
sys.path.append('.')  # make sure python knows to look in the current folder
from TopasBfieldAnalysis import MagneticFieldMap


OperaFileIn = '../Data/PurgMag3D.TABLE'  # data converted to opera format. this is read in topas
TopasFileIn = '../Data/PurgeMagnetTopasExport'  # data from topas

MF = MagneticFieldMap(CSTfile=None, TopasCompareFile=TopasFileIn, OperaFile=OperaFileIn)
MF.ReadPurgeMagnetOpera()  # you can read in CSTfile with MF.
MF.ReadTopasData()
MF.CompareCSTFieldsToTopasFields()
MF.CSTversusTopasPlots()

# check some individual points (also pretty slow):
# you should choose points which actually exist in the topas data (which is pretty sparse), so interpolation error should not be an
# issue
# x = [-24, 0, 24]
# y = [-12, 0, 12]
# z = [-156, 0, 156]
# [X, Y, Z] = np.meshgrid(x, y, z)
# X = X.flatten()
# Y = Y.flatten()
# Z = Z.flatten()

X = [0]
Y = [62]
Z = [-83]
MF.CheckXYZpoints(X, Y, Z)