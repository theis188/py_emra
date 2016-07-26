from LoadXls import *
from PrepareRxns import *
import numpy as np
from scipy import *
from sympy import *
from Calculus import *
import numpy.linalg

def Main(Path,PertUp = 10.0,PertDown = 0.1,EnsembleSize = 100,RandFloor = 0.1,RandCap = 10,StepNo = 25, fast = False, Enzr=None):
	Net = ReadXls(Path)
	if not Enzr:
		Enzr=range(len(Net["Enz"]))
	Obj = PrepareRxns(Net)

	Xvals = [1]*len(Obj["X"])
	Uvals = [1]*len(Obj["U"])
	Vref = [float(j) for j in Net["Vref"]]
	Obj["JacFun"] = Funify(Obj["Jac"],Obj["X"]+Obj["K"]+Obj["U"]+[symbols('Outer')],[])
	Obj["DFDUFun"] = Funify(Obj["DFDU"],Obj["X"]+Obj["K"]+Obj["U"]+[symbols('Outer')],[])
	Obj["K1SFun"] = Funify(Obj["K1S"],Obj["X"]+Obj["K"]+Obj["U"]+Obj["SYMV"]+[symbols('Outer')],[])
	Obj["VFun"] = Funify([Obj["V"]],Obj["X"]+Obj["K"]+Obj["U"]+[symbols('Outer')],[])

	K = {}
	for Ens in range(EnsembleSize):
		Stable = False
		while not Stable:
			Kvals = [random.random()*(RandCap-RandFloor)+RandFloor for i in Obj["K"]]
			K1vals = [ fun[0](*Xvals+Kvals+Uvals+Vref+[1]) for fun in Obj["K1SFun"] ]
			for i in Obj["NumParams"][:-1]: Kvals[int(i)]=K1vals.pop(0)
			jacval = Funeval(Obj["JacFun"],Xvals+Kvals+Uvals+[1])
			eigV,_ = numpy.linalg.eig(jacval)
			Stable = (np.max(np.real(eigV))<0)
		K[Ens] = Kvals
	reltol = 0.01 if fast else 1e-6
	steps = 500//StepNo if fast else 500
	ODE = scipy.integrate.ode(diffEQ)
	ODE.set_integrator('lsoda', nsteps=steps, rtol=reltol)
	Results = {}
	for Ens in range(EnsembleSize):
		print Ens
		for Enz in Enzr:
			UUp = Uvals[:]; UUp[Enz] = PertUp
			UDown = Uvals[:]; UDown[Enz] = PertDown

			UResults = diffEQBox(ODE,Obj,UUp,Uvals,StepNo,Xvals,K[Ens])
			DResults = diffEQBox(ODE,Obj,UDown,Uvals,StepNo,Xvals,K[Ens])

			UResults['V']=Funeval(Obj['VFun'],UResults['X']+K[Ens]+UResults['U']+[1])
			DResults['V']=Funeval(Obj['VFun'],DResults['X']+K[Ens]+DResults['U']+[1])

			Results[(Ens,Enz)]={'Up':UResults,'Down':DResults}
	
	Results['Params'] = {'StepNo':StepNo,'PertUp':PertUp,'PertDown':PertDown}
	return Results