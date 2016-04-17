# coding: utf-8
import dendropy
from dendropy.calculate import treemeasure
import collections
import pandas as pd
import sys
import collections 
import glob
import feather
import matplotlib.pyplot as plt
plt.style.use('ggplot')

#Usage:
# python comparisonTree listOfTreesSA 

def initializer():
#Load Tree
	def_tree = dendropy.Tree.get_from_path(sys.argv[1], schema='nexus')
	satree = dendropy.Tree.get_from_path(sys.argv[2], schema='nexus')
	fstring = sys.argv[2]
	fst = fstring.split('.')
	sep = '.'
	newst = sep.join([str(fst[0]), str(fst[1]), 'nosa', str(fst[3]), str(fst[4]), str(fst[5]), str(fst[6])]) 
	nosatree = dendropy.Tree.get_from_path(newst, schema='nexus')
	return(def_tree, satree, nosatree)

def get_ages(comp_tree, sa_tree, nosa_tree):	

	trees = []
	trees.append(comp_tree)
	trees.append(sa_tree)
	trees.append(nosa_tree)
	dub_list = []

	for tree in trees:
		tree.encode_bipartitions()
		tree.calc_node_ages(ultrametricity_precision=False)
		tree.calc_node_root_distances()
		bipartition_labels = collections.defaultdict(list)	
	
		newdf = pd.DataFrame.from_dict(bipartition_labels, orient='index')
		for bp in tree.bipartition_edge_map:
			node = tree.bipartition_edge_map[bp].head_node
			if node.annotations['age_median'].value:
				if float(node.annotations['age_median'].value):
					bipartition_labels[bp].append(node.annotations['age_median'].value)
			if not node.annotations['age_median'].value:
				if node.age > 0.0:
					bipartition_labels[bp].append(node.age)		
				def_df = pd.DataFrame.from_dict(bipartition_labels, orient='index')
				def_df.replace({7.028471:4.68}, inplace=True)
		dub_list.append(bipartition_labels)	
		
	return(def_df, dub_list)

def get_hpd(comp_tree, sa_tree, nosa_tree):	

	trees = []
	trees.append(comp_tree)
	trees.append(sa_tree)
	trees.append(nosa_tree)
	hpd_list = []

	for tree in trees:
		tree.encode_bipartitions()
		bipartition_labels = collections.defaultdict(list)	
	
		newdf = pd.DataFrame.from_dict(bipartition_labels, orient='index')
		for bp in tree.bipartition_edge_map:
			node = tree.bipartition_edge_map[bp].head_node
			if node.annotations['age_hpd95'].value:
				if float(node.annotations['age_hpd95'].value[0]) > 0.0 and float(node.annotations['age_hpd95'].value[1]) > 0.0:
					bipartition_labels[bp].append(node.annotations['age_hpd95'].value)
			if not node.annotations['age_hpd95'].value:
				if node.age > 0.0:
					bipartition_labels[bp].append(node.age)
				def_df = pd.DataFrame.from_dict(bipartition_labels, orient='index')
				def_df.replace({7.028471:4.68}, inplace=True)
		hpd_list.append(bipartition_labels)	
	return(def_df, hpd_list)

def comp_hpd(hpd_df):	

	defcol = hpd_df['def'].tolist()
	sa = hpd_df['sa'].tolist()
	saccess = []
	safailure = []
	nosa = hpd_df['nosa'].tolist()
	nosa = nosa
	nosaccess = []
	nosafailure = []
	
	for value, comp in zip(defcol, sa):
		if float(comp[0]) < float(value) < float(comp[1]):
			saccess.append(1)
		else:
			safailure.append(1)
	print('saccess ratio:', float(len(saccess)/float(len(sa))))
	for value, comp in zip(defcol, nosa):
#		print(comp[0], value, comp[1])
		if float(comp[0]) < float(value) < float(comp[1]):
			nosaccess.append(1)
		else:
			nosafailure.append(1)	
	print('nosaccess ratio:', float(len(nosaccess)/float(len(nosa))))
		
def io_time(def_df, list):
	dflist = []	
	for item in list:
		new_df = pd.DataFrame.from_dict(item, orient='index')
		dflist.append(new_df)	
#		print(dflist)
	mega_df = def_df
#	print('dflist', len(dflist), dflist)
	for item in dflist[1:]:
		mega_df = pd.merge(mega_df, item, left_index=True, right_index=True)
	mega_df.columns = ['def','sa','nosa']	
	mega_df['nosa'] = mega_df['nosa'].astype('float64')
	mega_df['sa'] = mega_df['sa'].astype('float64')
	mega_df.to_csv('%s_means.csv' % sys.argv[2])
	plt.figure()
	dflen=len(mega_df)
	mynum=range(0,dflen)
	mega_df['numeric']=mynum
	ax =mega_df.plot(kind='scatter', x='numeric', y='def',use_index=True,marker= 'x', s=50, label='def')
	ax =mega_df.plot(kind='scatter', x='numeric', y='sa',use_index=True,  s=50, label='sa', ax=ax)
	mega_df.plot(kind='scatter', x='numeric', y='nosa',use_index=True, marker= '^', s=50, label='nosa', ax=ax).set_axis_bgcolor('w')
	plt.savefig('%s_plot.png' % sys.argv[2])
	
def io_timehpd(def_df, list):
	dflist = []	
	for item in list:
		new_df = pd.DataFrame.from_dict(item, orient='index')
		dflist.append(new_df)	
#		print(dflist)
	mega_df = def_df
#	print('dflist', len(dflist), dflist)
	for item in dflist[1:]:
		mega_df = pd.merge(mega_df, item, left_index=True, right_index=True)
	mega_df.columns = ['def','sa','nosa']	
	mega_df.to_csv('%s_hpd.csv' % sys.argv[2])
	return(mega_df)

if __name__ == "__main__":
	comp_tree, sa_tree, nosa_tree = initializer()
	df, dub_list =  get_ages(comp_tree, sa_tree, nosa_tree)
	io_time(df, dub_list)
	df, hpd_list =  get_hpd(comp_tree, sa_tree, nosa_tree)
	hpd_df = io_timehpd(df, hpd_list)
	comp_hpd(hpd_df)