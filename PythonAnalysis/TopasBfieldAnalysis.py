"""
Convert a CST output into opera format for import into CST
This is just a matter of rewriting the header basically

Eventually this should be part of an automated workflow somewhere
"""
try:
    import logging
    import os,sys
    from time import perf_counter
    import numpy as np
    from matplotlib import pyplot as plt
    from scipy.interpolate import griddata
except ImportError:
    logging.warning('you require several non core libraries to run this code, see import statements')
    sys.exit()


class MagneticFieldMap:

    def __init__(self,CSTfile=None,TopasCompareFile=None,OperaFile=None,Zoffset = None):
        """
        just attaches the file locations to self for later processing
        crude error checking performed
        """

        if not CSTfile is None:
            self.CSTfile = CSTfile
        else:
            logging.info('no CST data provided')

        if not OperaFile is None:
            self.OperaFile = OperaFile
        else:
            logging.info('no Opera data provided')

        if (OperaFile==None) & (CSTfile==None):
            logging.warning('cant do anything with no input data. Exiting')
            sys.exit()
        elif (not OperaFile is None) & (not CSTfile is None):
            logging.warning('only one of the opera and CST files can be read in at a time (use either ReadCSTdata or ReadOperaData)')

        if not TopasCompareFile==None:
            self.TopasCompareFile = TopasCompareFile
        else:
            logging.warning('No topas file provided; will not be able to compare topas data to CST data')

    def ReadCSTdata(self):
        # 1. Read FileIn to numpy array:
        Data = np.loadtxt(self.CSTfile, skiprows=2)

        self.x = Data[:, 0]
        self.y = Data[:, 1]
        self.z = Data[:, 2]
        self.Bx = Data[:, 3]
        self.By = Data[:, 5]
        self.Bz = Data[:, 7]


        # # Print some info about the coordinates
        # print(f'Min x:  {min(x): 1.1f}    Max x: {max(x): 1.1f}')
        # print(f'Min y:  {min(y): 1.1f}    Max y: {max(y): 1.1f}')
        # print(f'Min z:  {min(z): 1.1f}    Max z: {max(z): 1.1f}')
        #
        # IndPoint = 30
        # xtemp = np.unique(x)
        # Xind = (xtemp >= -IndPoint) & (xtemp <= IndPoint)
        # print(f'There are {np.count_nonzero(Xind)} points within {-IndPoint} <= x <= {IndPoint}')
        # IndPoint = 200
        # ztemp = np.unique(z)
        # Zind = (ztemp >= -IndPoint) & (ztemp <= IndPoint)
        # print(f'There are {np.count_nonzero(Zind)} points within {-IndPoint} <= x <= {IndPoint}')

    def ReadOperaData(self):
        """
        To give a fair test to topas should check against the data it's actually reading in; maybe the issue is on my end
        """

        Data = np.loadtxt(self.OperaFile, skiprows=9)

        self.x = Data[:, 0]
        self.y = Data[:, 1]
        self.z = Data[:, 2]
        self.Bx = Data[:, 3]
        self.By = Data[:, 4]
        self.Bz = Data[:, 5]

    def ReadPurgeMagnetOpera(self):
        """
        slightly different format
        :return:
        """

        Data = np.loadtxt(self.OperaFile, skiprows=10)

        self.x = Data[:, 0] * 1e3 # convert to mm
        self.y = Data[:, 1] * 1e3
        self.z = Data[:, 2] * 1e3
        self.Bx = Data[:, 3]
        self.By = Data[:, 4]
        self.Bz = Data[:, 5]

    def ReadTopasData(self):
        """
        Read in topas field data
        """

        Data = np.loadtxt(self.TopasCompareFile)

        self.tpsx = Data[:, 0]
        self.tpsy = Data[:, 1]
        self.tpsz = Data[:, 2]
        # Note: in Geant4's system of units, fields in Tesla are multipled by .001. The factor of 1e3 below is to
        # recover the values in Tesla
        self.tpsBx= Data[:, 3] * 1e3
        self.tpsBy = Data[:, 4] * 1e3
        self.tpsBz = Data[:, 5] * 1e3

    def CheckXYZpoints(self,X,Y,Z):
        """
        Check individual points for input points X,Y,Z
        Note that this interpolates through both data sets
        it is quite slow, and particularly for the topas data if you pick a point which is not close to an included
        point in the rather sparse input data, the linear interpolation will probably fail quite badly.

        Note that this is almost as slow as doing it for an array of points. But it can be a useful spot checker
        """
        tic = perf_counter()
        print('performing griddata interpolation. this is quite slow')
        CST_Bx= griddata((self.x,self.y,self.z), self.Bx, (X,Y,Z), method='linear')
        Topas_Bx = griddata((self.tpsx,self.tpsy,self.tpsz), self.tpsBx, (X,Y,Z), method='linear')
        toc = perf_counter()
        print(f'Interpolating {np.shape(X)[0]} points from a grid of {self.x.shape[0]} points took {toc-tic: 1.1f} seconds')
        ## print a report to the screen:
        inc = 0
        print('Comparison of Bx:')
        print('-----------------')
        print('x    y    z    Bx(Original)    Bx(Topas')
        inc = 0
        for i in X:
            print(f'{X[inc]: 1.0f}    {Y[inc]: 1.0f}    {Z[inc]: 1.0f}    {CST_Bx[inc]: 1.4e}    {Topas_Bx[inc]: 1.4e}')
            inc = inc+1


        # ## the same thing for By and Bz; comment out for speed up

        # tic = perf_counter()
        # CST_By= griddata((self.x,self.y,self.z), self.By, (X,Y,Z), method='linear')
        # Topas_By = griddata((self.tpsx, self.tpsy, self.tpsz), self.tpsBy, (X,Y,Z), method='linear')
        # toc = perf_counter()
        # print(f'Interpolating {np.shape(X)[0]} points from a grid of {self.x.shape[0]} points took {toc-tic: 1.1f} seconds')
        # print('Comparison of By:')
        # print('-----------------')
        # print('x    y    z    By(Original)    Bx(Topas')
        # inc = 0
        # for i in X:
        #     print(f'{X[inc]: 1.0f}    {Y[inc]: 1.0f}    {Z[inc]: 1.0f}    {CST_By[inc]: 1.2e}    {Topas_By[inc]: 1.2e}')
        #     inc= inc+1
        #
        # CST_Bz = griddata((self.x,self.y,self.z), self.Bz, (X,Y,Z), method='linear')
        # Topas_Bz = griddata((self.tpsx, self.tpsy, self.tpsz), self.tpsBz, (X,Y,Z), method='linear')
        # toc = perf_counter()
        # print(f'Interpolating {np.shape(X)[0]} points from a grid of {self.x.shape[0]} points took {toc-tic: 1.1f} seconds')
        # print('Comparison of Bz:')
        # print('-----------------')
        # print('x    y    z    Bz(Original)    Bx(Topas')
        # inc = 0
        # for i in X:
        #     print(f'{X[inc]: 1.0f}    {Y[inc]: 1.0f}    {Z[inc]: 1.0f}    {CST_Bz[inc]: 1.2e}    {Topas_Bz[inc]: 1.2e}')
        #     inc= inc+1

    def CompareCSTFieldsToTopasFields(self):
        """
        This script interpolates the input data (either from the Opera file or the CST file) at every x,y,z position
        in the topas file

        It is quite slow.
        This might be a faster way to do it:
        https://stackoverflow.com/questions/56577658/fast-interpolation-of-a-scattered-dataframe
        """
        # first create a scattered interpolant

        ## interpolate the CST data at the topas coordinates and then compare
        tic = perf_counter()
        print('performing griddata interpolation. this is quite slow (~ 5 minutes)')
        self.grid_Bx = griddata((self.x,self.y,self.z), self.Bx, (self.tpsx,self.tpsy,self.tpsz), method='linear')
        toc = perf_counter()
        print(f'Interpolating {self.tpsx.shape[0]} points from a grid of {self.x.shape[0]} points took {toc - tic: 1.1f} seconds')
        tic = perf_counter()
        self.grid_By = griddata((self.x,self.y,self.z), self.By, (self.tpsx,self.tpsy,self.tpsz), method='linear')
        toc = perf_counter()
        print(f'Interpolating {self.tpsx.shape[0]} points from a grid of {self.x.shape[0]} points took {toc - tic: 1.1f} seconds')
        tic = perf_counter()
        self.grid_Bz = griddata((self.x,self.y,self.z), self.Bz, (self.tpsx,self.tpsy,self.tpsz), method='linear')
        toc = perf_counter()
        print(f'Interpolating {self.tpsx.shape[0]} points from a grid of {self.x.shape[0]} points took {toc - tic: 1.1f} seconds')

    def CSTversusTopasPlots(self):
        """
        Produce plots of the interpoalted CST data versus the topas data
        """

        figure,axs = plt.subplots(1, 3)

        axs[0].scatter(self.grid_Bx,self.tpsBx)
        axs[0].set_ylabel('Topas Data (T)')
        axs[0].set_xlabel('original Data (T)')
        # add 1:1 line
        xlims = axs[0].get_xlim()
        axs[0].plot(xlims, xlims)
        axs[0].grid(True)
        axs[0].set_title('Bx')

        axs[1].scatter(self.grid_By, self.tpsBy)
        axs[1].set_ylabel('Topas Data (T)')
        axs[1].set_xlabel('original Data (T)')
        # add 1:1 line
        xlims = axs[1].get_xlim()
        axs[1].plot(xlims, xlims)
        axs[1].grid(True)
        axs[1].set_title('By')

        axs[2].scatter(self.grid_Bz,self.tpsBz)
        axs[2].set_ylabel('Topas Data (T)')
        axs[2].set_xlabel('original Data (T)')
        plt.tight_layout()
        # add 1:1 line
        xlims = axs[2].get_xlim()
        axs[2].plot(xlims, xlims)
        axs[2].grid(True)
        axs[2].set_title('Bz')

    def OutputOperaFormat(self):
        """
        not set up properly atm
        """
        sys.exit('this doesnt work at the moment')

        FakeField = np.zeros(self.Bx.shape[0])  # for making table of zeros

        # should move this to its own function:
        # # plot Bz(0,0,z)
        # tol = 1
        # xind = abs(x)<=tol
        # yind = abs(y)<=tol
        # ind = np.logical_and(xind,yind)
        # Bx_plot = Bx[ind]
        # By_plot = By[ind]
        # Bz_plot = Bz[ind]
        # B_plot = np.sqrt(Bx_plot**2 + By_plot**2 + Bz_plot**2)
        #
        # z_plot = z[ind]
        # plt.figure()
        # plt.plot(z_plot,Bx_plot,':x')

        #2. Output as opera format:
        PathName, Filetype = os.path.splitext(FileIn)
        PathName, FileName = os.path.split(PathName)
        OutFile = PathName + '/' + FileName + '_Opera.TABLE'


        HeaderString = '\n' + str(np.unique(self.x).shape[0]) + ' ' + str(np.unique(self.y).shape[0]) + ' ' + str(np.unique(self.z).shape[0]) + \
                       '\n 1 X [mm]\n 2 Y [mm]\n 3 Z [mm]\n 4 BX [TESLA]\n 5 BY [TESLA]\n 6 BZ [TESLA]\n 0'  # not sure if this line matters or not
        DataOut = [x,y,z,Bx,By,Bz]
        DataOut = np.transpose(DataOut)
        FormatSpec = ['%11.5f', '%11.5f', '%11.5f', '%11.5e', '%11.5e', '%11.5e']
        np.savetxt(OutFile, DataOut, fmt=FormatSpec, delimiter='      ', header=HeaderString,comments='')

        ## Make fake data of zeros for trouble shooting
        OutFile = PathName + '/' + 'FakeData_Opera.TABLE'
        HeaderString = '\n' + str(np.unique(x).shape[0]) + ' ' + str(np.unique(y).shape[0]) + ' ' + str(
            np.unique(z).shape[0]) + \
                       '\n 1 X [M]\n 2 Y [M]\n 3 Z [M]\n 4 BX [TESLA]\n 5 BY [TESLA]\n 6 BZ [TESLA]\n 0'  # not sure if this line matters or not
        DataOut = [x, y, z, FakeField, FakeField, FakeField]
        DataOut = np.transpose(DataOut)
        FormatSpec = ['%11.5f', '%11.5f', '%11.5f', '%11.5e', '%11.5e', '%11.5e']
        np.savetxt(OutFile, DataOut, fmt=FormatSpec, delimiter='      ', header=HeaderString, comments='')
