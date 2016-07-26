import numpy as np
from scipy import *
from sympy import *

def getInd(S,k,Rev):
	if int(Rev[k,0]) == 0: #get substrates for irreversible
		MetInd = [item for sublist in [[int(j)]*int(-_) for j,_ in enumerate(S[:,k]) if int(_)<0] for item in sublist]
	else: ##get substrates & products for irreversible
		MetInd = [item for sublist in [[int(j)]*int(-_) for j,_ in enumerate(S[:,k]) if int(_)<0] for item in sublist]
		MetIndProd = [item for sublist in [[int(j)]*int(_) for j,_ in enumerate(S[:,k]) if int(_)>0] for item in sublist]
		MetInd.extend(MetIndProd)
	return MetInd

def RxnLaw(S,Params,NumParams,RxnTypes,X,Rev,i):
	rtype = int(RxnTypes[i])
	MetInds = getInd(S,i,Rev)
	Metabs = [X[j] for j in MetInds]
	if rtype in (7,8,9): Metabs.append(symbols('Outer'))#Outer is at the end
	funsel = {1:One_MM_Irr, 2:Two_MM_Irr, 3:One_to_1_Rev, 4:One_to_2_Rev, 5:Two_to_1_Rev, 6:Two_to_2_Rev, 7:Rev_In, 8:Irrev_In, 9:Rev_Out, 10:Irrev_Out}
	rxnfunc = funsel[rtype]
	ParamsToUse = Params[int(NumParams[i]):int(NumParams[i+1])]
	return rxnfunc(Metabs,ParamsToUse)

def One_MM_Irr(X,K):
	Sub1=X[0]; Vmax=K[0]; Km=K[1]
	return Vmax/(1+Km/Sub1)

def Two_MM_Irr(X,K):
	Sub1=X[0]; Sub2=X[1]; Vmax=K[0]; Km1=K[1]; Km2=K[2]
	return Vmax/(Km1*Km2/Sub1/Sub2 + Km1/Sub1 + Km2/Sub2 + 1)

def One_to_1_Rev(X,K):
	Sub1=X[0]; Prod1=X[1]; Vmax=K[0]; Keq=K[1]; Km1=K[2]; Km2=K[3];
	return Vmax*(Sub1-Prod1/Keq)*(1/Km1)/(1+Sub1/Km1+Prod1/Km2)

def One_to_2_Rev(X,K):
	Sub1=X[0]; Prod1=X[1]; Prod2=X[2]; Vmax=K[0]; Keq=K[1]; Km1=K[2]; Km2=K[3]; Km3=K[4];
	return Vmax*(Sub1-Prod1*Prod2/Keq)*(1/Km1)/(1+Sub1/Km1+Prod1/Km2+Prod2/Km3+Prod1*Prod2/Km2/Km3)

def Two_to_1_Rev(X,K):
	Sub1=X[0]; Sub2=X[1]; Prod1=X[2]; Vmax=K[0]; Keq=K[1]; Km1=K[2]; Km2=K[3]; Km3=K[4];
	return Vmax*(Sub1*Sub2-Prod1/Keq)*(1/Km1/Km2)/(1+Sub1/Km1+Sub2/Km2+Sub1*Sub2/Km1/Km2+Prod1/Km3)

def Two_to_2_Rev(X,K):
	Sub1=X[0]; Sub2=X[1]; Prod1=X[2]; Prod2=X[3]; Vmax=K[0]; Keq=K[1]; Km1=K[2]; Km2=K[3]; Km3=K[4]; Km4=K[5];
	N = Vmax*(Sub1*Sub2-(Prod1*Prod2)/Keq)*(1/Km1/Km2)
	D = (1+Sub1/Km1+Sub2/Km2+Sub1*Sub2/Km1/Km2+Prod1/Km3+Prod2/Km4+Prod1*Prod2/Km3/Km4)
	return N/D

def Rev_In(X,K):
	Prod1=X[0]; Sub1=X[1]; Vmax=K[0]; Keq=K[1]; Km1=K[2]; Km2=K[3];
	return Vmax*(Sub1-Prod1/Keq)/Km1/(1+Sub1/Km1+Prod1/Km2)

def Irrev_In(X,K):
	Sub1=X[0]; Vmax=K[0];
	return Vmax*Sub1

def Rev_Out(X,K):
	Sub1=X[0]; Prod1=X[1]; Vmax=K[0]; Keq=K[1]; Km1=K[2]; Km2=K[3];
	return Vmax*(Sub1-Prod1/Keq)/Km1/(1+Sub1/Km1+Prod1/Km2)

def Irrev_Out(X,K):
	Sub1=X[0]; Vmax=K[0];
	return Sub1*Vmax

## 1:One_MM_Irr 
## 2:Two_MM_Irr 
## 3:One_to_1_Rev 
## 4:One_to_2_Rev 
## 5:Two_to_1_Rev 
## 6:Two_to_2_Rev 
## 7:Rev_In 
## 8:Irrev_In 
## 9:Rev_Out 
## 10:Irrev_Out 