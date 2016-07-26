import py_emra
import time

Path = r"C:\Users\Matt\Dropbox\PythEMRA\Stoich.xls"

t = time.time()
Results = py_emra.Main.Main(Path,StepNo=25)
elapsed = time.time() - t

print elapsed


#EnzNo=2
#EnsembleNo=0
#stabplot(Results,EnzNo)
#print Results[(EnsembleNo,EnzNo)]["Up"]

EnzNo=0
EnsembleNo=0
print Results[(EnsembleNo,EnzNo)]["Up"]

