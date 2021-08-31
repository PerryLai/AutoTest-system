#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sup
import os.path
import shutil
import ipaddress

# 初始化所有資料夾
#for i in range(num_files):
def init_folder(output_dir,i):
    output_dir_Result = "%s\\Result%r" %(output_dir,i)
    # output_icmp_dir_Result = "%s\\Result%r" %(output_icmp_dir,i)  # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\ICMP\\Result%r
    # output_icmpv6_dir_Result = "%s\\Result%r" %(output_icmpv6_dir,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\ICMPv6\\Result%r
    # output_tcp_dir_Result = "%s\\Result%r" %(output_tcp_dir,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\TCP\\Result%r
    
    if os.path.isdir(output_dir_Result):
        shutil.rmtree(output_dir_Result)
    if not os.path.isdir(output_dir_Result):
        os.mkdir(output_dir_Result)

def analyzing_core(output,testcase_config,testcase_path,output_icmp_dir,output_icmpv6_dir,i):
      icmp_core(output,testcase_config,testcase_path,output_icmp_dir,output_icmpv6_dir,i)

# analyze for icmp & icmpv6
def icmp_core(output,testcase_config,testcase_path,output_icmp_dir,output_icmpv6_dir,i):

    # 預備輸出的output底下的資料夾
    output_icmp_dir_Result = "%s\\Result%r" %(output_icmp_dir,i)  # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\ICMP\\Result%r
    output_icmpv6_dir_Result = "%s\\Result%r" %(output_icmpv6_dir,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\ICMPv6\\Result%r
    # 回傳以日期為檔名的資料夾
    target_dir = os.listdir("%s\\Result%r\\Result"%(testcase_path,i))[0]
    # 以日期為檔名的資料夾底下有多少packet
    num_packet = sup.file_num("%s\\Result%r\\Result\\%s"%(testcase_path,i,target_dir))
    #放同一包日期文件中，每件封包的 Sequence Number 的文件
    seq_icmp_file = "%s\\SeqNum%r.txt"%(output_icmp_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\SeqNum%r.txt
    seq_icmpv6_file = "%s\\SeqNum%r.txt"%(output_icmpv6_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\SeqNum%r.txt
    #放 Sequence Number 文件中成對者的文件
    pair_icmp_file = "%s\\Pair%r.txt"%(output_icmp_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\Pair%r.txt
    pair_icmpv6_file = "%s\\Pair%r.txt"%(output_icmpv6_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\Pair%r.txt
    #放配對成功的Sequence Number 的文件
    result_icmp_file = "%s\\Result%r.txt"%(output_icmp_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\outpu\\Result%r.txt
    result_icmpv6_file = "%s\\Result%r.txt"%(output_icmpv6_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\outpu\\Result%r.txt

    sup.remove_old_file(seq_icmp_file)
    sup.remove_old_file(pair_icmp_file)
    sup.remove_old_file(result_icmp_file)

    sup.remove_old_file(seq_icmpv6_file)
    sup.remove_old_file(pair_icmpv6_file)
    sup.remove_old_file(result_icmpv6_file)

    Network_Layer_Type = "0"

    # 對同一包Result下的所有packet分析
    for j in range(num_packet):
        # 純粹回傳packet1~10檔名
        Read_in_File=[f for f in os.listdir("%s\\Result%r\\Result\\%s"%(testcase_path,i,target_dir)) if os.path.isfile(os.path.join("%s\\Result%r\\Result\\%s"%(testcase_path,i,target_dir),f))][j]
        #print("Read_in_File%s: "%j +"%s"%Read_in_File + "\n")
        # packet1~10 完整路徑
        Read_in_File_Path = ("%s\\Result%r\\Result\\%s\\%s"%(testcase_path,i,target_dir,Read_in_File))
        # packet1~10 的尺寸
        size = os.path.getsize(Read_in_File_Path)
        Data_Link_Layer_Distination = sup.field_define(Read_in_File_Path,1,12,1)                                                 # 1~12
        Data_Link_Layer_Source = sup.field_define(Read_in_File_Path,13,12,1)                                                     # 13~24
        VLAN_Layer_Type = sup.field_define(Read_in_File_Path,25,4,1)                                                             # 25~28
        if VLAN_Layer_Type == "8100":                                                                                            # 表示 vLan Type 是 802.1Q Virtual LAN
            Network_Layer_ID = sup.field_define(Read_in_File_Path,29,4,1)                                                        # 29~32
            Network_Layer_Type = sup.field_define(Read_in_File_Path,33,4,1)                                                      # 33~36
            #print("Network_Layer_Type: %s"%Network_Layer_Type)
            if Network_Layer_Type == "0800":                                                                                     # 表示 Network Layer Type 是 IPv4
                Network_Layer_Version = sup.field_define(Read_in_File_Path,37,1,1)                                               # 37
                Network_Layer_Header_Length = sup.field_define(Read_in_File_Path,38,1,1)                                         # 38
                Network_Layer_Differentiated_Services_Field = sup.field_define(Read_in_File_Path,39,2,1)                         # 39~40
                Network_Layer_Total_Length = sup.field_define(Read_in_File_Path,41,4,1)                                          # 41~44
                Network_Layer_Identification = sup.field_define(Read_in_File_Path,45,4,1)                                        # 45~48
                Network_Layer_Flags = sup.field_define(Read_in_File_Path,49,4,1)                                                 # 49~52
                Network_Layer_Time_to_live = sup.field_define(Read_in_File_Path,53,2,1)                                          # 53~54                                               
                Protocol = sup.field_define(Read_in_File_Path,55,2,1)                                                            # 55~56
                if Protocol == "01":                                                                                        # 表示 Transport Layer 是 ICMP
                    Protocol_name = "ICMP"
                    Network_Layer_Header_Checksum = sup.field_define(Read_in_File_Path,57,4,1)                                   # 57~60
                    Source = sup.field_define(Read_in_File_Path,61,8,1); Source_IP = str(ipaddress.ip_network(int(Source,16)))                         # 61~68
                    Destination = sup.field_define(Read_in_File_Path,69,8,1); Destination_IP = str(ipaddress.ip_network(int(Source,16)))          # 69~76
                    Transport_Layer_Type = sup.field_define(Read_in_File_Path,77,2,1)                                            # 77~78
                    Transport_Layer_Code = sup.field_define(Read_in_File_Path,79,2,1)                                            # 79~80
                    Transport_Layer_Checksum = sup.field_define(Read_in_File_Path,81,4,1)                                        # 81~84
                    Transport_Layer_Identifier_BE = sup.field_define(Read_in_File_Path,85,4,1)                                   # 85~88
                    Transport_Layer_Sequence_Number_BE = sup.field_define(Read_in_File_Path,89,4,1)                              # 89~92
                    Transport_Layer_Timestamp = sup.field_define(Read_in_File_Path,93,16,1)                                      # 93~108
                    Data = sup.field_define(Read_in_File_Path,109, int(size)-1,1)                                                # 108~last

                    ### 分析時產出文件的位址 ###
                    output_icmp_file = "%s\\Result%r\\output%r.txt" %(sup.config_file(testcase_config, "Testcase", "output_icmp_dir"),i,j+1)
                    with open(seq_icmp_file, 'a') as fw:
                        fw.write (Transport_Layer_Sequence_Number_BE+"\n")
                    fw.close()

                    if Transport_Layer_Type == "00":
                        Transport_Layer_Type_Re = "Reply"
                    elif Transport_Layer_Type == "08":
                        Transport_Layer_Type_Re = "Request"

                    with open(output_icmp_file, 'a') as fw:
                        fw.write ("---------- Data Link Layer ----------\n")
                        fw.write ("\n")
                        fw.write ("Data Link Layer Distination: "+Data_Link_Layer_Distination+"\n")
                        fw.write ("Data Link Layer Source: "+Data_Link_Layer_Source+"\n")
                        fw.write ("VLAN Layer Type: "+VLAN_Layer_Type+"\n")
                        fw.write (""+"\n")
                        fw.write ("---------- Network Layer ----------"+"\n")
                        fw.write (""+"\n")
                        fw.write ("Network Layer ID: "+Network_Layer_ID+"\n")
                        fw.write ("Network Layer Type: "+Network_Layer_Type+" ("+Protocol_name+")"+"\n")
                        fw.write ("Network Layer Version: "+Network_Layer_Version+"\n")
                        fw.write ("Network Layer Header Length: "+Network_Layer_Header_Length+"\n")
                        fw.write ("Network Layer Differentiated Services Field: "+Network_Layer_Differentiated_Services_Field+"\n")
                        fw.write ("Network Layer Total Length: "+Network_Layer_Total_Length+"\n")
                        fw.write ("Network Layer Identification: "+Network_Layer_Identification+"\n")
                        fw.write ("Network Layer Flags: "+Network_Layer_Flags+"\n")
                        fw.write ("Network Layer Time to live: "+Network_Layer_Time_to_live+"\n")
                        fw.write ("Protocol: "+Protocol+" ("+Protocol_name+")"+"\n")
                        fw.write ("Network Layer Header Checksum: "+Network_Layer_Header_Checksum+"\n")
                        fw.write ("Source IP: "+Source+" ("+Source_IP+")"+"\n")
                        fw.write ("Destination IP: "+Destination+" ("+Destination_IP+")"+"\n")
                        fw.write (""+"\n")
                        fw.write ("---------- Transport Layer ----------"+"\n")
                        fw.write (""+"\n")
                        fw.write ("Transport Layer Type: "+Transport_Layer_Type+" ("+Transport_Layer_Type_Re+")"+"\n")
                        fw.write ("Transport Layer Code: "+Transport_Layer_Code+"\n")
                        fw.write ("Transport Layer Checksum: "+Transport_Layer_Checksum+"\n")
                        fw.write ("Transport Layer Identifier BE: "+Transport_Layer_Identifier_BE+"\n")
                        fw.write ("Sequence Number: "+Transport_Layer_Sequence_Number_BE+"\n")
                        fw.write ("Transport Layer Timestamp: "+Transport_Layer_Timestamp+"\n")
                        fw.write (""+"\n")
                        fw.write ("Data: "+Data+"\n")  
                    fw.close()
                    #sup.seq_num_pair(seq_icmp_file,pair_icmp_file)                                                                    # check seq nums are pair or not

            if Network_Layer_Type == "86dd":                                                                                     # 表示 Network Layer Type 是 IPv6
                Network_Layer_Version = sup.field_define(Read_in_File_Path,37,1,1)                                               # 37
                Network_Layer_Traffic_Class = sup.field_define(Read_in_File_Path,38,2,1)                                         # 38~39
                Network_Layer_Flow_Label = sup.field_define(Read_in_File_Path,40,5,1)                                            # 40~44
                Network_Layer_Payload_Length = sup.field_define(Read_in_File_Path,45,4,1)                                        # 45~48
                Protocol = sup.field_define(Read_in_File_Path,49,2,1)                                                            # 49~50  #3a(58)=ICMPv6
                Transport_Layer_Type_Re = Protocol
                if Protocol == "3a":                                                                                             # 表示 Transport Layer 是 ICMPv6
                    Protocol_name = "ICMPv6"
                    Network_Layer_Hop_Limit = sup.field_define(Read_in_File_Path,51,2,1)                                         # 51~52
                    Source = sup.field_define(Read_in_File_Path,53,32,1); Source_IP = str(ipaddress.ip_network(int(Source,16)))                        # 53~84                                               
                    Destination = sup.field_define(Read_in_File_Path,85,32,1); Destination_IP = str(ipaddress.ip_network(int(Destination,16)))         # 85~116
                    Transport_Layer_Type_Ping_Echo = sup.field_define(Read_in_File_Path,117,2,1)                                 # 117~118

                    if Transport_Layer_Type_Ping_Echo == "80":
                        Transport_Layer_Type_Re = "Reply"
                    elif Transport_Layer_Type_Ping_Echo == "81":
                        Transport_Layer_Type_Re = "Request"
                    
                    Transport_Layer_Code = sup.field_define(Read_in_File_Path,119,2,1)                                           # 119~120
                    Transport_Layer_Checksum = sup.field_define(Read_in_File_Path,121,4,1)                                       # 121~124
                    Transport_Layer_Identifier = sup.field_define(Read_in_File_Path,125,4,1)                                     # 125~128
                    Transport_Layer_Sequence_Number = sup.field_define(Read_in_File_Path,129,4,1)                                # 129~132
                    Data = sup.field_define(Read_in_File_Path,133, int(size)-1,1)                                                # 133~last

                    ### 分析時產出文件的位址 ###
                    output_icmpv6_file = "%s\\Result%r\\output%r.txt" %(output_icmpv6_dir,i,j+1)
                    check_icmpv6_file = "%s\\Result%r\\check.txt" %(output_icmpv6_dir,i)

                    with open(check_icmpv6_file, 'a') as fw:
                        fw.write ("Packet: "+ "%s"%(j+1) +"\n") #DMAC
                        fw.write ("DMAC: "+Data_Link_Layer_Distination+"\n") #DMAC
                        fw.write ("SMAC: "+Data_Link_Layer_Source+"\n") #SMAC
                        fw.write ("VID: " +Network_Layer_ID+"\n") #VID
                        fw.write ("DIP: " +Destination_IP+"\n") #DIP
                        fw.write ("SIP: " +Source_IP+"\n") #SIP
                        fw.write ("Next hop: "+Network_Layer_Hop_Limit+"\n") #Next hop
                        fw.write ("-------------------------------------------------" + "\n")
                    fw.close()

                    with open(seq_icmpv6_file, 'a') as fw:
                        fw.write (Transport_Layer_Sequence_Number+"\n")
                    fw.close()
        
                    with open(output_icmpv6_file, 'a') as fw:
                        fw.write ("---------- Data Link Layer ----------\n")
                        fw.write ("\n")
                        fw.write ("DMAC: "+Data_Link_Layer_Distination+"\n")
                        fw.write ("SMAC: "+Data_Link_Layer_Source+"\n")
                        fw.write ("VLAN Layer Type: "+VLAN_Layer_Type+"\n")
                        fw.write (""+"\n")
                        fw.write ("---------- Network Layer ----------"+"\n")
                        fw.write (""+"\n")
                        fw.write ("Network Layer ID: "+Network_Layer_ID+"\n")
                        fw.write ("Network Layer Type: "+Network_Layer_Type+" ("+Protocol_name+")"+"\n")
                        fw.write ("Network Layer Version: "+Network_Layer_Version+"\n")
                        fw.write ("Network_Layer_Traffic_Class: "+Network_Layer_Traffic_Class+"\n")
                        fw.write ("Network_Layer_Flow_Label: "+Network_Layer_Flow_Label+"\n")
                        fw.write ("Network_Layer_Payload_Length: "+Network_Layer_Payload_Length+"\n")
                        fw.write ("Network_Layer_Hop_Limit: "+Network_Layer_Hop_Limit+"\n")
                        fw.write ("Source IP: "+Source+" ("+Source_IP+")"+"\n")
                        fw.write ("Destination IP: "+Destination+" ("+Destination_IP+")"+"\n")
                        fw.write ("Protocol: "+Protocol+" ("+Protocol_name+")"+"\n")
                        fw.write (""+"\n")
                        fw.write ("---------- Transport Layer ----------"+"\n")
                        fw.write (""+"\n")
                        if Transport_Layer_Type_Ping_Echo == "80":
                            Transport_Layer_Type_Re = "Reply"
                            fw.write ("Transport_Layer_Type_Ping_Echo: "+Transport_Layer_Type_Ping_Echo+" ("+Transport_Layer_Type_Re+")"+"\n")
                        elif Transport_Layer_Type_Ping_Echo == "81":
                            Transport_Layer_Type_Re = "Request"
                            fw.write ("Transport_Layer_Type_Ping_Echo: "+Transport_Layer_Type_Ping_Echo+" ("+Transport_Layer_Type_Re+")"+"\n")
                        fw.write ("Transport Layer Code: "+Transport_Layer_Code+"\n")
                        fw.write ("Transport Layer Checksum: "+Transport_Layer_Checksum+"\n")
                        fw.write ("Transport Layer Identifier: "+Transport_Layer_Identifier+"\n")
                        fw.write ("Sequence Number: "+Transport_Layer_Sequence_Number+"\n")
                        fw.write (""+"\n")
                        fw.write ("Data: "+Data+"\n")
                    fw.close()  
                    #sup.seq_num_pair(seq_icmpv6_file,pair_icmpv6_file)                                                        # check seq nums are pair or not
        #寫入最終結果的文件
    result_file = "%s\\Final.txt"%(output)
    if Network_Layer_Type == "0800":             
        sup.seq_num_pair(seq_icmp_file,pair_icmp_file)                                                                    # check seq nums are pair or not
        sup.uniq(pair_icmp_file,result_icmp_file)                                                                         # delete 重複的 seq num
        print("%r %s %s"%(i,sup.loss_ratio(seq_icmp_file, result_icmp_file),Protocol_name))                                                # 判斷是否連續
        with open(result_file, 'a') as fw:
            fw.write ("%s "%i + sup.loss_ratio(seq_icmp_file, result_icmp_file) + " %s\n"%Protocol_name)
        fw.close()
    elif Network_Layer_Type == "86dd":
        sup.seq_num_pair(seq_icmpv6_file,pair_icmpv6_file)                                                                    # check seq nums are pair or not
        sup.uniq(pair_icmpv6_file,result_icmpv6_file)                                                                     # delete 重複的 seq num
        print("%r %s %s"%(i,sup.loss_ratio(seq_icmpv6_file, result_icmpv6_file),Protocol_name))                                 # 判斷是否連續
        with open(result_file, 'a') as fw:
            fw.write ("%s "%i + "%s"%sup.loss_ratio(seq_icmpv6_file, result_icmpv6_file) + " %s\n"%Protocol_name)
        fw.close()
    else:
        print("%r: No Result."%i)                            
        with open(result_file, 'a') as fw:
            fw.write ("%s"%i + ": No Result." + "\n")
        fw.close()

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
