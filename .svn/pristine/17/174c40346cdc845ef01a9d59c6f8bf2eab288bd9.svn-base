#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import configparser
import zipfile
import paramiko as pm
import shutil
import telnetlib
import time

class myconf(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr

# 壓縮
def zip_dir(srcPath,dstname):
    zipHandle=zipfile.ZipFile(dstname,'w',zipfile.ZIP_DEFLATED)
    for dirpath,dirs,files in os.walk(srcPath):
        for filename in files:
            zipHandle.write(os.path.join(dirpath,filename)) #檔名路徑必須完整
            print (filename+" zip succeeded")
    zipHandle.close

# 解壓縮
def unzip_dir(srcname,dstPath):
    zipHandle=zipfile.ZipFile(srcname,"r")
    for filename in zipHandle.namelist():
        print (filename)
    zipHandle.extractall(dstPath) #解壓到指定目錄
    zipHandle.close()

# 從指定config中取得資料
def config_file(_config_file_, offset1, offset2):
    config = configparser.ConfigParser()
    config.read(_config_file_,encoding="utf-8")
    # 取得設定值
    return(config[offset1][offset2])

# 列出所有區段的大標題
def config_file_all_title(_config_file_):
    config = myconf()
    config.read(_config_file_)
    return(config.sections())

# 列出指定標題區段下所有設定值
def config_file_all_contents(_config_file_, _title_):
    config = configparser.ConfigParser()
    config.read(_config_file_)
    i=0
    a={}
    for k in config[_title_]:
        a[i]=("{}: {}".format(k, config[_title_][k]))
        i=i+1
    return a

# 將ip_config.ini內容取代control_config.ini
def alter_ip_to_config(_config_file_, _ip_file_,i):
    config = myconf()
    config.read(_config_file_, encoding="utf-8")
    config['Client']['test_program'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'test_program')
    config['Net Namespace Set 1']['NS1_NAME'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS1_NAME')
    config['Net Namespace Set 1']['NS1_VID'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS1_VID')
    config['Net Namespace Set 1']['NS1_BASE_IF'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS1_BASE_IF')
    config['Net Namespace Set 1']['NS1_IP4'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS1_IP4')
    config['Net Namespace Set 1']['NS1_MASK4'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS1_MASK4')
    config['Net Namespace Set 1']['NS1_GW4'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS1_GW4')
    config['Net Namespace Set 1']['NS1_IP6'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS1_IP6')
    config['Net Namespace Set 1']['NS1_MASK6'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS1_MASK6')
    config['Net Namespace Set 1']['NS1_GW6'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS1_GW6')
    config['Net Namespace Set 1']['NS1_GW_MAC'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS1_GW_MAC')
    config['Net Namespace Set 2']['NS2_NAME'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS2_NAME')
    config['Net Namespace Set 2']['NS2_VID'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS2_VID')
    config['Net Namespace Set 2']['NS2_BASE_IF'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS2_BASE_IF')
    config['Net Namespace Set 2']['NS2_IP4'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS2_IP4')
    config['Net Namespace Set 2']['NS2_MASK4'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS2_MASK4')
    config['Net Namespace Set 2']['NS2_GW4'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS2_GW4')
    config['Net Namespace Set 2']['NS2_IP6'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS2_IP6')
    config['Net Namespace Set 2']['NS2_MASK6'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS2_MASK6')
    config['Net Namespace Set 2']['NS2_GW6'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS2_GW6')
    config['Net Namespace Set 2']['NS2_GW_MAC'] = config_file(_ip_file_, "Net Namespace Set %s"%i, 'NS2_GW_MAC')
    config.write(open(_config_file_, "w"))

# 將sw_config.ini內容取代control_config.ini
def alter_sw_to_config(_config_file_, _switch_file_,i):
    config = myconf()
    config.read(_config_file_, encoding="utf-8")
    config['switch']['HOST'] = config_file(_switch_file_, "setting %s"%i, 'HOST')
    config['switch']['USER'] = config_file(_switch_file_, "setting %s"%i, 'USER')
    config['switch']['PASSWORD'] = config_file(_switch_file_, "setting %s"%i, 'PASSWORD')
    config['switch']['PORT'] = config_file(_switch_file_, "setting %s"%i, 'PORT')
    config['switch']['CP_normal'] = config_file(_switch_file_, "setting %s"%i, 'CP_normal')
    config['switch']['CP_fixed'] = config_file(_switch_file_, "setting %s"%i, 'CP_fixed')
    config['switch']['CP_forbidden'] = config_file(_switch_file_, "setting %s"%i, 'CP_forbidden')
    config['switch']['PC1_vlan'] = config_file(_switch_file_, "setting %s"%i, 'PC1_vlan')
    config['switch']['PC1_normal'] = config_file(_switch_file_, "setting %s"%i, 'PC1_normal')
    config['switch']['PC1_fixed'] = config_file(_switch_file_, "setting %s"%i, 'PC1_fixed')
    config['switch']['PC1_forbidden'] = config_file(_switch_file_, "setting %s"%i, 'PC1_forbidden')
    config['switch']['PC2_vlan'] = config_file(_switch_file_, "setting %s"%i, 'PC2_vlan')
    config['switch']['PC2_normal'] = config_file(_switch_file_, "setting %s"%i, 'PC2_normal')
    config['switch']['PC2_fixed'] = config_file(_switch_file_, "setting %s"%i, 'PC2_fixed')
    config['switch']['PC2_forbidden'] = config_file(_switch_file_, "setting %s"%i, 'PC2_forbidden')
    config.write(open(_config_file_, "w"))

# 將fw_config.ini內容取代control_config.ini
def alter_fw_to_config(_config_file_, _fw_file_,i):
    config = myconf()
    config.read(_config_file_, encoding="utf-8")
    config['Firmware config']['Firmware_config'] = config_file(_fw_file_, 'fw %s'%i, 'fw')
    config.write(open(_config_file_, "w"))

# 直接改變config.ini某欄參數
def alter_parameter_to_config(_config_file_,offset1,offset2,i):
    def alter(_config_file_, offset1, offset2,i):
        file_data = ""
        old_str = config_file(_config_file_, offset1, offset2)
        with open(_config_file_, "r", encoding="utf-8") as f:
            for line in f:
                line = line.replace(old_str,i)
                file_data += line
        with open(_config_file_,"w",encoding="utf-8") as f:
            f.write(file_data)
    alter(_config_file_, offset1,offset2,i)   

# 將config.ini內容取代set_netns_net0.sh
def alter_config_to_set_netns_net0(_config_file_,_alter_file_):
    def alter(_config_file_, offset1, offset2, _alter_file_, count, field):
        file_data = ""
        f = open(_alter_file_,'r')
        lines = f.readlines()[count]
        old_str = lines.split('=')
        new_str = config_file(_config_file_, offset1, offset2)

        with open(_alter_file_, "r") as f:
            for line in f:
                lines = line.replace(old_str[field],new_str+"\n")
                file_data += lines
        with open(_alter_file_,"w") as f:
            f.write(file_data)
    alter(_config_file_, "Net Namespace Set 1", "NS1_NAME"   , _alter_file_, 7, 1)    # NS1_NAME    # NS1
    alter(_config_file_, "Net Namespace Set 1", "NS1_VID"    , _alter_file_, 8, 1)    # NS1_VID
    alter(_config_file_, "Net Namespace Set 1", "NS1_BASE_IF", _alter_file_, 9, 1)    # NS1_BASE_IF
    alter(_config_file_, "Net Namespace Set 1", "NS1_IP4"    , _alter_file_, 10, 1)   # NS1_IP4
    alter(_config_file_, "Net Namespace Set 1", "NS1_MASK4"  , _alter_file_, 11, 1)   # NS1_MASK4
    alter(_config_file_, "Net Namespace Set 1", "NS1_GW4"    , _alter_file_, 12, 1)   # NS1_GW4
    alter(_config_file_, "Net Namespace Set 1", "NS1_IP6"    , _alter_file_, 13, 1)   # NS1_IP6
    alter(_config_file_, "Net Namespace Set 1", "NS1_MASK6"  , _alter_file_, 14, 1)   # NS1_MASK6
    alter(_config_file_, "Net Namespace Set 1", "NS1_GW6"    , _alter_file_, 15, 1)   # NS1_GW6
    alter(_config_file_, "Net Namespace Set 2", "NS2_NAME"   , _alter_file_, 18, 1)    # NS2_NAME    # NS2
    alter(_config_file_, "Net Namespace Set 2", "NS2_VID"    , _alter_file_, 19, 1)    # NS2_VID
    alter(_config_file_, "Net Namespace Set 2", "NS2_BASE_IF", _alter_file_, 20, 1)    # NS2_BASE_IF
    alter(_config_file_, "Net Namespace Set 2", "NS2_IP4"    , _alter_file_, 21, 1)   # NS2_IP4
    alter(_config_file_, "Net Namespace Set 2", "NS2_MASK4"  , _alter_file_, 22, 1)   # NS2_MASK4
    alter(_config_file_, "Net Namespace Set 2", "NS2_GW4"    , _alter_file_, 23, 1)   # NS2_GW4
    alter(_config_file_, "Net Namespace Set 2", "NS2_IP6"    , _alter_file_, 24, 1)   # NS2_IP6
    alter(_config_file_, "Net Namespace Set 2", "NS2_MASK6"  , _alter_file_, 25, 1)   # NS2_MASK6
    alter(_config_file_, "Net Namespace Set 2", "NS2_GW6"    , _alter_file_, 26, 1)   # NS2_GW6

# 將config.ini內容取代set_netns_net1.sh
def alter_config_to_set_netns_net1(_config_file_,_alter_file_):
    def alter(_config_file_, offset1, offset2, _alter_file_, count, field):
        file_data = ""
        f = open(_alter_file_,'r')
        lines = f.readlines()[count]
        old_str = lines.split('=')
        new_str = config_file(_config_file_, offset1, offset2)

        with open(_alter_file_, "r") as f:
            for line in f:
                lines = line.replace(old_str[field],new_str+"\n")
                file_data += lines
        with open(_alter_file_,"w") as f:
            f.write(file_data)
    alter(_config_file_, "Net Namespace Set 1", "NS1_NAME"   , _alter_file_, 7, 1)    # NS1_NAME    # NS1
    alter(_config_file_, "Net Namespace Set 1", "NS1_VID"    , _alter_file_, 8, 1)    # NS1_VID
    alter(_config_file_, "Net Namespace Set 1", "NS1_BASE_IF", _alter_file_, 9, 1)    # NS1_BASE_IF
    alter(_config_file_, "Net Namespace Set 1", "NS1_IP4"    , _alter_file_, 10, 1)   # NS1_IP4
    alter(_config_file_, "Net Namespace Set 1", "NS1_MASK4"  , _alter_file_, 11, 1)   # NS1_MASK4
    alter(_config_file_, "Net Namespace Set 1", "NS1_GW4"    , _alter_file_, 12, 1)   # NS1_GW4
    alter(_config_file_, "Net Namespace Set 1", "NS1_IP6"    , _alter_file_, 13, 1)   # NS1_IP6
    alter(_config_file_, "Net Namespace Set 1", "NS1_MASK6"  , _alter_file_, 14, 1)   # NS1_MASK6
    alter(_config_file_, "Net Namespace Set 1", "NS1_GW6"    , _alter_file_, 15, 1)   # NS1_GW6
    alter(_config_file_, "Net Namespace Set 2", "NS2_NAME"   , _alter_file_, 18, 1)    # NS2_NAME    # NS2
    alter(_config_file_, "Net Namespace Set 2", "NS2_VID"    , _alter_file_, 19, 1)    # NS2_VID
    alter(_config_file_, "Net Namespace Set 2", "NS2_BASE_IF", _alter_file_, 20, 1)    # NS2_BASE_IF
    alter(_config_file_, "Net Namespace Set 2", "NS2_IP4"    , _alter_file_, 21, 1)   # NS2_IP4
    alter(_config_file_, "Net Namespace Set 2", "NS2_MASK4"  , _alter_file_, 22, 1)   # NS2_MASK4
    alter(_config_file_, "Net Namespace Set 2", "NS2_GW4"    , _alter_file_, 23, 1)   # NS2_GW4
    alter(_config_file_, "Net Namespace Set 2", "NS2_IP6"    , _alter_file_, 24, 1)   # NS2_IP6
    alter(_config_file_, "Net Namespace Set 2", "NS2_MASK6"  , _alter_file_, 25, 1)   # NS2_MASK6
    alter(_config_file_, "Net Namespace Set 2", "NS2_GW6"    , _alter_file_, 26, 1)   # NS2_GW6


# 將config.ini內容取代目標文件某行某格
def alter(_origin_file_, line, field, _config_file_, offset1, offset2):
    file_data = ""
    f = open(_origin_file_,'r')
    lines = f.readlines()[line]
    old_str = lines.split(' ')
    new_str = config_file(_config_file_, offset1, offset2)
    with open(_origin_file_, "r") as f:
        for line in f:
            line = line.replace(old_str[field],new_str)
            file_data += line
    with open(_origin_file_,"w") as f:
        f.write(file_data)

# 用cle燒fw
def cle_set(cle, fw):
    cmd = '''D: & \
    cd %s & \
    cle.exe spi erase all & \
    cle.exe spi update %s & \
    ''' %(cle,fw)
    if fw != '':
        os.system(cmd)

# NET0
def paramiko_net0(HOST,USER,PASSWORD,PORT,source_code_local,source_code_client):
    # 連線server與client並執行指令   
    class AllowAllKeys(pm.MissingHostKeyPolicy):
        def missing_host_key(self, client, hostname, key):
            return

    transport = pm.Transport((HOST,int(PORT))) 
    transport.connect(username = USER, password = PASSWORD)
    sftp = pm.SFTPClient.from_transport(transport)
    sftp.put(source_code_local,source_code_client)

    client = pm.SSHClient()
    client.load_system_host_keys()
    client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    client.set_missing_host_key_policy(AllowAllKeys())
    client.connect(HOST,PORT,USER,PASSWORD)

    session = client.get_transport().open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command('''
    cd /home/pi/Desktop
    echo "raspberry" | sudo -S unzip RaspberryPi.zip
    cp CN5SW1/Desktop/AutoTest\ Platform/Source\ Code/client/RaspberryPi/set_netns_net0.sh set_netns.sh
    echo "raspberry" | sudo -S chmod +x set_netns.sh
    dos2unix set_netns.sh
    ./set_netns.sh
    sudo rm -r CN5SW1
    sudo rm set_netns.sh error.txt RaspberryPi.zip
    '''
    )
    stdin = session.makefile('wb', -1)
    stdout = session.makefile('rb', -1)
    stdin.write('net0 done\n')
    stdin.flush()
    print(stdout.read().decode("utf-8"))
    stdout.close()
    stdin.close()
    client.close()
    session.close()
    transport.close()

# NET1
def paramiko_net1(HOST,USER,PASSWORD,PORT,source_code_local,source_code_client):
    # 連線server與client並執行指令   
    class AllowAllKeys(pm.MissingHostKeyPolicy):
        def missing_host_key(self, client, hostname, key):
            return

    transport = pm.Transport((HOST,int(PORT))) 
    transport.connect(username = USER, password = PASSWORD)
    sftp = pm.SFTPClient.from_transport(transport)
    sftp.put(source_code_local,source_code_client)

    client = pm.SSHClient()
    client.load_system_host_keys()
    client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    client.set_missing_host_key_policy(AllowAllKeys())
    client.connect(HOST,PORT,USER,PASSWORD)

    session = client.get_transport().open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command('''
    cd /home/pi/Desktop
    echo "raspberry" | sudo -S unzip RaspberryPi.zip
    cp CN5SW1/Desktop/AutoTest\ Platform/Source\ Code/client/RaspberryPi/set_netns_net1.sh set_netns.sh
    echo "raspberry" | sudo -S chmod 777 set_netns.sh
    dos2unix set_netns.sh
    ./set_netns.sh
    sudo rm -r CN5SW1
    
    '''
    )
    stdin = session.makefile('wb', -1)
    stdout = session.makefile('rb', -1)
    stdin.write('net1 done\n')
    stdin.flush()
    print(stdout.read().decode("utf-8"))
    stdout.close()
    stdin.close()
    client.close()
    session.close()
    transport.close()
    
# main
def paramiko_link(HOST,USER,PASSWORD,PORT,main_local,main_client,source_code_local,source_code_client,result_client,result_local,i):
    
    # 連線server與client並執行指令   
    class AllowAllKeys(pm.MissingHostKeyPolicy):
        def missing_host_key(self, client, hostname, key):
            return

    transport = pm.Transport((HOST,int(PORT))) 
    transport.connect(username = USER, password = PASSWORD)
    sftp = pm.SFTPClient.from_transport(transport)
    sftp.put(main_local,main_client)
    sftp.put(source_code_local,source_code_client)

    client = pm.SSHClient()
    client.load_system_host_keys()
    client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    client.set_missing_host_key_policy(AllowAllKeys())
    client.connect(HOST,22,USER,PASSWORD)

    session = client.get_transport().open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command('''
    cd /home/pi/Desktop
    echo "raspberry" | sudo -S rm Result.zip
    echo "raspberry" | sudo -S chmod 777 main.sh
    dos2unix main.sh
    ./main.sh
    sudo rm packet_capture.sh packet_offset.sh packet_transfer.sh error.txt ping_record.txt main.sh RaspberryPi.zip set_netns.sh
    sudo rm -r txt Result packet_transfer_programs CN5SW1 
    '''
    )
    stdin = session.makefile('wb', -1)
    stdout = session.makefile('rb', -1)
    stdin.write('main.sh done\n')
    stdin.flush()
    print(stdout.read().decode("utf-8"))
    stdout.close()
    stdin.close()
    client.close()
    session.close()
    sftp.get(result_client, result_local+"%s.zip"%(int(i/2)+1))  #將/home/rtk/Desktop/Result.zip內容存到D:\perry_lai\Desktop\\Result(i).zip
    sftp.close()
    transport.close()

# switch 設定
def switch_set(HOST,USER,PASSWORD,PORT):
    # 自動代入剛才設定好的host IP and port.
    tn = telnetlib.Telnet()
    tn.open(HOST,PORT)

    # 要符合Cisco設備所出現的提示字元, 故改為Username: 
    tn.read_until(b"User name:")
    # user會代入剛才手動輸入的帳戶名
    tn.write(USER.encode('ascii') + b"\n")
    if PASSWORD:
    # 要符合設備所出現的提示字元, Cisco設備會出現Password:
        tn.read_until(b"Password: ")
    # 把剛才手動輸入的密碼帶入
        tn.write(PASSWORD.encode('ascii') + b"\n")

    # 這邊可以寫上我將要在登入設備後去執行的指令
    tn.write(b"configure\n")

    tn.write(b"vlan 1\n")
    tn.write(b"fixed 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28\n")
    tn.write(b"forbidden 1,2,3,4\n")
    tn.write(b"exit\n")

    tn.write(b"vlan 2\n")
    tn.write(b"forbidden 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28\n")
    tn.write(b"fixed 1,2,3,4\n")
    tn.write(b"exit\n")

    tn.write(b"vlan 5\n")
    tn.write(b"forbidden 1,2,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28\n")
    tn.write(b"fixed 3,4\n")
    tn.write(b"exit\n")

# 將ip list內容以空白為分隔方式儲存
def ip_field(_ip_list_file_, count, field):
    f = open(_ip_list_file_,'r')
    lines = f.readlines()[count]
    str = lines.split(' ')
    return str[field]

# 移動檔案的功能
def movefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print ("%s not exist!" %srcfile)
    else:
        fpath=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print ("move %s -> %s" %srcfile,dstfile)
 
# 複製檔案的功能
def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print ("%s not exist!" %srcfile)
    else:
        fpath=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print ("copy %s -> %s" %(srcfile,dstfile))

# 控制顯示欄位
def field_define(Read_in_File, location, length, mode):
    fr = open (Read_in_File, 'r')
    if mode == 1:
        fr.seek(int(location)-1)
        result = fr.read(int(length))
        return result
    elif mode == 0 :
        fr.close()
    else:
        exit(1)

# 將ipv4 address變成10進位
def ip_addr(ip):
    IP_1 = ip[0]+ip[1]; IP_2 = ip[2]+ip[3]; IP_3 = ip[4]+ip[5]; IP_4 = ip[6]+ip[7]
    IP = f"{int(IP_1, 16)}.{int(IP_2, 16)}.{int(IP_3, 16)}.{int(IP_4, 16)}"
    return IP

# 判斷路徑資料夾下有多少檔案(不含資料夾)
def file_num(path):
    num_files = len([f for f in os.listdir(path)
                    if os.path.isfile(os.path.join(path, f))])
    return num_files

# 判斷任意Seqence Number是否重複出現
def seq_num_pair(seq_file,pair_file): 
    count = len(open(seq_file,'rU').readlines()) 
    for i in range(count): 
        with open(seq_file) as fseq:
            seq_num = fseq.readlines()[i].split("\n")[0] 
        file_object = open(seq_file,'r')
        all_the_text = file_object.readlines()
        pair = 0
        for j in range(count):
            line = all_the_text[j].rstrip() 
            file_object.close()
            if (seq_num == line):
                pair = pair + 1
            else:
                pair = pair
        if (pair % 2 == 0):
            with open(pair_file, 'a') as fs:                   
                fs.write (seq_num+"\n")

# 將文件中的重複字串刪除
def uniq(pair_file,result_file):
    if os.path.exists("tmp.txt"): # 先刪掉暫存檔
        if os.path.isfile("tmp.txt"):
            os.remove("tmp.txt")
    with open(pair_file, 'a') as fr:
        print("", file=fr)
    with open(pair_file, 'r') as fr:    # 打開需要處理的檔案和放入重新整理資料的檔案
        with open("tmp.txt", 'w') as fw:
            # 刪除重複的
            print (''.join(list(set([i for i in fr]))), file = fw)
            print("", file = fw)
    with open("tmp.txt", "r") as f:
        data = f.readlines()
        data.sort()
        for i in range(len(data)):
            with open(result_file, "a") as f:
                if data[i].split():               
                    print (data[i].split("\n")[0], file = f)
                else:
                    print ("", end='', file = f)
    f1 = open(pair_file, 'r')
    f2 = open("tmp3.txt", 'w')
    lines = f1.readlines()
    for line in lines:
        line = line.strip()
        if line.split():
            f2.writelines(line+"\n")
        else:
            f2.writelines("")
    f1 = open(pair_file, 'w')
    f2 = open("tmp3.txt", 'r')
    lines = f2.readlines()
    for line in lines:
        line = line.strip()
        if line.split():
            f1.writelines(line+"\n")
        else:
            f1.writelines("")
            
# 移除不會自動重制內容的文件，如不存在文件也不會跳錯誤通知
def remove_old_file(file_path):
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)
    else:
        print("", end='')

# 判斷有多少%是loss的 
def loss_ratio(seq_num_file, result_file):
    with open(seq_num_file, "r") as f:
        seq_num = f.readlines()
    with open(result_file, "r") as f:
        pair_num = f.readlines()
    ratio = (len(pair_num)*2)/len(seq_num)
    return str(ratio*100)+'%'

# 判斷是否為連續數字
def continuous_number(file_path):
    if os.path.getsize(file_path) != 0: # 若檔案為空則不做以下的事情
        with open(file_path, "r") as f:
            num_list = f.readlines()
            first = int(num_list[0],16)
            last = int(num_list[len(num_list)-1],16)
            rangee = last - first
            #print(str(first)+" "+str(last)+" "+str(rangee), end='')
            loss = 0
            for i in range(rangee): # 從第一行的值到最後一行的值
                if i+1 < len(num_list):
                    loss_first = int(num_list[i],16)
                    loss_next = int(num_list[i+1],16)
                    if loss_next - loss_first != 1: # 每行都跟上一行相減，若差值不是1表示非連續  ##模組化!!!
                        for j in range(loss_first+1,loss_next):
                            print ("Loss "+hex(j))               # 列出loss的部分
                            loss = loss+1                # loss的記數 + 1
                            # 這裡可以放置其他要對loss的內容作的處置
            if loss == 0:
                a="No loss."
            else:
                a="loss"
            return a

def switch_portset(HOST,USER,PASSWORD,PORT,vlan,normal,fixed,forbidden):
    if HOST != '':
        tn = telnetlib.Telnet()
        tn.open(HOST,PORT)
        tn.read_until(b"User name:")
        tn.write(USER.encode('ascii') + b"\n")
        if PASSWORD:
            tn.read_until(b"Password: ")
            tn.write(PASSWORD.encode('ascii') + b"\n")
        tn.write(b"configure\n")
        tn.write(b"vlan " + vlan.encode() + b"\n")
        tn.write(b"normal " + normal.encode() + b"\n")
        tn.write(b"fixed " + fixed.encode() + b"\n")
        tn.write(b"forbidden " + forbidden.encode() + b"\n")
        tn.write(b"exit\n")

#def check_item(_check_file_,item):
    #return result