#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sup
import os
import shutil
import time
import packet_analyze
### Config Setting ###
# 設定檔位址
ip_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\ip_config.ini'
fw_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\fw_config.ini'
switch_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\switch_config.ini'
control_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\control_config.ini'
testcase_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\testcase_config.ini'
# 要寄到client自動測試的檔案們
main = sup.config_file(control_config, "Client", "main")
set_netns_net0 = sup.config_file(control_config, "Client", "set_netns_net0")
set_netns_net1 = sup.config_file(control_config, "Client", "set_netns_net1")
test_program_folder = sup.config_file(control_config, "Client", "test_program_folder")
test_program_path = sup.config_file(control_config, "Client", "test_program_path")
test_program = sup.config_file(control_config, "Client", "test_program")
packet_capture = sup.config_file(control_config, "Client", "packet_capture")
#壓縮
zip_dir_srcPath = sup.config_file(control_config, "Control_Panel", "zip_dir_srcPath")
zip_dir_dstname = sup.config_file(control_config, "Control_Panel", "zip_dir_dstname")
# 所有從client回傳的資料統整在這個資料夾
testcase_path = sup.config_file(control_config, "Control_Panel", "testcase_path")
### Client address ###
main_client = sup.config_file(control_config, "Control_Panel", "main_client")
source_code_client = sup.config_file(control_config, "Control_Panel", "source_code_client")
### Server address ###
main_local = sup.config_file(control_config, "Control_Panel", "main_local")
source_code_local = sup.config_file(control_config, "Control_Panel", "source_code_local")
result_client=sup.config_file(control_config, "Control_Panel", "result_client") #/home/pi/Desktop/Result.zip
result_local=sup.config_file(control_config, "Control_Panel", "result_local") #D:\CN5SW1\Desktop\\Result
### 解壓縮路徑 ###
unzip_dir_srcName = sup.config_file(control_config, "Control_Panel", "unzip_dir_srcName")
unzip_dir_dstPath = sup.config_file(control_config, "Control_Panel", "unzip_dir_dstPath")
### 外部程式 ###
analyze = sup.config_file(control_config, "Control_Panel", "analyze")
cli = sup.config_file(control_config, "Control_Panel", "cli") # 這是程式路徑
cle = sup.config_file(control_config, "Control_Panel", "cle") # 這是程式路徑
clecfg = sup.config_file(control_config, "Control_Panel", "clecfg") # 這是程式路徑
# 設定檔位址
ip_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\ip_config.ini'
control_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\control_config.ini'
testcase_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\testcase_config.ini'
# 所有從client回傳的資料統整在這個資料夾
testcase_path = sup.config_file(testcase_config, "Testcase", "testcase_path")
output = sup.config_file(testcase_config, "Testcase", "output_dir") # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output
output_icmp_dir = sup.config_file(testcase_config, "Testcase", "output_icmp_dir") # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\ICMP
output_icmpv6_dir = sup.config_file(testcase_config, "Testcase", "output_icmpv6_dir") # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\ICMPv6
output_tcp_dir = sup.config_file(testcase_config, "Testcase", "output_tcp_dir") # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\TCP

result_file = "%s\\Final.txt"%(output)
sup.remove_old_file(result_file)

for i in range(3):
    i=i+1
    packet_analyze.icmp_core(output,testcase_config,testcase_path,output_icmp_dir,output_icmpv6_dir,i)