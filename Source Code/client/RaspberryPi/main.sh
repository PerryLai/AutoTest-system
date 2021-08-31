#!/bin/bash
unzip RaspberryPi.zip
cp CN5SW1/Desktop/AutoTest\ Platform/Source\ Code/client/RaspberryPi/set_netns_net0.sh set_netns.sh
cp CN5SW1/Desktop/AutoTest\ Platform/Source\ Code/client/RaspberryPi/packet_capture.sh packet_capture.sh
cp CN5SW1/Desktop/AutoTest\ Platform/Source\ Code/client/RaspberryPi/packet_offset.sh packet_offset.sh
cp CN5SW1/Desktop/AutoTest\ Platform/Source\ Code/client/RaspberryPi/packet_transfer.sh packet_transfer.sh
cp -r CN5SW1/Desktop/AutoTest\ Platform/Source\ Code/client/RaspberryPi/txt /home/pi/Desktop/txt
cp -r CN5SW1/Desktop/AutoTest\ Platform/Source\ Code/client/RaspberryPi/packet_transfer_programs /home/pi/Desktop/packet_transfer_programs

echo "raspberry" | sudo -S chmod 777 set_netns.sh
echo "raspberry" | sudo -S chmod 777 packet_capture.sh
echo "raspberry" | sudo -S chmod 777 packet_offset.sh 
echo "raspberry" | sudo -S chmod 777 packet_transfer.sh
dos2unix packet_capture.sh packet_offset.sh packet_transfer.sh set_netns.sh
cd packet_transfer_programs
echo "raspberry" | sudo -S chmod 777 icmp.sh
echo "raspberry" | sudo -S chmod 777 icmpv6.sh
echo "raspberry" | sudo -S chmod 777 tcp.sh
dos2unix icmp.sh icmpv6.sh tcp.sh
cd ..
cd txt
dos2unix test_program.txt packet_type.txt
cd ..

sudo rm -r Result 
mkdir Result   #Reset Result folder, error file, and final result file

### Rusult Folder Set ###
date=$(date '+%m%d_%H:%M:%S:%3N')
cd Result
mkdir $date
cd $date
pwd > /home/pi/Desktop/txt/pwd.txt
cd ..
cd ..

### packet transfer reset ###
./packet_transfer.sh 2>>error.txt

### packet capture reset ###
./packet_capture.sh 2>>error.txt
echo "packet_capture done"

### packet offset ###
./packet_offset.sh 2>>error.txt
echo "packet_offset done"

### processes kill ###
cd $pwd
sudo ip netns exec net0 ps aux | grep ping >kill_ping.txt 
PING_PID=`sed -n "2p" kill_ping.txt | awk {'print $2s'}` >killed_PID.txt
echo "PING_PID=$PING_PID"
sudo kill $PING_PID 
sudo rm kill_ping.txt killed_PID.txt

cd /home/pi/Desktop
sleep 10

sudo zip -r Result.zip Result
