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

def prune_func(extant_tree, extinct_tree, rho_val):
    prune_labels = []
    for node in extant_tree.leaf_node_iter():         
        if str(node.taxon.label).startswith('T'):
            rand = random.random()
            if rand > float(rho_val):
                prune_labels.append(node.taxon.label)
    extant_tree.prune_taxa_with_labels(prune_labels)
    extinct_tree.prune_taxa_with_labels(prune_labels)
    return(extant_tree, extinct_tree, prune_labels)

def simulate_seq(pruned, file):
    print(file)
    cmdstring = "seq-gen -mGTR -g4 < %s.pruned > %s.phy" % (file, file)
    os.system(cmdstring)
    seqfile = '%s.phy' % file
    f0 = open(seqfile)
    lines = f0.readlines()[1:]
    lines = [line.strip() for line in lines]
    lines = [str(line.split()[1]) for line in lines]
    dat = dendropy.DnaCharacterMatrix.get_from_path('%s.phy' % file, schema='phylip')
    new_tax = []
    for taxon in dat.taxon_namespace:
        taxon = "<sequence id='seq_%s' taxon='%s' totalcount='4' value='" %(str(taxon).strip('\''), str(taxon).strip('\''))
        new_tax.append(str(taxon))            
    file2='%s.dna' % file 
    f2=open(file2, "w")   
    dict={}
    for name in zip(new_tax, lines):
    	dict[name[0]] = name[1]
    for key, val in dict.items():
        new_line = key+val +"'/>"+'\n'
        f2.write(new_line)
    f2.close()

def simulate_morph(extinct_tree, file):
    md_val = "?"*1000+"'/>"
    dict_of_dat = {}
    list_of_names = []
#    print(extinct_tree.taxon_namespace)
    for node in extinct_tree.leaf_node_iter():         
        if str(node.taxon.label).startswith('X'):
            list_of_names.append("<sequence id='seq_%s' taxon='%s' totalcount='4' value='" \
            %(str(node.taxon.label).strip('\''), str(node.taxon.label).strip('\'')))
    for name in list_of_names:
        dict_of_dat[name] = md_val
    morph_block = open('%s.morph' % file, "w")
    for key, val in dict_of_dat.items():
        new_line = key+val + '\n'
        morph_block.write(new_line)
    morph_block.close()


def get_ages(extinct_tree):
    node_ages = []
    ages = extinct_tree.calc_node_ages(ultrametricity_precision=100)
    extinct_tree.calc_node_root_distances()
    rootage = extinct_tree.seed_node.distance_from_tip()
    for node in extinct_tree.leaf_node_iter(): 
        if str(node.taxon.label).startswith('X'):
            n_string = str(node.taxon.label)+'='+str(rootage - node.root_distance)+','
            node_ages.append(n_string) 
    node_ages[-1] = node_ages[-1].strip(',')                
    return(node_ages, rootage)    

def get_blocks(pruned_extinct, prune_list):
    sib_list = [] 
    used = []
    block_list = []    
    print(prune_list)
    pruned_extinct.prune_taxa_with_labels(prune_list)
    val = 1
    for node in pruned_extinct.leaf_node_iter():
       sibs = node.sibling_nodes()
       for sib in sibs:
           if sib.is_leaf():
               sib_list.append(str(sib.taxon.label))
       block_list.append('<distribution id="%s.prior" \
       spec="beast.math.distributions.MRCAPrior" monophyletic="true" tree="@Tree.t:data"> \
      <taxonset id="%s" spec="TaxonSet">' %(val, val))
       for sib in sib_list:
           if sib not in prune_list:
              if sib not in used:
                 used.append(sib)
                 block_list.append('<taxon id="%s" spec="Taxon"/>' % sib)
              elif sib in used:
                  if sib not in prune_list:
                      block_list.append('<taxon idref="%s" spec="Taxon"/>' % sib)
       block_list.append('</taxonset></distribution>') 
       val = val + 1
    return(block_list)    

def mod_origin(age, file):
    f = open('param.xml')
    red = f.readlines()
    file2='%s.param' % file 
    f2=open(file2, "w")
    for line in red:
        line = re.sub('lowerbound', str(age), line)    
        line = re.sub('upperbound', str(age + 5), line)    
        f2.write(line)
    f2.close()
    
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
    pruned, pruned_extinct, prune_list = prune_func(extant_tree, extinct_tree, rho_val)    
    simulate_seq(pruned, file)
    simulate_morph(extinct_tree, file)
    node_ages, age = get_ages(extinct_tree)
    blocks = get_blocks(pruned_extinct, prune_list)
    mod_origin(age, file)
    write_out(file, pruned, node_ages, blocks)
    