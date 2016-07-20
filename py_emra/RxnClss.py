from LoadXls import *
from PrepareRxns import *
import numpy as np
from scipy import *
from sympy import *
import xlrd

def RxnClass(Net):
	num_enz = int(Net["S"].shape[1])
	RxnTypes = np.zeros(num_enz)
	for i in range(0,num_enz):
		S_col = Net["S"][:,i]
		num_subs = int(abs(sum(S_col[S_col < 0])))
		num_prods = int(sum(S_col[S_col > 0]))
		rev = int(Net["Rev"][i,0])
		#print "num subs is", num_subs
		#print "num prods is", num_prods
		#print "rev is", rev
		if rev == 0:
			if num_prods != 0:
				if num_subs == 1:
					RxnTypes[i] = 1
				elif num_subs == 2:
					RxnTypes[i] = 2
				elif (num_subs == 0) & (num_prods == 1):
					RxnTypes[i] = 8
			elif (num_prods == 0) & (num_subs == 1):
				RxnTypes[i] = 10
		elif rev == 1:
			if num_subs == 1:
				if num_prods == 1:
					RxnTypes[i] = 3
				elif num_prods == 2:
					RxnTypes[i] = 4
				elif num_prods == 0:
					RxnTypes[i] = 9
			elif num_subs == 2:
				if num_prods == 1:
					RxnTypes[i] = 5
				elif num_prods == 2:
					RxnTypes[i] = 6
			elif (num_subs == 0) & (num_prods == 1):
				RxnTypes[i] = 7
	return RxnTypes

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