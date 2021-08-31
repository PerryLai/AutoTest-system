#!/bin/bash

pwd=`sed -n '1p' /home/rtk/Desktop/pwd.txt`

cd $pwd

### Hex Result ###

k=1
LINE=`wc -l icmp_first_4_row.txt | awk '{print int($1)}'`

for ((i=1; i<=$LINE; i+=4))
do

j=`expr $i + 3`

sed -n "$i","$j"p icmp_first_4_row.txt | awk '{print $2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17}'  > icmp$k.txt

### Analyzing Protocol ###

Protocol=`sed -n '2p' icmp$k.txt | awk '{print $1,$2}'`

if [ "$Protocol" = "08 00" ] 
then
	echo "No.$k"	
	echo "This is ICMP"

else
	echo "No.$k"	
	echo "This is other protocol"	
	cat icmp.txt >$pwd/error_file_icmp$k.txt
fi
	
	
### Analyzing Sources ###

src1=`sed -n '2p' icmp$k.txt | awk '{print $15,$16}'`
src2=`sed -n '3p' icmp$k.txt | awk '{print $1,$2}'`
src_ip="$src1 $src2"
echo "src_ip = $src_ip"

### Analyzing Destinations ###

dst_ip=`sed -n '3p' icmp$k.txt | awk '{print $3,$4,$5,$6}'`
echo "dst_ip = $dst_ip"

### Analyzing Types ###

seq_num=`sed -n '3p' icmp$k.txt | awk '{print $13,$14}'`
echo "$seq_num" > seq_num$k.txt

TYPE=`sed -n '3p' icmp$k.txt | awk '{print $7}'`

if [ "$TYPE" = "00" ] 
then
	echo "This is Reply, seq_num is $seq_num" 
	echo "$seq_num" >> result_reply.txt
	
elif [ "$TYPE" = "08" ]
then
	echo "This is Request, seq_num is $seq_num"
	echo "$seq_num" >> result_request.txt

else
	echo "Error Occured."
fi

### Analyzing Sequence Number (Pair or not) ###

if [ "$k" -ne 1 ]
then
	h1=`expr $k - 1`
	h2=1
	h3=-1

	seq_num$h="$pwd/seq_num$h.txt"
	seq_num$k="$pwd/seq_num$k.txt"

	if [ -s "$seq_num$h" ] && [ -s "$seq_num$k" ]
	then
		for h in $(seq $h1 $h3 $h2)
		do
			seq_num1=`sed -n '1p' $pwd/seq_num$h.txt | awk '{print $1,$2}'`
			seq_num2=`sed -n '1p' $pwd/seq_num$k.txt | awk '{print $1,$2}'`
			
			if [ "$seq_num1" == "$seq_num2" ]
			then	
				echo ""		
				echo "----> $h and $k are a pair. <----"
			fi
		done
	fi
fi

echo ""

k=`expr $k + 1`

done
echo "---------------------------"



