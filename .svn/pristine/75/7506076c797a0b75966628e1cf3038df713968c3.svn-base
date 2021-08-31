#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sup
import os
### Config Setting ###
# 設定檔位址
config_file = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config.ini'

cle = sup.config_file(config_file, "Control Panel", "cle")

# 設定fw
# 呼叫cle子程式

cmd = '''D: & \
cd %s & \
cle.exe spi erase all & \
cle.exe spi update fw_config.bin & \
''' %cle

os.system(cmd)
