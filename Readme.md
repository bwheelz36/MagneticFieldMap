# Topas magnetic field analysis

I'm having some trouble with importing a magnetic field map into topas. 
This code is my troubleshooting.

I am putting all this code here because I am a bit stuck (see figure 1) and I am hoping someone can figure out what I have done wrong!

## Directory structure

1. Data: All necessary text data files. Original data is from CST, which 
is converted into the opera format for read in to topas. The topas data is
the same data read back out of topas. Unfortunately I cannot get these to match.
2. PythonAnalysis: my python code to analyse all the data
3. TopasExtensions: I've made some minor changes to the topas mapped field file
such that it prints a lot of data to the screen. 
4. TopasScripts: this contains my topas script to read in the Field data. It also contains the purgingMagnet example, which has been edited to use the topas extension above
