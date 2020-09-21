# Topas Scripts

This contains the topas script files needed to run the examples.

The 'PurgingMagnet' is very similar to the one included with topas, except I have removed all time dependant behavior for simplicity.
THe 'MinimumExample' is to read in my CST data (converted to opera format) and run a 10 MeV electron through it.
Note that I have made the geometry of the component the field is mapped to exactly the same as thee export geometry in CST - a 400 mm cylinder of radius 30 mm. So, I don't know why this isn't mapping the field properly. but both the trajectory of the particles and the re-exported B fields suggest the the B field has not been correctly mapped.
