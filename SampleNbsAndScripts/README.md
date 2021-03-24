## Description
This directory contains several sample notebooks and py files. The main, source of truth, file is myanalysis_plotly.py. The other ones also likely run, but are older.

## Packages needed
* pandas
* numpy
* plotly
* sodapy
* nbformat
* psutil
* You'll need to install Orca for plotly. See https://plotly.com/python/orca-management. On Windows download the Windows executable. The path is set in the cell '# Do all states & counties' and you'll have to change it to wherever you put the orca executable. If you're on Mac, I don't know how to set it up.
	
	
3. Click the Run Below code-lens at the top of the file (or Ctrl-Shift-P, "Jupyter: Run All Cells")
4. You'll be prompted at the bottom right to install ipykernel. Do so, and then run again.

With any luck it should run all the way through.The script generates a bunch of covid-19 graphs for states, cities, counties, etc from data it pulls from websites like CDC. It then packages them up into a simple html file: CovidAnalysis.html.