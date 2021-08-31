#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sup
import os
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

print("")
print("Please input your action: [modify] [check] [help] [exit]")
while(1):
    action = input("> ")
    #print("action: %s, file: %s,title: %s, offset: %s "%(action, file, title, offset))
    if (action == "help"):
        print('''
-modify : modify values of config parameters.
    -fw        : modify fw_config.ini
    -ip        : modify ip_config.ini
    -sw        : modify switch_config.ini
    -control   : modify control_config.ini
    -testcase  : modify testcase_config.ini
    -..      : Stop modify.
    -help      : Get some help.

-check: check titles of config files.
    -[file]                : check titles under files.
    -[file,title]          : check offsets under the title.
    -[file,title,offset]   : check values of the offset.
    -..                  : Stop check.
    -help                  : Get some help.

-exit: Leave setting and start test automatically.

-help: Get some help.
''')
    
    elif (action == "modify"):
        print("Please select the part and input the value you want to change: (Format: file,title,offset)")
        print("file: [ip], [fw], [sw], [control], [testcase], Type 'exit' to stop modify.")
        exit=0
        while(exit!=1):
            nums_str = input("> ").split(' ')
            if len(nums_str) == 1:
                file = nums_str[0]
                if( file == "ip"):
                    print("")
                    sup.config_file_title("%s"%ip_config)
                    print("")
                elif( file == "fw"):
                    print("")
                    sup.config_file_title("%s"%fw_config)
                    print("")
                elif( file == "sw"):
                    print("")
                    sup.config_file_title("%s"%switch_config)
                    print("")
                elif( file == "control"):
                    print("")
                    sup.config_file_title("%s"%control_config)
                    print("")
                elif( file == "testcase"):
                    print("")
                    sup.config_file_title("%s"%testcase_config)
                    print("")
                elif( file == "exit"):
                    exit=1
                else:
                    print("Error, please try again.\n")
                    continue
            
            elif len(nums_str) == 2:
                file = nums_str[0]
                title = nums_str[1]
                if( file == "ip"):
                    print("")
                    sup.config_file_all_show_value(ip_config, title)
                    print("")
                elif( file == "fw"):
                    print("")
                    sup.config_file_all_show_value(fw_config, title)
                    print("")
                elif( file == "sw"):
                    print("")
                    sup.config_file_all_show_value(switch_config, title)
                    print("")
                elif( file == "control"):
                    print("")
                    sup.config_file_all_show_value(control_config, title)
                    print("")
                elif( file == "testcase"):
                    print("")
                    sup.config_file_all_show_value(testcase_config, title)
                    print("")
                else:
                    print("No such file.")
                    continue
            
            elif len(nums_str) == 3:
                file = nums_str[0]
                title = nums_str[1]
                offset = nums_str[2]
                if( file == "ip"):
                    if ( sup.config_file_show_value(ip_config,title,offset) != -1):
                        print("")
                        print("The origin value is: %s."%sup.config_file_show_value(ip_config, title, offset))
                        i = input("Please input your new value> ")
                        sup.alter_parameter_to_config("%s"%ip_config,"%s"%title,"%s"%offset,"%s"%i)
                        print("Done.\n")
                        print("")
                    else:
                        print("No such title or offset.\n")
                        continue
                elif( file == "fw"):
                    if ( sup.config_file_show_value(fw_config, title, offset) != -1):
                        print("")
                        print("The origin value is: %s."%sup.config_file_show_value(fw_config, title, offset))
                        i = input("Please input your new value> ")
                        sup.alter_parameter_to_config("%s"%fw_config,"%s"%title,"%s"%offset,"%s"%i)
                        print("Done.\n")
                        print("")
                    else:
                        print("No such title or offset.\n")
                        continue
                elif( file == "sw"):
                    if ( sup.config_file_show_value(switch_config, title, offset) != -1):
                        print("")
                        print("The origin value is: %s."%sup.config_file_show_value(switch_config, title, offset))
                        i = input("Please input your new value> ")
                        sup.alter_parameter_to_config("%s"%switch_config,"%s"%title,"%s"%offset,"%s"%i)
                        print("Done.\n")
                        print("")
                    else:
                        print("No such title or offset.\n")
                        continue
                elif( file == "control"):
                    if ( sup.config_file_show_value(control_config, title, offset) != -1):
                        print("")
                        print("The origin value is: %s."%sup.config_file_show_value(control_config, title, offset))
                        i = input("Please input your new value> ")
                        sup.alter_parameter_to_config("%s"%control_config,"%s"%title,"%s"%offset,"%s"%i)
                        print("Done.\n")
                        print("")
                    else:
                        print("No such title or offset.\n")
                        continue
                elif( file == "testcase"):
                    if ( sup.config_file_show_value(testcase_config, title, offset) != -1):
                        print("")
                        print("The origin value is: %s."%sup.config_file_show_value(testcase_config, title, offset))
                        i = input("Please input your new value> ")
                        sup.alter_parameter_to_config("%s"%testcase_config,"%s"%title,"%s"%offset,"%s"%i)
                        print("Done.\n")
                        print("")
                    else:
                        print("No such title or offset.\n")
                        continue
                else:
                    print("No such file.\n")
                    print("")
                    continue
            
            else:
                print("Error, please try again.\n")
                continue

    elif (action == "check"):
        print("")
        print("Please select the part and input the value you want to check: (Format: file,title,offset)")
        print("file: [ip], [fw], [sw], [control], [testcase]. Type 'exit' to stop check.")
        exit=0
        while(exit!=1):
            nums_str = input("> ").split(' ')
            if len(nums_str) == 1:
                file = nums_str[0]
                if( file == "ip"):
                    print("")
                    sup.config_file_title("%s"%ip_config)
                    print("")
                elif( file == "fw"):
                    print("")
                    sup.config_file_title("%s"%fw_config)
                    print("")
                elif( file == "sw"):
                    print("")
                    sup.config_file_title("%s"%switch_config)
                    print("")
                elif( file == "control"):
                    print("")
                    sup.config_file_title("%s"%control_config)
                    print("")
                elif( file == "testcase"):
                    print("")
                    sup.config_file_title("%s"%testcase_config)
                    print("")
                elif( file == "exit"):
                    exit = 1
                else:
                    print("No such file.")
                    continue
            
            elif len(nums_str) == 2:
                file = nums_str[0]
                title = nums_str[1]
                if( file == "ip"):
                    print("")
                    sup.config_file_all_show_value(ip_config, title)
                    print("")
                elif( file == "fw"):
                    print("")
                    sup.config_file_all_show_value(fw_config, title)
                    print("")
                elif( file == "sw"):
                    print("")
                    sup.config_file_all_show_value(switch_config, title)
                    print("")
                elif( file == "control"):
                    print("")
                    sup.config_file_all_show_value(control_config, title)
                    print("")
                elif( file == "testcase"):
                    print("")
                    sup.config_file_all_show_value(testcase_config, title)
                    print("")
                else:
                    print("No such file.")
                    continue

            elif len(nums_str) == 3:
                file = nums_str[0]
                title = nums_str[1]
                offset = nums_str[2]
                if( file == "ip"):
                    if ( sup.config_file_show_value(ip_config,title,offset) != -1):
                        print("")
                        print("%s"%sup.config_file_show_value(ip_config, title, offset))
                        print("")
                    else:
                        print("No such title or offset.")
                        continue
                elif( file == "fw"):
                    if ( sup.config_file_show_value(fw_config,title,offset) != -1):
                        print("")
                        print("%s"%sup.config_file_show_value(fw_config, title, offset))
                        print("")
                    else:
                        print("No such title or offset.")
                        continue
                elif( file == "sw"):
                    if ( sup.config_file_show_value(switch_config,title,offset) != -1):
                        print("")
                        print("%s"%sup.config_file_show_value(switch_config, title, offset))
                        print("")
                    else:
                        print("No such title or offset.")
                        continue
                elif( file == "control"):
                    if ( sup.config_file_show_value(control_config,title,offset) != -1):
                        print("")
                        print("%s"%sup.config_file_show_value(control_config, title, offset))
                        print("")
                    else:
                        print("No such title or offset.")
                        continue
                elif( file == "testcase"):
                    if ( sup.config_file_show_value(testcase_config,title,offset) != -1):
                        print("")
                        print("%s"%sup.config_file_show_value(testcase_config, title, offset))
                        print("")
                    else:
                        print("No such title or offset.")
                        continue
                else:
                    print("No such file.")
                    continue
            else:
                print("Error, please try again.")
                continue
            
    elif (action == "exit"):
        print("")
        print("The AutoTest will start running and won't stop until fatel error happened.")
        start=input("Are you sure you want to leave? (Y/n)> ")
        if (start == "Y" or start == "y"):
            break
        elif(start == "N" or start == "n"):
            continue
        else:
            print("Error, please try again.")
            continue
    
    elif (action == ""):
        www=0
    else:
        print("No such command, please try again.")
        continue