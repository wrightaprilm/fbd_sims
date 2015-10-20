# Author: April Wright
# License: BSD
# Usage:
# python parse_script.py true_tree '*extension'
# in which the true tree is the tree while the true dates, and *extension is the extension
# of the sim replicants. *extension MUST be in quotes, or glob won't expand it right.

# coding: utf-8
import dendropy
from dendropy.calculate import treemeasure
import pandas
import sys
import glob
import numpy as np
right_vecmin = []
right_vecmax = []

def initializer():
#Load Tree
	tree = dendropy.Tree.get(path=sys.argv[1], schema="nexus", rooting="force-unrooted")
#Get Edges from tree
	edges = [edge.length for edge in tree.preorder_edge_iter()]
	edges[0] = 0
#Start a pandas dataframe
	df = pandas.DataFrame(pandas.Series(edges, edges),columns=['true'])
#Use the correct edges as the header
	return(df)

def get_files():
	container = [file for file in glob.glob(sys.argv[2])]
	for file in container:
		print("processing file %s" % file)	
		tree = dendropy.Tree.get(path=file, schema="nexus", extract_comment_metadata=True, rooting="default-unrooted")
		node_hpd = [nd.annotations.findall(name='length_hpd95') for nd in tree.preorder_node_iter()]
		node_med = [nd.annotations.findall(name='length_median') for nd in tree.preorder_node_iter()]
	return(file, node_hpd, node_med)
	
def make_df(node_hpd, df):	

	kvs = [nd.values_as_dict() for nd in node_hpd]
	gnocchi = [kv.values() for kv in kvs]
	max = [line[0][1] for line in gnocchi]
	min = [line[0][0] for line in gnocchi]
	df['min'] = pandas.Series(min, index=df.index)
	df[['min']] = df[['min']].astype(float)
	df['max'] = pandas.Series(max, index=df.index)
	df[['max']] = df[['max']].astype(float)
	df['boolcol'] = df['min'] < df['true']
	df['boolcolmax'] = df['max'] > df['true']
	return(df, right_vecmin, right_vecmax)
	
def add_med(node_med, df):	
	kvs = [nd.values_as_dict() for nd in node_med]
	gnocchi = [kv.values() for kv in kvs]
	med = [float(line[0]) for line in gnocchi]
	df['med'] = pandas.Series(med, index=df.index)
	df['devcol'] = df['med'] - df['true']
	return(df)
	
def count_correct(df):
	min_true = (df.boolcol==True).sum()
	max_true = int((df.boolcolmax==True).sum())
	count = int(df.boolcol.count())
	print(max_true)
	print(min_true)
	return(min_true, max_true)	
	
def io_time(df, file):
	df.to_csv("%s.csv" % file)
	
if __name__ == "__main__":
	df = initializer()
	file, node_hpd, node_med = get_files()
	df, right_vecmin, right_vecmax = make_df(node_hpd, df)
	exported_data = add_med(node_med, df)
	min, max = count_correct(df)
	io_time(exported_data, file)