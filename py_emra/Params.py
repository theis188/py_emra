from LoadXls import *
from PrepareRxns import *
import numpy as np
from scipy import *
from sympy import *
import xlrd

def ParamDet(RxnTypes):
	initparam = 0
	ParamInfo = np.zeros(len(RxnTypes)+1)
	ParamNos = dict([
			(1,2),
			(2,3),
			(3,4),
			(4,5),
			(5,5),
			(6,6),
			(7,4),
			(8,1),
			(9,2),
			(10,1),
			])
	for i in range(0,len(RxnTypes)):
		ParamInfo[i] = int(initparam)
		initparam = int(initparam + ParamNos[RxnTypes[i]])
	ParamInfo[-1] = initparam
	return ParamInfo

## 1:1_MM_Irr
## 2:2_MM_Irr
## 3:1_to_1_Rev
## 4:1_to_2_Rev
## 5:2_to_1_Rev
## 6:2_to_2_Rev
## 7:Rev_In
## 8:Irrev_In
## 9:Rev_Out
## 10:Irrev_Out