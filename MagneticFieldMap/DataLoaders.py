from abc import ABC, abstractmethod
import numpy as np
from pathlib import Path
import warnings

class _DataLoadersBase(ABC):
    """
    DataLoader Abstract Base Class.
    Inherited by new instances of DataLoaders

    :param input_data: location of file to read, or data to read
    :param particle_type: optional parameter if phase space format does not specify particle.
        particle type is a string matching a particle name from particle config
    :param units:  optionally specify units by passing a unit set
    """

    def __init__(self, input_data_loc: (str, Path), header_rows: (int, None) = None):

        self.x = None
        self.y = None
        self.z = None
        self.Bx = None
        self.By = None
        self.Bz = None
        self._input_data_loc = input_data_loc
        self._header_rows = header_rows
        self._import_data()
        self._check_loaded_data()


    @abstractmethod
    def _import_data(self):
        """
        this function loads the data
        :return:
        """
        pass

    def _check_loaded_data(self):
        """
        check that the phase space data
        1. contains the required columns
        2. doesn't contain any non-allowed columns
        3. doesn't contain NaN
        4. "particle id" should be unique
        """
        required_fields = ['x', 'y', 'z', 'Bx', 'By', 'Bz']
        for field in required_fields:
            assert hasattr(self, field)
            assert getattr(self, field) is not None


class Opera_Loader(_DataLoadersBase):

    def _import_data(self):
        """
        To give a fair test to topas should check against the data it's actually reading in; maybe the issue is on my end
        """

        if self._header_rows is None:
            self._header_rows = 10

        Data = np.loadtxt(self._input_data_loc, skiprows=self._header_rows)

        self.x = Data[:, 0]
        self.y = Data[:, 1]
        self.z = Data[:, 2]
        self.Bx = Data[:, 3]
        self.By = Data[:, 4]
        self.Bz = Data[:, 5]


class Comsol_Loader(_DataLoadersBase):

    def _import_data(self):

        if self._header_rows is None:
            self._header_rows = 9

        Data = np.loadtxt(self._input_data_loc, skiprows=self._header_rows)
        self.x = Data[:, 0]
        self.y = Data[:, 1]
        self.z = Data[:, 2]
        self.Bx = Data[:, 3]
        self.By = Data[:, 4]
        self.Bz = Data[:, 5]


class CST_Loader(_DataLoadersBase):

    def _import_data(self):

        if self._header_rows is None:
            self._header_rows = 2
        Data = np.loadtxt(self._input_data_loc, skiprows=self._header_rows)

        self.x = Data[:, 0]
        self.y = Data[:, 1]
        self.z = Data[:, 2]
        self.Bx = Data[:, 3]
        self.By = Data[:, 5]
        self.Bz = Data[:, 7]


