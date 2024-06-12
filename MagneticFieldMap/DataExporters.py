import numpy as np
from abc import ABC, abstractmethod
from MagneticFieldMap import MagneticFieldMap
from pathlib import Path

class _DataExportersBase(ABC):
    """
    Abstract base class to be inherited by other DataExporters
    """

    def __init__(self, MagneticFieldMapInstance: MagneticFieldMap, output_location: (str, Path), output_name: str):

        if not isinstance(MagneticFieldMapInstance, MagneticFieldMap):
            raise TypeError(f'MagneticFieldMapInstance must be an instance of MagneticFieldMap,'
                            f'not {type(MagneticFieldMapInstance)}')
        self._MF = MagneticFieldMapInstance

        self._output_location = Path(output_location)
        self._check_output_location_exists()
        self._output_name = str(output_name)
        self._export_data()

    def _check_output_location_exists(self):
        if not self._output_location.is_dir():
            raise FileNotFoundError(f'output_location should be an existing path;'
                                    f'\n{self._output_location}\n does not exist')

    @abstractmethod
    def _export_data(self):
        """
        this is the method which should actually perform the data export
        :return:
        """
        pass


class Opera_Exporter(_DataExportersBase):

    def _export_data(self):
        HeaderString = '\n' + str(np.unique(self._MF._data.x).shape[0]) + ' ' + str(np.unique(self._MF._data.y).shape[0]) + ' ' + str \
            (np.unique(self._MF._data.z).shape[0]) + \
                       '\n 1 X [M]\n 2 Y [M]\n 3 Z [M]\n 4 BX [TESLA]\n 5 BY [TESLA]\n 6 BZ [TESLA]\n 0'

        DataOut = [self._MF._data.x/1e3, self._MF._data.y/1e3, self._MF._data.z/1e3,
                   self._MF._data.Bx, self._MF._data.By, self._MF._data.Bz]
        DataOut = np.transpose(DataOut)
        FormatSpec = ['%11.5f', '%11.5f', '%11.5f', '%11.5e', '%11.5e', '%11.5e']
        np.savetxt(self._output_location / self._output_name, DataOut, fmt=FormatSpec, delimiter='      ', header=HeaderString, comments='')


class GPT_Exporter(_DataExportersBase):

    def _export_data(self):
        HeaderString = '          x                y              z               Bx               By               Bz '

        DataOut = [self._MF._data.x/1e3, self._MF._data.y/1e3, self._MF._data.z/1e3,
                   self._MF._data.Bx, self._MF._data.By, self._MF._data.Bz]
        DataOut = np.transpose(DataOut)
        FormatSpec = ['%11.5f', '%11.5f', '%11.5f', '%11.5e', '%11.5e', '%11.5e']
        np.savetxt(self._output_location / self._output_name, DataOut, fmt=FormatSpec, delimiter='      ',
                   header=HeaderString, comments='')
