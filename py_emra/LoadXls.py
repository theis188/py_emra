import numpy as np
from scipy import *
from sympy import *
import xlrd

def ReadXls(bookname):
	Book = xlrd.open_workbook(filename=bookname)
	Net = {}
	S = Book.sheet_by_name("S")
	S_array = S.col_values(0)
	nrow = len(S_array)
	S_array = np.array(S_array).reshape((len(S_array),1))

	for i in range(1,S.ncols):
		S_array = np.concatenate((S_array,np.array(S.col_values(i)).reshape(nrow,1)),axis=1)

	Net["S"] = S_array

	Vref = Book.sheet_by_name("Vref")
	Vref_array = np.array(Vref.col_values(0)).reshape((S.ncols,1))
	Net["Vref"] = Vref_array
	
	Enz = Book.sheet_by_name("Enz")
	Enz_List = Enz.col_values(0)
	Enz_List = map(str,Enz_List)
	Net["Enz"] = Enz_List

	Met = Book.sheet_by_name("Met")
	Met_List = Met.col_values(0)
	Met_List = map(str,Met_List)
	Net["Met"] = Met_List

	Rev = Book.sheet_by_name("Rev")
	Rev_array = np.array(Rev.col_values(0)).reshape((S.ncols,1))
	Net["Rev"] = Rev_array
	return Net

#v = np.array([[2],[2],[1],[1],[1],[1]])
#print v

#dx = np.dot(S,v)
#print dx