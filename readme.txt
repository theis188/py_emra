This is the readme for the py_emra package, developed in Python 2.7. To use on your system, copy the py_emra folder to the folder you are working in, or your library folders. Check your library paths with the following python commands: 'import sys','sys.path'

py_emra is the Python module for Ensemble Modeling Robustness Analysis. For more information about the package and the algorithm, see the biorXiv paper here: http://biorxiv.org/content/early/2016/07/21/065177

You must have the following packages installed:

+numpy
+scipy
+matplotlib
+xlrd

To install a convenient version of Python with these packages preloaded, check out Anaconda: https://www.continuum.io/downloads

These are the functions contained. Access these functions by first writing 'import py_emra' in your python Script.

+++ py_emra.Main.Main(Path,**kwargs) +++

This is the main function performing all the math, model construction, parameter sampling and integration. It ouputs results in a dictionary which can be saved and plotted.

Arguments:

Path = String of path to your model (r'C:\path\pathy\model.xls')
**kwargs
PertUp = 10.0 - magnitude of upward perturbation 
PertDown = 0.1 - magnitude of downward perturbation
EnsembleSize = 100 Number of models to simulate
RandFloor = 0.1 - minimum for enzyme parameter values
RandCap = 10 - maximum for enzyme parameter values
StepNo = 25 - number of integration steps. lower number of steps will not harm numerical integrity of results as integration is handled by a variable step-size but it will affect resolution of instability detection.
fast = False - decreases accuracy and increases speed of integration if set to True
Enzr=[All Enzymes] - list of enzyme indices to perturb

Output:
Dictionary containing resulting perturbation, metabolite, and 

+++ py_emra.stabplot.resultProc(Results,**kwargs) +++

The is the main results processing, plotting, and saving function. Will produce stability profiles and save results in csv format.

Results = Results variable as from py_emra.Main.Main
**kwargs
Enzr = list of enzymes to plot & save
save=True - whether or not to save a csv of results
plot=True - whether or not to plot results

+++Model format+++

+Currently py_emra supports .xls based models. The .xls should contain 'S','Enz','Met','Vref' & 'Rev' tabs.

'S'=Stoichiometric matrix of integers defining model network.
'Enz'=Column of enzyme names in same order as 'S'
'Met'=Column of metab names in same order as 'S'
'Vref'=Column of reference steady state enzyme fluxes defining a steady state for network defined in 'S'
'Rev'=Column of enzyme reversibilities (0 = irrev, 1 = reversibile).

***See Test.py for example of how the functions work together***

***See Mcc.xls for example of model format.***

***See MCC.png for example of EMRA stability plot.***