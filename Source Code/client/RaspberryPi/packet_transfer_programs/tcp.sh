#!/bin/bash
cd ..
set_netns=set_netns.sh

### Reset variable ###
cd txt
row_net0=`cat row_net0.txt | awk '{print $1}'`
row_net1=`cat row_net1.txt | awk '{print $1}'`
NS1_IP6=`cat ip_list.txt | awk 'NR==row{print $7}' row="$row_net0"`
NS2_IP6=`cat ip_list.txt | awk 'NR==row{print $7}' row="$row_net1"`
cd ..

cd packet_transfer_programs
tcp_sender_multi_connection_bind=`cat tcp_sender_multi_connection.py | awk -F '"' 'NR==17 {print $2}'`
tcp_sender_multi_connection_connect=`cat tcp_sender_multi_connection.py | awk -F '"' 'NR==20 {print $2}'`
tcp_listener_multi_connection=`cat tcp_listener_multi_connection.py | awk -F '"' 'NR==13 {print $2}'`

### replace data to tcp listener/sender.py ###
sed -i "s/\<${tcp_sender_multi_connection_bind}\>/${NS1_IP6}/g" tcp_sender_multi_connection.py
sed -i "s/\<${tcp_sender_multi_connection_connect}\>/${NS1_IP6}/g" tcp_sender_multi_connection.py
sed -i "s/\<${tcp_listener_multi_connection}\>/${NS2_IP6}/g" tcp_listener_multi_connection.py

echo "123" | sudo -S ip netns exec net1 ./tcp_listener_multi_connection.py &
sleep 3
echo "123" | sudo -S ip netns exec net0 ./tcp_sender_multi_connection.py &
