#!/bin/bash

pwd=`sed -n '1p' /home/rtk/Desktop/pwd.txt`

cd $pwd

### Hex Result ###

k=1
for i in {1..399..4}
do

	j=`expr $i + 3`

	sed -n "$i","$j"p tcp_first_4_row.txt | awk '{print $2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17}'  > tcp$k.txt

### Analyzing Types ###

	TYPE=`sed -n '2p' tcp$k.txt | awk '{print $1,$2}'`

	if [ "$TYPE" = "86 dd" ]  
	then
		echo "No.$k"
		echo "This is TCP"

	else
		echo "No.$k"	
		echo "This is other protocol"	
		cat tcp$k.txt >$pwd/error_file_tcp$k.txt
	fi
	
	### Analyzing Sources ###

	src1=`sed -n '2p' tcp$k.txt | awk '{print $11,$12,$13,$14,$15,$16}'`
	src2=`sed -n '3p' tcp$k.txt | awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10}'`
	src_ip="$src1 $src2"
	echo "src_ip = $src_ip"

	### Analyzing Destinations ###

	dst1=`sed -n '3p' tcp$k.txt | awk '{print $11,$12,$13,$14,$15,$16}'`
	dst2=`sed -n '4p' tcp$k.txt | awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10}'`
	dst_ip="$dst1 $dst2"
	echo "dst_ip = $dst_ip"

	### Sorting Ports ###

	PORT16=`sed -n '4p' tcp$k.txt | awk 'BEGIN {FS=" "; OFS=""} {for(i=1;i<=NF;++i) {out = out OFS $i}} END {print $13,$14}'`
	echo "PORT16 = $PORT16"
	echo $PORT16 >>tmp1.txt

	k=`expr $k + 1`
done

