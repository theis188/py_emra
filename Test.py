import py_emra
import time

Path = "C:\Users\Matt\Dropbox\PythEMRA\Stoich.xls"

t = time.time()
Results = py_emra.Main.Main(Path,StepNo=1)
elapsed = time.time() - t

print elapsed
EnzNo=0
EnsembleNo=0
print Results[(EnsembleNo,EnzNo)]["Up"]