#!/bin/bash

pwd=`sed -n '1p' /home/rtk/Desktop/pwd.txt`
set_netns=b_set_netns.sh
cd $pwd
echo ""
echo "----------Starting to grep IP address-----------"
echo ""
grep 'NS1_IP4=' /home/rtk/Desktop/$set_netns > net0_ipv4.txt
grep 'NS2_IP4=' /home/rtk/Desktop/$set_netns > net1_ipv4.txt
NS1_IP4=`awk -F '=' '{print $2s}' net0_ipv4.txt`
NS2_IP4=`awk -F '=' '{print $2s}' net1_ipv4.txt`
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
echo ""

k=1
for i in {1..5}
do

sudo ip netns exec net0 ping -i 0.1 $NS2_IP4 -c10 > ping1.txt 2>&1

grep "$NS2_IP4:" ping1.txt > ipv4_ping_succes.txt 2>&1
ipv4_ping_succes="ipv4_ping_succes.txt"

grep -i "Unreachable" ping1.txt > Destination_Host_Unreachable.txt 2>&1
Destination_Host_Unreachable="Destination_Host_Unreachable.txt"

if [ -s "$Destination_Host_Unreachable" ] && [ -s "$ipv4_ping_succes" ]
then
	IPV4SUCCESS1='2';

elif [ -s "$ipv4_ping_succes" ]
then

	IPV4SUCCESS1='1';

else
	IPV4SUCCESS1='0';

fi

sudo ip netns exec net1 ping -i 0.1 $NS1_IP4 -c10 > ping2.txt 2>&1

grep "$NS1_IP4:" ping2.txt > ipv4_ping_succes.txt 2>&1
ipv4_ping_succes="ipv4_ping_succes.txt"

grep -i "Unreachable" ping2.txt > Destination_Host_Unreachable.txt 2>&1
Destination_Host_Unreachable="Destination_Host_Unreachable.txt"

if [ -s "$Destination_Host_Unreachable" ] && [ -s "$ipv4_ping_succes" ]
then
	IPV4SUCCESS2='2';

elif [ -s "$ipv4_ping_succes" ]
then

	IPV4SUCCESS2='1';

else
	IPV4SUCCESS2='0';

fi

sudo ip netns exec net0 ping6 -i 0.1 $NS2_IP6 -c10 > ping3.txt 2>&1

grep "$NS2_IP6:" ping3.txt > ipv6_ping_succes.txt 2>&1
ipv6_ping_succes="ipv6_ping_succes.txt"

grep -i "Unreachable" ping3.txt > Destination_Host_Unreachable.txt 2>&1
Destination_Host_Unreachable="Destination_Host_Unreachable.txt"


if [ -s "$Destination_Host_Unreachable" ] && [ -s "$ipv6_ping_succes" ]
then
	IPV6SUCCESS3='2';

elif [ -s "$ipv6_ping_succes" ]
then
	IPV6SUCCESS3='1';

else
	IPV6SUCCESS3='0';

fi

sudo ip netns exec net1 ping6 -i 0.1 $NS1_IP6 -c10 > ping4.txt 2>&1

grep "$NS1_IP6:" ping4.txt > ipv6_ping_succes.txt 2>&1
ipv6_ping_succes="ipv6_ping_succes.txt"

grep -i "Unreachable" ping4.txt > Destination_Host_Unreachable.txt 2>&1
Destination_Host_Unreachable="Destination_Host_Unreachable.txt" 

if [ -s "$Destination_Host_Unreachable" ] && [ -s "$ipv6_ping_succes" ]
then
	IPV6SUCCESS4='2';

elif [ -s "$ipv6_ping_succes" ]
then
	IPV6SUCCESS4='1';

else
	IPV6SUCCESS4='0';

fi

time=`sed -n '1p' /home/rtk/Desktop/times.txt`

if [ "$IPV4SUCCESS1" -eq 1 ] && [ "$IPV4SUCCESS2" -eq 1 ] && [ "$IPV6SUCCESS3" -eq 1 ] && [ "$IPV6SUCCESS4" -eq 1 ]
then
	echo "Test $time: Mode 2: SUCCESS." | tee -a /home/rtk/Desktop/final_result.txt
	break

elif [ "$IPV4SUCCESS1" -eq 2 ] || [ "$IPV4SUCCESS2" -eq 2 ] || [ "$IPV6SUCCESS3" -eq 2 ] || [ "$IPV6SUCCESS4" -eq 2 ]
then
	if [ "$IPV4SUCCESS1" -ne 0 ] || [ "$IPV4SUCCESS2" -ne 0 ] || [ "$IPV6SUCCESS3" -ne 0 ] || [ "$IPV6SUCCESS4" -ne 0 ]
	then
		if [ "$IPV6SUCCESS4" -eq 0 ]
		then
			if [ "$k" -ne 5 ]
			then
				echo "Test $time: Mode 2: Failed but it used to Successed." | tee -a /home/rtk/Desktop/final_result.txt
				echo "For making sure, system will ping again." | tee -a /home/rtk/Desktop/final_result.txt
				k=`expr $k + 1`
				continue
			
			else
				echo "Test $time: Mode 2: Failed every last time. Please check." | tee -a /home/rtk/Desktop/final_result.txt
				break
			fi			

		elif [ "$IPV6SUCCESS4" -ne 0 ]
		then
			if [ "$k" -ne 5 ]
			then
				echo "Test $time: Mode 2: SUCCESS but Unstable." | tee -a /home/rtk/Desktop/final_result.txt
				echo "For making sure, system will ping again." | tee -a /home/rtk/Desktop/final_result.txt
				k=`expr $k + 1`
				continue
			
			else
				echo "Test $time: Mode 2: SUCCESS but still Unstable." | tee -a /home/rtk/Desktop/final_result.txt
				break
			fi
		else
			echo "Test $time: Mode 2: I don't know what's happened." | tee -a /home/rtk/Desktop/final_result.txt
		fi
	else
		echo "Test $time: Mode 2: Failed" | tee -a /home/rtk/Desktop/final_result.txt
		break
	fi

else 
	echo "Test $time: Mode 2: Failed." | tee -a /home/rtk/Desktop/final_result.txt
	break
fi

done

cd ..
