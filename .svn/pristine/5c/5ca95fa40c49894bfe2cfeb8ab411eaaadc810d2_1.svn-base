#!/bin/bash
echo "123" | sudo -S ip netns exec net1 ./tcp_listener_multi_connection.py &
sleep 3
echo "123" | sudo -S ip netns exec net0 ./tcp_sender_multi_connection.py &
