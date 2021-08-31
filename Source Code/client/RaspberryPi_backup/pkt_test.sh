#!/bin/bash

#set -e
set_netns=b_set_netns.sh
pwd=`sed -n '1p' /home/rtk/Desktop/pwd.txt`

### IP address ###
echo ""
echo "----------Starting to grep IP address-----------"
echo ""
grep 'NS1_IP4=' $set_netns > $pwd/net0_ipv4.txt
grep 'NS2_IP4=' $set_netns > $pwd/net1_ipv4.txt
NS1_IP4=`awk -F '=' '{print $2s}' $pwd/net0_ipv4.txt`
NS2_IP4=`awk -F '=' '{print $2s}' $pwd/net1_ipv4.txt`
cd $pwd
echo "NS1_IP4 = $NS1_IP4"
echo "NS2_IP4 = $NS2_IP4"
sudo rm net0_ipv4.txt net1_ipv4.txt

grep 'NS1_IP6=' /home/rtk/Desktop/$set_netns > net0_ipv6.txt
grep 'NS2_IP6=' /home/rtk/Desktop/$set_netns > net1_ipv6.txt
NS1_IP6=`awk -F '=' '{print $2s}' net0_ipv6.txt`
NS2_IP6=`awk -F '=' '{print $2s}' net1_ipv6.txt`
echo "NS1_IP6 = $NS1_IP6"
echo "NS2_IP6 = $NS2_IP6"
sudo rm net0_ipv6.txt net1_ipv6.txt

### Ping net0 -> net1 ###
#echo ""
#echo "----------Starting to ping net0 -> net1----------"
sudo ip netns exec net0 ping -i 0.1 $NS2_IP4 >ping_record.txt &

### tshark Setting ###
sudo tshark -D >tshark_record.txt
sed -e '/eth/!d' tshark_record.txt >eth.txt
sed -n '1p' eth.txt  >eth0.txt
sed -n '2p' eth.txt  >eth1.txt
eth0=`awk -F '.' '{print $1s}' eth0.txt`
eth1=`awk -F '.' '{print $1s}' eth1.txt`
sudo rm tshark_record.txt eth.txt eth0.txt eth1.txt

### Analyzing eth0 ###
sudo timeout 30 tshark -i eth0 -x -f icmp -c 10 > icmp.txt 
grep '00[0-3]0' icmp.txt >icmp_first_4_row.txt

cd ..
cd ..

./icmp_analyze.sh > $pwd/icmp_analyze_result.txt

cd $pwd

#echo "Analyze finished."
#echo "---------------------------"

### Stopping Ping ###
#echo "Start to kill ping."
#echo "---------------------------"

sudo ip netns exec net0 ps aux | grep ping >kill_ping.txt 

PING_PID=`sed -n "2p" kill_ping.txt | awk {'print $2s'}` >killed_PID.txt
sudo kill $PING_PID 
sudo rm kill_ping.txt killed_PID.txt

#echo "Kill ping Finished"

#--------------------------------------------------------------------------------

diff -y result_request.txt result_reply.txt > compare.txt

sed -i '/>/d' compare.txt
sed -i '/</d' compare.txt

ping_success=`wc -l compare.txt | awk {'printf $1'}`
ping_all=`wc -l result_reply.txt | awk {'printf $1'}`
sudo rm compare.txt

ratio=`awk 'BEGIN{printf ('$ping_success'/5)*100}'`

#echo "---------------------------"
echo ""
echo "Ping $ratio% are succeed."
echo ""
 
times=`sed -n '1p' /home/rtk/Desktop/times.txt`

if [ "$ratio" -gt 79 ]
then		
	echo "Test $times: Mode 1: SUCCESS." | tee -a /home/rtk/Desktop/final_result.txt
else	
	echo "Test $times: Mode 1: Failed. Only $ratio% Passed." | tee -a /home/rtk/Desktop/final_result.txt
fi
