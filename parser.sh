sed 's/(//g' *.ppf_info.cal > stripped 
sed -i 's/)//g' stripped 
cut -f -2 stripped > cal
sed -i 's/,/\t/g' cal
sed -i '2,$s/^/-t\t/g' cal
rm stripped
cut -f 5- *ppf_info.cal > samp_prop
sed -i  '1d' samp_prop
sum=0; len=0; while read num ; do sum=$(($sum + $num)); len=$((len +1)); done < samp_prop ; echo $sum; echo $len
expr $sum/$len > prop
