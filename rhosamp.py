import dendropy
import random
import sys
import pandas as pd
import re
import os

def read_in(file):
    fileparts = file.split('.')
    e_tree = fileparts[0]+'.ext.'+fileparts[2]
    ex_tree = fileparts[0]+'.PPF.'+fileparts[2]
    extant_tree = dendropy.Tree.get_from_path(e_tree, schema="nexus")    
    extinct_tree = dendropy.Tree.get_from_path(ex_tree, schema="nexus")    
    return(extant_tree, extinct_tree)

def prune_func(tree, rho_val):
    prune_labels = []
    for node in tree.leaf_node_iter():         
        if str(node.taxon.label).startswith('T'):
            if random.random() > rho_val:
                prune_labels.append(node.taxon.label)
    tree.prune_taxa_with_labels(prune_labels)
    return(tree)

def simulate_seq(pruned, file):
    os.system('seq-gen -mGTR -g4 < $file.pruned > $file.phy')
    dat = dendropy.DnaCharacterMatrix.get_from_path('%s.phy' % file, schema='phylip')
    new_tax = []
    for taxon in dat.taxon_set:
        taxon = '<sequence id="seq_%s" taxon="%s" totalcount="4" value="\n' %(taxon, taxon)
        new_tax.append(taxon)            
    back = len(dat)*'"/>\n'
    dat.taxon_namespace=new_tax
    file='%s.back' % file
    f=open(file, "w")
    for x in back:
        f.write(x)
    file='%s.dna' % file 
    f=open(file, "w")   
    for x in dat:
        f.write(x)

def simulate_morph(pruned, file):
    md_val = "?"*1000+'"/>'
    dict_of_dat = {}
    list_of_names = []
    for node in pruned.leaf_node_iter():         
        if str(node.taxon.label).startswith('X'):
            list_of_names.append('<sequence id="seq_%s" taxon="%s" totalcount="4" value="' \
            %(node.taxon.label, node.taxon.label))
    
    for name in list_of_names:
        dict_of_dat[name] = md_val
        
    morph_block = open('%s.morph' % file, "w")
    for val in dict_of_dat.values():
        new_line = val + '\n'
        morph_block.write(new_line)


def get_ages(extinct_tree):
    node_ages = []
    ages = extinct_tree.calc_node_ages(ultrametricity_precision=100)
    extinct_tree.calc_node_root_distances()

    rootage = max(ages)
    for node in extinct_tree.leaf_node_iter(): 
        if str(node.taxon.label).startswith('X'):
            n_string = str(node.taxon.label)+'='+str(rootage - node.root_distance)
            print(n_string)
            node_ages.append(n_string)          
    return(node_ages, rootage)    

def get_blocks(pruned):
    sib_list = [] 
    for node in pruned.leaf_node_iter():
       val = 1
       sibs = node.sibling_nodes()
       for sib in sibs:
           if sib.is_leaf():
               sib_list.append(sib.taxon.label)
       new_sibs = set(sib_list)
       block_list = []
       block_list.append('<distribution id="%s.prior" \
       spec="beast.math.distributions.MRCAPrior" monophyletic="true" tree="@Tree.t:data \
       "> <taxonset id="%s" spec="TaxonSet">' %(val, val))
       for sib in new_sibs:
            block_list.append('<taxon id="%s" spec="Taxon"/>' % sib)
       block_list.append('</taxonset></distribution>') 
       val  =val + 1
    return(block_list)    

def mod_origin(age, file):
    f = open('param.xml')
    red = f.readlines()
    re.sub('lowerbound', 'age', red)    
    re.sub('upperbound', str(age + 5), red)    
    red.write('%s.param' % file)

def write_out(file, pruned, node_ages, blocks):
    print(file)
    pruned.write_to_path('%s.pruned' % file, schema='nexus')
    myfile = '%s.txt' % file
    thefile = open(myfile, 'w')
    for item in node_ages:
        thefile.write("%s\n" % item)
    myfile = '%s.sets' % file
    thefile = open(myfile, 'w')        
    for item in blocks:
        thefile.write("%s\n" % item)

if __name__ == "__main__":
    file = sys.argv[1]
    rho_val = sys.argv[2]
    extant_tree, extinct_tree = read_in(file)
    pruned = prune_func(extant_tree, rho_val)
    simulate_seq(pruned, file)
    simulate_morph(pruned, file)
    node_ages, age = get_ages(extinct_tree)
    blocks = get_blocks(pruned)
    write_out(file, pruned, node_ages, blocks)
    