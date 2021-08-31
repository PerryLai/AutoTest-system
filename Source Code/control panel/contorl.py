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

mode = input('''
Please select the mode you want to start: 
1. [I]nteractive Mode: There will be chance to modify and check every data before testing.
2. [A]uto Run Mode: Once you complete data setting, the test will keep going until all testcases are finished.
> ''')
while(mode != "jkvbejksvfjwenbhfvjreb"):
    if (mode == "I"):
        # 初始化所有testcase Result資料夾
        testcase_file_num = len([name for name in os.listdir(testcase_path) if os.path.isdir(os.path.join(testcase_path, name))])
        for i in range(testcase_file_num-1):
            i=i+1
            Result_dir = "%s\\testcase\\Result%r" %(sup.config_file(control_config, "Control_Panel", "AutoTest_Path"),i)
            shutil.rmtree(Result_dir)
            if not os.path.isdir(Result_dir):
                os.mkdir(Result_dir)

        ip_nums = len(sup.config_file_all_title(ip_config))

        # 主程式
        for i in range(ip_nums):
            ### 呼叫呼叫設定命令列 ###
            commandText = "python "+'"' + cli + '"'
            os.system(commandText)
            i=i+1
            ### 設定IP ###
            sup.alter_ip_to_config(control_config, ip_config,i) # ip_list.ini -> control_config
            sup.alter_config_to_set_netns_net0(control_config, set_netns_net0) # 抓config的資料到set_netns_net0
            sup.alter_config_to_set_netns_net1(control_config, set_netns_net1) # 抓config的資料到set_netns_net1
            sup.alter(test_program_path, 0, 0, control_config, "Client", "test_program") # 抓config的資料到test_program.txt
            #sup.alter(packet_capture, 30, 8, control_config, "Client", "packet_catch_num") # 抓config設定的擷取封包數到packet_capture.sh
            #sup.alter(packet_capture, 29, 8, control_config, "Client", "packet_catch_num") # 抓config設定的擷取封包數到packet_capture.sh
            #sup.alter("%s\\%s"%(test_program_folder,test_program), 6, 10, control_config, "Client", "packet_ping_num") # 抓config設定的打封包數到packet_transfer_program，若有修改務必改掉參數                 
            ### 設定FW ###
            sup.alter_fw_to_config(control_config,fw_config,i)# fw_config.ini -> control_config.ini
            fw_bin = sup.config_file(control_config, "Firmware_config", "Firmware_config") # 這是待測Fw檔名
            i2cid = sup.config_file(control_config, "Firmware_config", "i2cid") # 這是待測Fw檔名
            #a = input ("i2cid: %s, fw: %s, type anything"%(i2cid,fw_bin))
            print("i2cid: %s, fw: %s, type anything"%(i2cid,fw_bin))
            sup.i2cid_set(clecfg, i2cid)
            sup.cle_set(cle,fw_bin)
            ### Switch ###
            sup.alter_sw_to_config(control_config,switch_config,i)# sw_config.ini -> control_config.ini
            HOST = sup.config_file(control_config, "switch", "HOST")
            USER = sup.config_file(control_config, "switch", "USER")
            PASSWORD = sup.config_file(control_config, "switch", "PASSWORD")
            PORT = sup.config_file(control_config, "switch", "PORT")
            CP_normal = sup.config_file(control_config, "switch", "CP_normal")
            CP_fixed = sup.config_file(control_config, "switch", "CP_fixed")
            CP_forbidden = sup.config_file(control_config, "switch", "CP_forbidden")
            PC1_vlan = sup.config_file(control_config, "switch", "PC1_vlan")
            PC1_normal = sup.config_file(control_config, "switch", "PC1_normal")
            PC1_fixed = sup.config_file(control_config, "switch", "PC1_fixed")
            PC1_forbidden = sup.config_file(control_config, "switch", "PC1_forbidden")
            PC2_vlan = sup.config_file(control_config, "switch", "PC2_vlan")
            PC2_normal = sup.config_file(control_config, "switch", "PC2_normal")
            PC2_fixed = sup.config_file(control_config, "switch", "PC2_fixed")
            PC2_forbidden = sup.config_file(control_config, "switch", "PC2_forbidden")
            sup.switch_portset(HOST,USER,PASSWORD,PORT,PC1_vlan,PC1_normal,PC1_fixed,PC1_forbidden)
            sup.switch_portset(HOST,USER,PASSWORD,PORT,PC2_vlan,PC2_normal,PC2_fixed,PC2_forbidden)
            sup.switch_portset(HOST,USER,PASSWORD,PORT,'1',CP_normal,CP_fixed,CP_forbidden) # switch 對 CP default 的 vlan 就是 1 
            # 把所有寫死的參數全部改成從config抓取變數，包含set_netns.sh(另寫一支子程式呼叫set_netns並修改參數)
            HOST_net0 = sup.config_file(control_config, "Control_Panel", "HOST_net0")
            USER_net0 = sup.config_file(control_config, "Control_Panel", "USER_net0")
            PASSWORD_net0 = sup.config_file(control_config, "Control_Panel", "PASSWORD_net0")
            PORT_net0 = sup.config_file(control_config, "Control_Panel", "PORT_net0")
            HOST_net1 = sup.config_file(control_config, "Control_Panel", "HOST_net1")
            USER_net1 = sup.config_file(control_config, "Control_Panel", "USER_net1")
            PASSWORD_net1 = sup.config_file(control_config, "Control_Panel", "PASSWORD_net1")
            PORT_net1 = sup.config_file(control_config, "Control_Panel", "PORT_net1")
            
            ### 將檔案壓縮存到特定位址 ###
            sup.zip_dir(zip_dir_srcPath,zip_dir_dstname)
            ### 將壓縮檔案傳送到client並進行指令控制 ###
            sup.paramiko_net0(HOST_net0,USER_net0,PASSWORD_net0,PORT_net0,source_code_local,source_code_client)
            sup.paramiko_net1(HOST_net1,USER_net1,PASSWORD_net1,PORT_net1,source_code_local,source_code_client)
            sup.paramiko_link(HOST_net0,USER_net0,PASSWORD_net0,PORT_net0,main_local,main_client,source_code_local,source_code_client,result_client,result_local,i)
            ### 解壓縮client蒐集到的封包 ###
            sup.unzip_dir("%s\\Result%s.zip" %(sup.config_file(control_config, "Control_Panel", "unzip_dir_srcName"),i),"%s\\Result%s"%(sup.config_file(control_config, "Control_Panel", "unzip_dir_dstPath"),i))
            packet_analyze.init_folder(output_icmp_dir,i)
            packet_analyze.init_folder(output_icmpv6_dir,i)
            #packet_analyze.analyzing_core()
            # report_generator()
            packet_analyze.icmp_core(output,testcase_config,testcase_path,output_icmp_dir,output_icmpv6_dir,i)
        break
    
    elif (mode == "A"):
        # 初始化所有testcase Result資料夾
        testcase_file_num = len([name for name in os.listdir(testcase_path) if os.path.isdir(os.path.join(testcase_path, name))])
        for i in range(testcase_file_num-1):
            i=i+1
            Result_dir = "%s\\testcase\\Result%r" %(sup.config_file(control_config, "Control_Panel", "AutoTest_Path"),i)
            shutil.rmtree(Result_dir)
            if not os.path.isdir(Result_dir):
                os.mkdir(Result_dir)

        ip_nums = len(sup.config_file_all_title(ip_config))

        ### 呼叫設定命令列 ###
        commandText = "python "+'"' + cli + '"'
        os.system(commandText)

        # 主程式
        for i in range(ip_nums):
            i=i+1
            ### 設定IP ###
            sup.alter_ip_to_config(control_config, ip_config,i) # ip_list.ini -> control_config
            sup.alter_config_to_set_netns_net0(control_config, set_netns_net0) # 抓config的資料到set_netns_net0
            sup.alter_config_to_set_netns_net1(control_config, set_netns_net1) # 抓config的資料到set_netns_net1
            sup.alter(test_program_path, 0, 0, control_config, "Client", "test_program") # 抓config的資料到test_program.txt
            #sup.alter(packet_capture, 30, 8, control_config, "Client", "packet_catch_num") # 抓config設定的擷取封包數到packet_capture.sh
            #sup.alter(packet_capture, 29, 8, control_config, "Client", "packet_catch_num") # 抓config設定的擷取封包數到packet_capture.sh
            #sup.alter("%s\\%s"%(test_program_folder,test_program), 6, 10, control_config, "Client", "packet_ping_num") # 抓config設定的打封包數到packet_transfer_program，若有修改務必改掉參數                 
            ### 設定FW ###
            sup.alter_fw_to_config(control_config,fw_config,i)# fw_config.ini -> control_config.ini
            fw_bin = sup.config_file(control_config, "Firmware_config", "Firmware_config") # 這是待測Fw檔名
            i2cid = sup.config_file(control_config, "Firmware_config", "i2cid") # 這是待測Fw檔名
            #a = input ("i2cid: %s, fw: %s, type anything"%(i2cid,fw_bin))
            print("i2cid: %s, fw: %s, type anything"%(i2cid,fw_bin))
            sup.i2cid_set(clecfg, i2cid)
            sup.cle_set(cle,fw_bin)
            ### Switch ###
            sup.alter_sw_to_config(control_config,switch_config,i)# sw_config.ini -> control_config.ini
            HOST = sup.config_file(control_config, "switch", "HOST")
            USER = sup.config_file(control_config, "switch", "USER")
            PASSWORD = sup.config_file(control_config, "switch", "PASSWORD")
            PORT = sup.config_file(control_config, "switch", "PORT")
            CP_normal = sup.config_file(control_config, "switch", "CP_normal")
            CP_fixed = sup.config_file(control_config, "switch", "CP_fixed")
            CP_forbidden = sup.config_file(control_config, "switch", "CP_forbidden")
            PC1_vlan = sup.config_file(control_config, "switch", "PC1_vlan")
            PC1_normal = sup.config_file(control_config, "switch", "PC1_normal")
            PC1_fixed = sup.config_file(control_config, "switch", "PC1_fixed")
            PC1_forbidden = sup.config_file(control_config, "switch", "PC1_forbidden")
            PC2_vlan = sup.config_file(control_config, "switch", "PC2_vlan")
            PC2_normal = sup.config_file(control_config, "switch", "PC2_normal")
            PC2_fixed = sup.config_file(control_config, "switch", "PC2_fixed")
            PC2_forbidden = sup.config_file(control_config, "switch", "PC2_forbidden")
            sup.switch_portset(HOST,USER,PASSWORD,PORT,PC1_vlan,PC1_normal,PC1_fixed,PC1_forbidden)
            sup.switch_portset(HOST,USER,PASSWORD,PORT,PC2_vlan,PC2_normal,PC2_fixed,PC2_forbidden)
            sup.switch_portset(HOST,USER,PASSWORD,PORT,'1',CP_normal,CP_fixed,CP_forbidden) # switch 對 CP default 的 vlan 就是 1 
            # 把所有寫死的參數全部改成從config抓取變數，包含set_netns.sh(另寫一支子程式呼叫set_netns並修改參數)
            HOST_net0 = sup.config_file(control_config, "Control_Panel", "HOST_net0")
            USER_net0 = sup.config_file(control_config, "Control_Panel", "USER_net0")
            PASSWORD_net0 = sup.config_file(control_config, "Control_Panel", "PASSWORD_net0")
            PORT_net0 = sup.config_file(control_config, "Control_Panel", "PORT_net0")
            HOST_net1 = sup.config_file(control_config, "Control_Panel", "HOST_net1")
            USER_net1 = sup.config_file(control_config, "Control_Panel", "USER_net1")
            PASSWORD_net1 = sup.config_file(control_config, "Control_Panel", "PASSWORD_net1")
            PORT_net1 = sup.config_file(control_config, "Control_Panel", "PORT_net1")
            
            ### 將檔案壓縮存到特定位址 ###
            sup.zip_dir(zip_dir_srcPath,zip_dir_dstname)
            ### 將壓縮檔案傳送到client並進行指令控制 ###
            sup.paramiko_net0(HOST_net0,USER_net0,PASSWORD_net0,PORT_net0,source_code_local,source_code_client)
            sup.paramiko_net1(HOST_net1,USER_net1,PASSWORD_net1,PORT_net1,source_code_local,source_code_client)
            sup.paramiko_link(HOST_net0,USER_net0,PASSWORD_net0,PORT_net0,main_local,main_client,source_code_local,source_code_client,result_client,result_local,i)
            ### 解壓縮client蒐集到的封包 ###
            sup.unzip_dir("%s\\Result%s.zip" %(sup.config_file(control_config, "Control_Panel", "unzip_dir_srcName"),i),"%s\\Result%s"%(sup.config_file(control_config, "Control_Panel", "unzip_dir_dstPath"),i))
        
            packet_analyze.init_folder(output_icmp_dir,i)
            packet_analyze.init_folder(output_icmpv6_dir,i)
            #packet_analyze.analyzing_core()
            # report_generator()
            packet_analyze.icmp_core(output,testcase_config,testcase_path,output_icmp_dir,output_icmpv6_dir,i)
        break
    else:
        print("Error, please try again.")
        mode = input('''
Please select the mode you want to start: 
1. [I]nteractive Mode: There will be chance to modify and check every data before testing.
2. [A]uto Run Mode: The test will keep going until all tests are finished.
> ''')

a=input("Type anything.")
### 呼叫fork子程式 ###
# commandText = "python "+'"' + analyze + '"'
# os.system(commandText)
