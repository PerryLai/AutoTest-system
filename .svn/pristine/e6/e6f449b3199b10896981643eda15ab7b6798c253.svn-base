#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sup
import os
import paramiko as pm
import shutil
import time

### Config Setting ###
# 設定檔位址
ip_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\ip_config.ini'
fw_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\fw_config.ini'
switch_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\switch_config.ini'
control_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\control_config.ini'
testcase_config = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config\\testcase_config.ini'
# 要寄到client自動測試的檔案們
set_netns_net0 = sup.config_file(control_config, "Client", "set_netns_net0")
set_netns_net1 = sup.config_file(control_config, "Client", "set_netns_net1")
main = sup.config_file(control_config, "Client", "main")
test_program_folder = sup.config_file(control_config, "Client", "test_program_folder")
test_program = sup.config_file(control_config, "Client", "test_program")
packet_capture = sup.config_file(control_config, "Client", "packet_capture")
#壓縮
zip_dir_srcPath = sup.config_file(control_config, "Control Panel", "zip_dir_srcPath")
zip_dir_dstname = sup.config_file(control_config, "Control Panel", "zip_dir_dstname")
# 所有從client回傳的資料統整在這個資料夾
testcase_path = sup.config_file(control_config, "Control Panel", "testcase_path")
### Client address ###
main_client = sup.config_file(control_config, "Control Panel", "main_client")
source_code_client = sup.config_file(control_config, "Control Panel", "source_code_client")
### Server address ###
main_local = sup.config_file(control_config, "Control Panel", "main_local")
source_code_local = sup.config_file(control_config, "Control Panel", "source_code_local")
result_client=sup.config_file(control_config, "Control Panel", "result_client") #/home/pi/Desktop/Result.zip
result_local=sup.config_file(control_config, "Control Panel", "result_local") #D:\CN5SW1\Desktop\\Result
### 解壓縮路徑 ###
unzip_dir_srcName = sup.config_file(control_config, "Control Panel", "unzip_dir_srcName")
unzip_dir_dstPath = sup.config_file(control_config, "Control Panel", "unzip_dir_dstPath")
### 外部程式 ###
analyze = sup.config_file(control_config, "Control Panel", "analyze")
cle = sup.config_file(control_config, "Control Panel", "cle") # 這是程式路徑

sup.alter("%s\\%s"%(test_program_folder,test_program), 6, 10, control_config, "Client", "packet_ping_num")  