for file in *.ext.tre
	do
	echo $file
	cat block1.xml $file.dna $file.morph block2.xml $file.txt $file.param $file.sets sa_ops.xml > $file.sa.xml	
	cat block1.xml $file.dna $file.morph block2.xml $file.txt $file.param $file.sets nosa_ops.xml > $file.nosa.xml
done
