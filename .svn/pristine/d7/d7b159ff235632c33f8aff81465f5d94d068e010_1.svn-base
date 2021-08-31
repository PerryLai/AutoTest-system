#!/bin/bash
pwd=`sed -n '1p' /home/pi/Desktop/txt/pwd.txt`
cd $pwd
cat -n tshark_record_pcap.txt > tmp.txt
LINE=`wc -l tmp.txt | awk '{print $1}'`
for ((i=1; i<=$LINE; i++))
do
	empty_row=`sed -n "$i"p tmp.txt | awk '{print $2}'`
	if [ ! -n "$empty_row" ];then
		a=`sed -n "$i"p tmp.txt | awk '{print $1}'`
		echo $a >>empty_row.txt
	fi 
done

LINE=`wc -l empty_row.txt | awk '{print $1}'`
k=1
h=1
for ((i=1; i<=$LINE; i++))
do
	tmp=`sed -n "$i"p empty_row.txt | awk '{print $1}'`
	tmp=`expr $tmp - 1`
	sed -n "$k","$tmp"p tshark_record_pcap.txt | awk '{print $2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17}' >$h.txt
	cat $h.txt | tr '\n' ' ' | sed s/[[:space:]]//g >packet$h.txt
	cat packet$h.txt
	echo "\n"
	k=`expr $tmp + 2`
	sudo rm $h.txt
	h=`expr $h + 1`
done
sudo rm empty_row.txt tshark_record_pcap.txt tmp.txt

