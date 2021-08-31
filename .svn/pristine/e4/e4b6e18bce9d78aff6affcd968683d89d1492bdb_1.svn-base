#!/bin/bash

set_netns=b_set_netns.sh

sudo rm -r Result

sudo rm final_result.txt

sudo rm error.txt

mkdir Result

times='1'
LINE=`wc -l ip_list.txt | awk '{print int($1)}'`
#echo "LINE = $LINE"

for ((i=1; i<=$LINE; i+=2))
do

echo $times > times.txt

times=` expr $times + 1 `

### grep new data ###
row_net0="$i"
row_net1=`expr $row_net0 + 1`

NS1_NAME=`cat ip_list.txt | awk 'NR==row{print $1}' row="$row_net0"`
NS1_VID=`cat ip_list.txt | awk 'NR==row{print $2}' row="$row_net0"`
NS1_BASE_IF=`cat ip_list.txt | awk 'NR==row{print $3}' row="$row_net0"`
NS1_IP4=`cat ip_list.txt | awk 'NR==row{print $4}' row="$row_net0"`
NS1_MASK4=`cat ip_list.txt | awk 'NR==row{print $5}' row="$row_net0"`
NS1_GW4=`cat ip_list.txt | awk 'NR==row{print $6}' row="$row_net0"`
NS1_IP6=`cat ip_list.txt | awk 'NR==row{print $7}' row="$row_net0"`
NS1_MASK6=`cat ip_list.txt | awk 'NR==row{print $8}' row="$row_net0"`
NS1_GW6=`cat ip_list.txt | awk 'NR==row{print $9}' row="$row_net0"`
NS1_GW_MAC=`cat ip_list.txt | awk 'NR==row{print $10}' row="$row_net0"`

NS2_NAME=`cat ip_list.txt | awk 'NR==row{print $1}' row="$row_net1"`
NS2_VID=`cat ip_list.txt | awk 'NR==row{print $2}' row="$row_net1"`
NS2_BASE_IF=`cat ip_list.txt | awk 'NR==row{print $3}' row="$row_net1"`
NS2_IP4=`cat ip_list.txt | awk 'NR==row{print $4}' row="$row_net1"`
NS2_MASK4=`cat ip_list.txt | awk 'NR==row{print $5}' row="$row_net1"`
NS2_GW4=`cat ip_list.txt | awk 'NR==row{print $6}' row="$row_net1"`
NS2_IP6=`cat ip_list.txt | awk 'NR==row{print $7}' row="$row_net1"`
NS2_MASK6=`cat ip_list.txt | awk 'NR==row{print $8}' row="$row_net1"`
NS2_GW6=`cat ip_list.txt | awk 'NR==row{print $9}' row="$row_net1"`
NS2_GW_MAC=`cat ip_list.txt | awk 'NR==row{print $10}' row="$row_net1"`

### grep old data ###
NS1_NAME_OLD=`cat $set_netns | awk -F "=" 'NR==8 {print $2}'`
NS1_VID_OLD=`cat $set_netns | awk -F "=" 'NR==9 {print $2}'`
NS1_BASE_IF_OLD=`cat $set_netns | awk -F "=" 'NR==10 {print $2}'`
NS1_IP4_OLD=`cat $set_netns | awk -F "=" 'NR==11 {print $2}'`
NS1_MASK4_OLD=`cat $set_netns | awk -F "=" 'NR==12 {print $2}'`
NS1_GW4_OLD=`cat $set_netns | awk -F "=" 'NR==13 {print $2}'`
NS1_IP6_OLD=`cat $set_netns | awk -F "=" 'NR==14 {print $2}'`
NS1_MASK6_OLD=`cat $set_netns | awk -F "=" 'NR==15 {print $2}'`
NS1_GW6_OLD=`cat $set_netns | awk -F "=" 'NR==16 {print $2}'`
NS1_GW_MAC_OLD=`cat $set_netns | awk -F "=" 'NR==17 {print $2}'`

