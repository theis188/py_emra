import matplotlib.pyplot as plt
import numpy as np
import time

def resultProc(Results,Enzr=None,save=True,plot=True):
	Ensr = Results['Params']['Ens']
	nEnz = Results['Params']['nEnz']
	Net = Results['Net']
	print Net['Enz']
	print Net['Enz'][Enzr[0]]
	if Enzr == None:
		#nEnz=int(Results[(0,0)]['Up']['V'].shape[0])
		Enzr == range(nEnz)
	
	logXD = [ 0.1*i - 1 for i in range(10) ]
	logXU = [ 0.1*i for i in range(1,11) ]
	XD = [10**i for i in logXD]
	XU = [10**i for i in logXU]
	totalU = [0]*len(XD)
	totalD = [0]*len(XU)
	Fracs = []

	for Enz in Enzr:
		totalU = [0]*len(XD)
		totalD = [0]*len(XU)
		for Ens in range(Ensr):
			res = Results[(Ens,Enz)]
			UUp = res['Up']['U'][Enz]
			print UUp
			stabU = [1 if (i<(float(UUp)+0.1)) else 0 for i in XU]
			totalU = [k+l for k,l in zip(stabU,totalU)]

			UDown = res['Down']['U'][Enz]
			print UDown
			stabD = [1 if (i>(float(UDown)-0.02)) else 0 for i in XD]
			totalD = [k+l for k,l in zip(stabD,totalD)]

		enzFracs = [float(i)/float(Ensr) for i in totalD] + [1] + [float(i)/float(Ensr) for i in totalU]
		if not Fracs: 
			Fracs = np.array(enzFracs)
		else:
			Fracs = np.vstack((Fracs,enzFracs))

	Fracs = np.vstack((logXD+[0]+logXU,Fracs))

	if save:
		model_name = raw_input('Model name?')
		mmddhhmmss = time.strftime("%m")+time.strftime("%d")+time.strftime("%H")+time.strftime("%M")+time.strftime("%S")
		resultName = 'py_emra'+model_name+mmddhhmmss
		Enznames = ' '.join([Net['Enz'][i] for i in Enzr])
		headertext = 'Results from EMRA model of {0}. Enzyme stability in order {1}. First data row is log10 of fold change from reference. Subsequent rows are fraction of stable models.'.format(model_name,Enznames)

		np.savetxt(resultName+'.csv',Fracs,header=headertext,delimiter=',')

	n2plt = len(Enzr)
	if plot:
		for i in range(1,n2plt+1):
			plt.scatter(Fracs[0,:],Fracs[i,:],marker = 'o',facecolors='none',edgecolors='r',s=80)
			plt.plot(Fracs[0,:],Fracs[i,:])
			
			axes = plt.gca()
			axes.set_xlim([-1.1,1.1])
			axes.set_ylim([0,1.2])
			plt.xticks([-1,0,1])
			plt.yticks([0,0.5,1])
			axes.set_xticklabels(['0.1','1','10'])
			axes.set_yticklabels(['0','','1'])
			axes.set_xlabel('Fold-chg. from reference')
			axes.set_ylabel('Fraction of models stable')
			plt.title('EMRA Profile for {0}'.format(Net['Enz'][Enzr[i-1]]))

			plt.show()

#def plot(Fracs,X):
	