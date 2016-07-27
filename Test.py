import py_emra
import time

Path = r"C:\Users\Matt\Dropbox\PythEMRA\Mcc.xls"

t = time.time()
Results = py_emra.Main.Main(Path,StepNo=25,Enzr=[2],EnsembleSize=50)
elapsed = time.time() - t

print elapsed

py_emra.stabplot.resultProc(Results,Enzr = [2])