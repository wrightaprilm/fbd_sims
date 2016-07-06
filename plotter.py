import pandas as pd
import sys
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
import os
import glob

def plotter(sa, nosa):	
	tru = sys.argv[1]
	sa_df = pd.read_csv(sa)
	sa_df['curve'] = tru
	sa_df['ident'] = 'Sampled Ancestor Model'
	nosa_df = pd.read_csv(nosa)
	nosa_df['curve'] = tru
	nosa_df['ident'] = 'Non Sampled Ancestor Model'	
	mega_df = pd.concat([sa_df, nosa_df])
	plt.plot(sa_df.curve, sa_df.Turnover,'r.') # x vs y
	plt.plot(sa_df.Turnover,sa_df.Turnover,'k-')	
	plt.plot(nosa_df.curve,nosa_df.Turnover,'b-')	

	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.savefig('plot.png')	
#	hpd_nosadf['ident'] = 'No Sampled Ancestors'
#	hpd_out = pd.DataFrame([hpd_sadf.min(), hpd_sadf.max(), hpd_sadf.median(),hpd_nosadf.min(), hpd_nosadf.max(), hpd_nosadf.median()])
#	hpd_out.to_csv('%s_hpd_params.csv' % sys.argv[1])
#	mega_df = pd.concat([hpd_sadf, hpd_nosadf])

if __name__ == "__main__":
	nosa = sys.argv[2]
	sa = sys.argv[3]
	plotter(sa, nosa)
	
