#!/bin/bash
cd ..
set_netns=set_netns.sh
pwd=`sed -n '1p' /home/pi/Desktop/txt/pwd.txt`

NS2_IP6=`grep -n 'NS2_IP6' $set_netns | awk -F '=' '{print $2s}'`
sudo ip netns exec net0 ping -i 0.1 $NS2_IP6 -c 200 >ping_record.txt &
echo "packet_transfer done"
