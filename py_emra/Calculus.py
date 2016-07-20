import numpy as np
from scipy import *
from sympy import *
import scipy.integrate
import numpy.linalg

def GetDX(S,V,DX):
	if S.any():
		DX.append(sum ( [ int( j[0] ) * j[1] for j in zip( S[0,:] , V)] ) )
		return GetDX(np.delete(S,0,0),V,DX)
	else: return DX

def Jacobian(DX,X,jac):
	if DX:
		jac.append( [ diff( DX[0] , X[i] ) for i in range( len(X) ) ] )
		return Jacobian(DX[1:],X,jac)
	else: return jac

def Funeval(Fun,Args):
	ret = np.zeros([0,len(Fun[0])])
	for funList in Fun:
		row = [float(fun(*Args)) for fun in funList]
		ret = np.vstack((ret, row))
	return ret

def Funify(Obj,Vars,ret):
	if Obj:
		ret.append([lambdify(Vars,Expr) for Expr in Obj[0]])
		return Funify(Obj[1:],Vars,ret)
	else: return ret

def diffEQBox(ODE,Obj,Uf,Uini,NoSteps,X,K):
	U0 = Uini
	flag = 0
	for i in range(NoSteps):
		U1 = [float(j)+(float(k)-float(l))/NoSteps for j,k,l in zip(U0,Uf,Uini)]
		ODE.set_f_params(U0,U1,Obj,K)
		ODE.set_initial_value(X,0)
		X = list(ODE.integrate(1))
		if [j for j in X if j<0]:
			flag = 1
			print 'Metab Neg Flag'
		U0=U1[:]
		jacval = Funeval(Obj["JacFun"],X+K+U0+[1])
		eigV,_ = numpy.linalg.eig(jacval)
		if np.ndarray.max(np.real(eigV))>1e-6:
			print eigV
			print 'K=',K
			print 'X=',X
			print 'U=',U
			flag = 1
			print 'Instability Flag'
			cc = raw_input('pause...')
		if flag: break
	Results = {'X':X,'U':U0}
	return Results

def diffEQ(t,X,U1,Uf,Obj,K):
	dU = [k-l for k,l in zip(Uf,U1)]
	U = [k+l*t for k,l in zip(U1,dU)]
	X=list(X)
	jacval = Funeval(Obj["JacFun"],X+K+U+[1])
	jacmat = np.matrix(jacval)
	dfdu = Funeval(Obj["DFDUFun"],X+K+U+[1])
	dfduXdu=np.dot(dfdu,dU)
	dx = numpy.linalg.lstsq(jacmat,dfduXdu)
	return -dx[0]