NS2_NAME_OLD=`cat $set_netns | awk -F "=" 'NR==19 {print $2}'`
NS2_VID_OLD=`cat $set_netns | awk -F "=" 'NR==20 {print $2}'`
NS2_BASE_IF_OLD=`cat $set_netns | awk -F "=" 'NR==21 {print $2}'`
NS2_IP4_OLD=`cat $set_netns | awk -F "=" 'NR==22 {print $2}'`
NS2_MASK4_OLD=`cat $set_netns | awk -F "=" 'NR==23 {print $2}'`
NS2_GW4_OLD=`cat $set_netns | awk -F "=" 'NR==24 {print $2}'`
NS2_IP6_OLD=`cat $set_netns | awk -F "=" 'NR==25 {print $2}'`
NS2_MASK6_OLD=`cat $set_netns | awk -F "=" 'NR==26 {print $2}'`
NS2_GW6_OLD=`cat $set_netns | awk -F "=" 'NR==27 {print $2}'`
NS2_GW_MAC_OLD=`cat $set_netns | awk -F "=" 'NR==28 {print $2}'`

### replace data to set_netns.sh ###
sed -i "s/\<${NS1_NAME_OLD}\>/${NS1_NAME}/g" $set_netns
sed -i "s/\<${NS1_VID_OLD}\>/${NS1_VID}/g" $set_netns
sed -i "s/\<${NS1_BASE_IF_OLD}\>/${NS1_BASE_IF}/g" $set_netns
sed -i "s/\<${NS1_IP4_OLD}\>/${NS1_IP4}/g" $set_netns
sed -i "s/\<${NS1_MASK4_OLD}\>/${NS1_MASK4}/g" $set_netns
sed -i "s/\<${NS1_GW4_OLD}\>/${NS1_GW4}/g" $set_netns
sed -i "s/\<${NS1_IP6_OLD}\>/${NS1_IP6}/g" $set_netns
sed -i "s/\<${NS1_MASK6_OLD}\>/${NS1_MASK6}/g" $set_netns
sed -i "s/\<${NS1_GW6_OLD}\>/${NS1_GW6}/g" $set_netns
sed -i "s/\<${NS1_GW_MAC_OLD}\>/${NS1_GW_MAC}/g" $set_netns

sed -i "s/\<${NS2_NAME_OLD}\>/${NS2_NAME}/g" $set_netns
sed -i "s/\<${NS2_VID_OLD}\>/${NS2_VID}/g" $set_netns
sed -i "s/\<${NS2_BASE_IF_OLD}\>/${NS2_BASE_IF}/g" $set_netns
sed -i "s/\<${NS2_IP4_OLD}\>/${NS2_IP4}/g" $set_netns
sed -i "s/\<${NS2_MASK4_OLD}\>/${NS2_MASK4}/g" $set_netns
sed -i "s/\<${NS2_GW4_OLD}\>/${NS2_GW4}/g" $set_netns
sed -i "s/\<${NS2_IP6_OLD}\>/${NS2_IP6}/g" $set_netns
sed -i "s/\<${NS2_MASK6_OLD}\>/${NS2_MASK6}/g" $set_netns
sed -i "s/\<${NS2_GW6_OLD}\>/${NS2_GW6}/g" $set_netns
sed -i "s/\<${NS2_GW_MAC_OLD}\>/${NS2_GW_MAC}/g" $set_netns

### TCP ip addr grep ###
tcp_sender_multi_connection_bind=`cat tcp_sender_multi_connection.py | awk -F '"' 'NR==17 {print $2}'`
tcp_sender_multi_connection_connect=`cat tcp_sender_multi_connection.py | awk -F '"' 'NR==20 {print $2}'`
tcp_listener_multi_connection=`cat tcp_listener_multi_connection.py | awk -F '"' 'NR==13 {print $2}'`

### replace data to tcp listener/sender.py ###
sed -i "s/\<${tcp_sender_multi_connection_bind}\>/${NS1_IP6}/g" tcp_sender_multi_connection.py
sed -i "s/\<${tcp_sender_multi_connection_connect}\>/${NS1_IP6}/g" tcp_sender_multi_connection.py
sed -i "s/\<${tcp_listener_multi_connection}\>/${NS2_IP6}/g" tcp_listener_multi_connection.py

### grep mode ###
mode=`cat ip_list.txt | awk 'NR==row{print int($11)}' row="$row_net0"`
### Start test ###
date=$(date '+%m\%d_%H:%M:%S:%3N')
cd Result
mkdir $date
cd $date
pwd > /home/rtk/Desktop/pwd.txt
cd ..
cd ..


case "$mode" in
1)
	./$set_netns
	sleep 5
	./pkt_test.sh 2>>error.txt
;;

2) 
	./$set_netns	
	sleep 5
	./ping_test.sh 2>>error.txt
;;

3)
	./$set_netns
	sleep 5
	./tcp_test.sh 2>>error.txt
;;

4)
	exit 1
;;

*)
	echo ""	
	echo "Error. Please try again."
;;

esac

done
