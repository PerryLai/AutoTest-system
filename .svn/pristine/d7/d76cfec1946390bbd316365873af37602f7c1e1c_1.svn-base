#!/bin/bash
set_netns=set_netns.sh
pwd=`sed -n '1p' /home/pi/Desktop/txt/pwd.txt`

### Setting IP address ###
echo ""
echo "----------Starting to grep IP address-----------"
echo ""
### Setting variable IPv4 ###
NS1_IP4=`grep 'NS1_IP4=' $set_netns | awk -F '=' '{print $2s}'`
NS2_IP4=`grep 'NS2_IP4=' $set_netns | awk -F '=' '{print $2s}'`
cd $pwd
echo "NS1_IP4 = $NS1_IP4"
echo "NS2_IP4 = $NS2_IP4"
### Setting variable IPv6 ###
NS1_IP6=`grep 'NS1_IP6=' /home/pi/Desktop/$set_netns | awk -F '=' '{print $2s}'`
NS2_IP6=`grep 'NS2_IP6=' /home/pi/Desktop/$set_netns | awk -F '=' '{print $2s}'`
echo "NS1_IP6 = $NS1_IP6"
echo "NS2_IP6 = $NS2_IP6"

### Setting tshark ###
sudo tshark -D >tshark_record.txt
sed -e '/eth/!d' tshark_record.txt >eth.txt
eth0=`sed -n '1p' eth.txt | awk -F '.' '{print $2s}'`
eth1=`sed -n '2p' eth.txt | awk -F '.' '{print $2s}'`
packet_type=`sed -n '1p' /home/pi/Desktop/txt/packet_type.txt`
sudo rm tshark_record.txt eth.txt

### Analyzing eth0 ###
#sudo timeout 30 tshark -i $eth0 -V -c 10 > /home/pi/Desktop/tshark_record.txt 
sudo timeout 30 tshark -i $eth0 -x -c 10 > tshark_record_pcap.txt

