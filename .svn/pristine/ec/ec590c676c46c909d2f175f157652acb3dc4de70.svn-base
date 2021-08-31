#!/bin/bash

#set -e
set_netns=b_set_netns.sh
./tcp.sh

pwd=`sed -n '1p' /home/rtk/Desktop/pwd.txt`

### IP address ###
echo ""
echo "----------Starting to grep IP address-----------"
echo ""
grep 'NS1_IP4=' $set_netns >$pwd/net0_ipv4.txt
grep 'NS2_IP4=' $set_netns >$pwd/net1_ipv4.txt
cd $pwd
NS1_IP4=`awk -F '=' '{print $2s}' net0_ipv4.txt`
NS2_IP4=`awk -F '=' '{print $2s}' net1_ipv4.txt`
echo "NS1_IP4 = $NS1_IP4"
echo "NS2_IP4 = $NS2_IP4"
sudo rm $pwd/net0_ipv4.txt $pwd/net1_ipv4.txt

grep 'NS1_IP6=' /home/rtk/Desktop/$set_netns > net0_ipv6.txt
grep 'NS2_IP6=' /home/rtk/Desktop/$set_netns > net1_ipv6.txt
NS1_IP6=`awk -F '=' '{print $2s}' net0_ipv6.txt`
NS2_IP6=`awk -F '=' '{print $2s}' net1_ipv6.txt`
echo "NS1_IP6 = $NS1_IP6"
echo "NS2_IP6 = $NS2_IP6"
sudo rm net0_ipv6.txt net1_ipv6.txt

### tshark Setting ###
sudo tshark -D >tshark_record.txt
sed -e '/eth/!d' tshark_record.txt >eth.txt
sed -n '1p' eth.txt  >eth0.txt
sed -n '2p' eth.txt  >eth1.txt
eth0=`awk -F '.' '{print $1s}' eth0.txt`
eth1=`awk -F '.' '{print $1s}' eth1.txt`
sudo rm tshark_record.txt eth.txt eth0.txt eth1.txt

### Analyzing eth0 ###
sudo timeout 30 tshark -i eth0 -x -f tcp -c 100 > tcp.txt 
grep '00[0-3]0' tcp.txt >tcp_first_4_row.txt

cd ..
cd ..
#echo "----------Starting to Analyze-----------"
./tcp_analyze.sh > $pwd/tcp_analyze_result.txt
cd $pwd

### Analyzing ports ###

sort -o tmp2.txt tmp1.txt
uniq tmp2.txt > tmp3.txt
sed '$d' tmp3.txt > port_list.txt

LINE=`wc -l port_list.txt | awk '{print $1}'`

for i in $(seq 1 $LINE)
do
	tmp=`sed -n "$i"p port_list.txt | awk '{print $1}'`
	((k=0x$tmp)); echo $k >$k.txt; echo $k >> kk.txt
done
TAIL=`tail -n 1 kk.txt`

SUCCESS=0
times=`sed -n '1p' /home/rtk/Desktop/times.txt`

for h in $(seq 1 $TAIL)
do
	if [ -f "$h.txt" ]
	then		
		SUCCESS=`expr $SUCCESS + 1`
	else			
		echo ""			
		echo "Test $times: Mode 3: TCP Loss $h.txt. Please check port_list.txt." | tee -a /home/rtk/Desktop/final_result.txt
	fi
done

if [ $SUCCESS -eq $TAIL ];then
	echo ""	
	echo "Test $times: Mode 3: SUCCESS." | tee -a /home/rtk/Desktop/final_result.txt
fi

### Stopping Ping ###
#echo "----------Start to kill ping.-----------"
sudo ps aux | grep root | grep tcp_ > kill_tcp.txt

PING_PID1=`sed -n "1p" kill_tcp.txt | awk {'print $2s'}` >killed_PID1.txt
PING_PID2=`sed -n "2p" kill_tcp.txt | awk {'print $2s'}` >killed_PID2.txt
PING_PID3=`sed -n "3p" kill_tcp.txt | awk {'print $2s'}` >killed_PID3.txt
PING_PID4=`sed -n "4p" kill_tcp.txt | awk {'print $2s'}` >killed_PID4.txt

sudo kill $PING_PID1 $PING_PID2 $PING_PID3 $PING_PID4 
sudo rm kill_tcp.txt killed_PID1.txt killed_PID2.txt killed_PID3.txt killed_PID4.txt 

#echo "Kill ping Finished"

#--------------------------------------------------------------------------------


