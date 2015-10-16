# coding: utf-8
import dendropy
from dendropy.calculate import treemeasure
import pandas
import sys
import glob

def initializer():
#Load Tree
	tree = dendropy.Tree.get(path=sys.argv[1], schema="nexus")
#Get Edges from tree
	edges = [edge.length for edge in tree.preorder_edge_iter()]
#Start a pandas dataframe
	df = pandas.DataFrame(columns=edges)
#Use the correct edges as the header
	cols = df.columns
#And also the first row
	df.append(pandas.Series(edges, index=cols),ignore_index=True)
	return(df, cols)

def get_files(dataframe, index):
	container = glob.glob(sys.argv[2])
	for file in container:
		print("processing file %s" % file)
		tree = dendropy.Tree.get(path=file, schema="nexus")
		edges = [edge.length for edge in tree.preorder_edge_iter()]
		dataframe.append(pandas.Series(edges, index=index),ignore_index=True)
	return(dataframe)
	

def io_time(dataframe):
	dataframe.to_csv()
	

if __name__ == "__main__":
	dataframe, index = initializer()
	export_data = get_files(dataframe, index)
	io_time(export_data)