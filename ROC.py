import pandas as pd
import sys
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
import os
import glob

def initializer():
#Load Tree
	tup = []
#	flist = glob.glob('%s' % sys.argv[1])
#	for file in flist:
#		print(file)
	sadf = pd.read_table(sys.argv[1], skiprows=int(sys.argv[2]))
	intburn = int(round(len(sadf)*.3))
	sample_sadf = sadf.loc[intburn:, :]
#	sample_nosadf = nosadf.loc[intburn:, :]
#	sample_nosadf.sort('likelihood', ascending=False, inplace=True)
	sample_sadf.sort('likelihood', ascending=False, inplace=True)
	hpd_val = int(round(len(sample_sadf)*.95))
	hpd_sadf = pd.DataFrame(sample_sadf[:hpd_val])
	med = hpd_sadf.turnoverFBD.median()
#		hpd_nosadf = pd.DataFrame(sample_nosadf[:hpd_val])
	tup.append(med)	
	return(tup)

def export(list_of_tuples):
	df = pd.DataFrame(tup)
	if not os.path.isfile('./%s' % sys.argv[3]):
  		df.to_csv('./%s' % sys.argv[3], header=['Turnover'])
	else:
		df.to_csv('./%s' % sys.argv[3], mode = 'a',  header=None)
	
if __name__ == "__main__":
	file = sys.argv[3]
	tup = initializer()
	export(tup)

	
	