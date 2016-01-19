# coding: utf-8
import dendropy
import pandas
import glob
import sys

treefile = sys.argv[1]
file = sys.argv[2]
def morph_name_append(treefile):
	s = '_'
	list_of_names=[]
	tree = dendropy.Tree.get(file=open(treefile), schema = 'nexus')
	for node in tree.leaf_node_iter():
		if 'X' in node.taxon.label:
			list_of_names.append(s.join([node.taxon.label, str(node.edge_length)]))
	return(list_of_names)
    
def make_morph(name_list):    
	md_val = "?"*1000
	dict_of_dat = {}
	for name in list_of_names:
		dict_of_dat[name] = md_val
	morph_block = open('morph.xml', 'w')
	for val in dict_of_dat.values():
		new_line = val + '\n'
		morph_block.write(new_line)

def format_dna(file):
	s = '_'
	f = open(file)
	lines = f.readlines()
	list_of_lines = []
	for line in lines:
		list_of_lines.append(line.strip().split('       '))
	for line in list_of_lines:
		print(line)	
		line[0] = s.join([str(line[0]), str('0.0')])		
	dna_block = open('dna.xml', 'w')
	for line in list_of_lines[1:]:
		print(line)
		new_line = line[1] + '\n'
		dna_block.write(new_line)

if __name__ == '__main__':
	list_of_names = morph_name_append(treefile)
	make_morph(list_of_names)
	format_dna(file)
