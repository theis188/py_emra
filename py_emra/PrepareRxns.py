from LoadXls import *
from PrepareRxns import *
import numpy as np
from scipy import *
from sympy import *
from RxnClss import *
from Params import *
from RxnLaw import *
from Calculus import *
import xlrd

def PrepareRxns(Net):

	num_met = int(Net["S"].shape[0])
	num_enz = int(Net["S"].shape[1])
	
	Obj = {}

	X = [symbols("x"+str(i)) for i in range(0,num_met)]
	Obj["X"] = X
	
	RxnTypes = RxnClass(Net)
	Obj["RxnTypes"] = RxnTypes

	NumParams = ParamDet(RxnTypes)
	Obj["NumParams"] = ParamDet(RxnTypes)
	
	K = [symbols("k"+str(i)) for i in range(0,int(Obj["NumParams"][-1]))]
	Obj["K"] = K

	U = [symbols("U"+str(i)) for i in range(num_enz)]
	Obj["U"] = U

	SYMV = [symbols("V"+str(i)) for i in range(num_enz)]
	Obj["SYMV"] = SYMV

	V = [RxnLaw(Net["S"],K,NumParams,RxnTypes,X,Net["Rev"],i) for i in range(num_enz)]
	V = [j[0]*j[1] for j in zip(U,V)]
	Obj["V"] = V
	
	DX = GetDX(Net["S"],V,[])
	Obj["DX"] = DX

	Jac = Jacobian(DX,X,[])
	Obj["Jac"] = Jac

	DFDU = Jacobian(DX,U,[])
	Obj["DFDU"] = DFDU

	K1S=[solvers.solve(V[j] - SYMV[j], K[ int(NumParams[j]) ]) for j in range(num_enz)]
	Obj["K1S"]=K1S

	#Nullspace = Null(Net["S"].T)
	return Obj
