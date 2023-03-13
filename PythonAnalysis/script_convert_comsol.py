from TopasBfieldAnalysis import MagneticFieldMap
from pathlib import Path

data_loc = Path(r'/home/brendan/Dropbox (Sydney Uni)/Projects/Tibaray_planning/field_export_test.txt')

mf = MagneticFieldMap(ComsolFile=data_loc)
mf.ReadComsolData()
mf.sort_field_data()  # crucial step for allowing topas to read correctly
mf.OutputOperaFormat()