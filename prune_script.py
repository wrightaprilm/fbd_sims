import dendropy

import sys

tree = dendropy.Tree.get(path = sys.argv[1], schema = "nexus", preserve_underscores=True)
retain_labels = []
for node in tree.leaf_node_iter():
	if 'T' in node.taxon.label:
		retain_labels.append(node.taxon.label)

tree.retain_taxa_with_labels(retain_labels)
print(tree)
print(tree.as_ascii_plot())

new_name = sys.argv[1] + '.pruned'
tree.write(path = new_name, schema = 'nexus')
		
