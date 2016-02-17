# coding: utf-8
import dendropy
from dendropy.calculate import treemeasure
import pandas
import sys
import collections 
import glob

def initializer():
#Load Tree
	agehpd = []
	tree = dendropy.Tree.get(path=sys.argv[1], schema="nexus")
#Get Edges from tree
	print(tree)
	tree.resolve_polytomies()
	for node in tree.preorder_node_iter():
			if node.annotations:
				agehpd.append(node.annotations['age_median'].value)				 			
			else:
				agehpd.append('0.0')	
#Start a pandas dataframe
	df = pandas.DataFrame(columns=agehpd)
#Use the correct edges as the header
	cols = df.columns
#And also the first row
	df.append(pandas.Series(agehpd, index=cols),ignore_index=True)
	return(df, cols, tree, agehpd)

def get_files():
	container = glob.glob(sys.argv[2])
	trees = []
	for file in container:
		print("processing file %s" % file)
		tree = dendropy.Tree.get(path=file, schema="nexus")		
		trees.append(tree)
		for tree in trees:
			agehpd = []
			tree.resolve_polytomies()
	return(trees)
	
def get_ages(trees, dataframe, index, agedf):	
	
	for tree in trees:
		agehpd = []
		individ_widths = []	
		wdths = []	
		for node in tree.preorder_node_iter():
			if node.annotations:
				agehpd.append(node.annotations['age_hpd95'].value)
			else:
				agehpd.append([0,0])
		s2 = pandas.Series(agehpd, index=index)
		dataframe = dataframe.append(s2, ignore_index=True)
		for item in agehpd:
			if type(item) == list:
				individ_widths.append((float(item[0]) - float(item[1])))
			wdths.append(individ_widths)
		wd = pandas.DataFrame(wdths)		

	for tree in trees:
		agemed = []
		tree.resolve_polytomies()
		for node in tree.preorder_node_iter():
			if node.annotations:
				agemed.append(node.annotations['age_median'].value)
			else:
				agemed.append(0)	

	for age, med in zip(agemed, agedf): 
		diffs = []
		diff = float(age) - float(med)
		diffs.append(diff)			
		med = pandas.Series(diffs, index=index)
	datamed = dataframe.append(med, ignore_index=True)		
		
	return(dataframe, file, agehpd, datamed, wd)

def comparisons(dataframe, hpds, index):
	successes = []
	for rng in hpds: 
		min = rng[0]
		max = rng[1]
		for value in index:
			if max > value > min:
				successes.append('yes!')
	print len(index)
	print len(successes)
	
	print('Successes:', int(len(successes))/float(len(index)))


def io_time(dataframe, diff_frame, width_frame):
	name = sys.argv[3]
	dataframe.to_csv('%s_edges.csv' % name)
	diff_frame.to_csv('%s_diffs.csv' % name)
	width_frame.to_csv('%s_widths.csv' % name)



if __name__ == "__main__":
	dataframe, index, comp_tree, agedf = initializer()
	trees = get_files()
	export_data, file, hpds, diff_frame, width_frame = get_ages(trees, dataframe, index, agedf)
	comparisons(export_data, hpds, index)
	io_time(export_data, diff_frame, width_frame)