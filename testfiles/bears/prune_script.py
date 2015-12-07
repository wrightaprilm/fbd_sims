#! /usr/bin/env python

import dendropy

import sys

tree = dendropy.Tree.get(path = sys.argv[1], schema = "nexus", preserve_underscores=True)
        
no_good_taxa = ['Parictis_montanus_33.5',
'Zaragocyon_daamsi_21.4',
'Ballusia_elmensis_15',
'Ursavus_primaevus_14.81',
'Ursavus_brevihinus_16.4',
'Indarctos_vireti_8.20',
'Indarctos_arctoides_9.2',
'Indarctos_punjabiensis_7.25',
'Ailurarctos_lufengensis_7',
'Agriarctos_spp_6.35',
'Kretzoiarctos_beatrix_11.5',
'Arctodus_simus_1.296',
'Ursus_abstrusus_3.55',
'Ursus_spelaeus_0.1385']

good_taxa = ['Canis_lupus_0',
'Phoca_largha_0',
'Ailuropoda_melanoleuca_0',
'Tremarctos_ornatus_0',
'Helarctos_malayanus_0',
'Melursus_ursinus_0',
'Ursus_americanus_0',
'Ursus_arctos_0',
'Ursus_thibetanus_0',
'Ursus_maritimus_0',]

#for taxon in no_good_taxa:
tree.retain_taxa_with_labels(['Canis_lupus_0',
'Phoca_largha_0',
'Ailuropoda_melanoleuca_0',
'Tremarctos_ornatus_0',
'Helarctos_malayanus_0',
'Melursus_ursinus_0',
'Ursus_americanus_0',
'Ursus_arctos_0',
'Ursus_thibetanus_0',
'Ursus_maritimus_0',])
	
print(tree)	
print(tree.as_ascii_plot())

new_name = sys.argv[1] + '.pruned'
tree.write(path = new_name, schema = 'nexus')

        
