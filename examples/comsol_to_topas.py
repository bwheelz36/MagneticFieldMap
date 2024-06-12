from pathlib import Path
from MagneticFieldMap import DataLoaders, MagneticFieldMap, DataExporters

'''
this demonstrates reading a file from comsol, sorting it the way topas expects, then exporting in Opera format
which topas can read
'''

data_loc = Path(r'0p56_shielded.txt')

data = DataLoaders.Comsol_Loader(data_loc)
field = MagneticFieldMap(data)
del data

field.replace_nans(replace_value=0)
field.sort_data()  # crucial step to allow topas to process properly!!
DataExporters.Opera_Exporter(field, output_location=data_loc.parent, output_name='demo_export.TABLE')
