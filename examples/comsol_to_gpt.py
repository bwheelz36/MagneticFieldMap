from pathlib import Path
from MagneticFieldMap import DataLoaders, MagneticFieldMap, DataExporters

'''
this demonstrates reading a file from comsol and export to gpt format
'''

data_loc = Path(r'0p56_shielded.txt')

data = DataLoaders.Comsol_Loader(data_loc)
field = MagneticFieldMap(data)
del data

field.replace_nans(replace_value=0)
DataExporters.GPT_Exporter(field, output_location=data_loc.parent, output_name='gpt_export.dat')