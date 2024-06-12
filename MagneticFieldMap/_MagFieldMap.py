import numpy as np
from matplotlib import pyplot as plt
from .DataLoaders import _DataLoadersBase
from copy import deepcopy



class MagneticFieldMap:

    def __init__(self, data_loader: _DataLoadersBase):

        if not isinstance(data_loader, _DataLoadersBase):
            raise TypeError(f'must be instantiated with a valid object'
                            f'from DataLoaders, not {type(data_loader)}')
        self._data = deepcopy(data_loader)
        # don't need data_loader anymore
        del data_loader

    def Plot00z(self):
        """
        plot B(0,0,z) versus Z for the input data (be it opera or CST file)
        :return:
        """

        tol = 20
        xind = abs(self._data.x) <= tol
        yind = abs(self._data.y) <= tol
        ind = np.logical_and(xind,yind)
        Bx_plot = self._data.Bx[ind]
        By_plot = self._data.By[ind]
        Bz_plot = self._data.Bz[ind]
        B_plot = np.sqrt(Bx_plot**2 + By_plot**2 + Bz_plot**2)

        z_plot = self._data.z[ind]
        plt.figure()
        plt.plot(z_plot, B_plot, ':x')
        plt.title('Bx(0,0,z) extracted from input data')
        plt.show()

    def PlotCoords(self):
        """
        plot X, Y, Z versus indice
        does topas assume some form of ordering for the indices??
        :return:
        """
        figure,axs = plt.subplots(1,3)

        axs[0].plot(self._data.x)
        axs[1].plot(self._data.y)
        axs[2].plot(self._data.z)
        plt.show()

    def replace_nans(self, replace_value=0):

        self._data.Bx[np.isnan(self._data.Bx)] = replace_value
        self._data.By[np.isnan(self._data.By)] = replace_value
        self._data.Bz[np.isnan(self._data.Bz)] = replace_value

    def sort_data(self):
        """
        Resort the data ordering to match what topas expects. you MUST do this before attempting a topas import
        :return:
        """
        my_list = [self._data.x, self._data.y, self._data.z]
        my_list = np.array(my_list)
        ind = np.lexsort((my_list[2, :], my_list[1, :], my_list[0, :]))

        self._data.x = self._data.x[ind]
        self._data.y = self._data.y[ind]
        self._data.z = self._data.z[ind]
        self._data.Bx = self._data.Bx[ind]
        self._data.By = self._data.By[ind]
        self._data.Bz = self._data.Bz[ind]


