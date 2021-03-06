#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sup
import os.path
import shutil
import ipaddress
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
num_files = len(sup.config_file_all_title(ip_config))

print("----------------------------------------------------------")

#寫入最終結果的文件
result_file = "%s\\Final.txt"%(output)
sup.remove_old_file(result_file)
# 初始化所有資料夾
for i in range(num_files):
    i=i+1
    output_icmp_dir_Result = "%s\\Result%r" %(output_icmp_dir,i)  # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\ICMP\\Result%r
    output_icmpv6_dir_Result = "%s\\Result%r" %(output_icmpv6_dir,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\ICMPv6\\Result%r
    output_tcp_dir_Result = "%s\\Result%r" %(output_tcp_dir,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\TCP\\Result%r
    
    if os.path.isdir(output_icmp_dir_Result):
        shutil.rmtree(output_icmp_dir_Result)
    
    if not os.path.isdir(output_icmp_dir_Result):
        os.mkdir(output_icmp_dir_Result)

    if os.path.isdir(output_icmpv6_dir_Result):
        shutil.rmtree(output_icmpv6_dir_Result)
    
    if not os.path.isdir(output_icmpv6_dir_Result):
        os.mkdir(output_icmpv6_dir_Result)
    
    if os.path.isdir(output_tcp_dir_Result):
        shutil.rmtree(output_tcp_dir_Result)
    
    if not os.path.isdir(output_tcp_dir_Result):
        os.mkdir(output_tcp_dir_Result)

# 主要分析環節
for i in range(num_files): #1): 
    i=i+1
    output_icmp_dir_Result = "%s\\Result%r" %(output_icmp_dir,i)  # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\ICMP\\Result%r
    output_icmpv6_dir_Result = "%s\\Result%r" %(output_icmpv6_dir,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\ICMPv6\\Result%r
    output_tcp_dir_Result = "%s\\Result%r" %(output_tcp_dir,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\TCP\\Result%r
    # 回傳以日期為檔名的資料夾
    target_dir = os.listdir("%s\\Result%r\\Result"%(testcase_path,i))[0]
    # 以日期為檔名的資料夾底下有多少packet
    num_packet = sup.file_num("%s\\Result%r\\Result\\%s"%(testcase_path,i,target_dir))
    #放同一包日期文件中，每件封包的 Sequence Number 的文件
    seq_icmp_file = "%s\\SeqNum%r.txt"%(output_icmp_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\SeqNum%r.txt
    seq_icmpv6_file = "%s\\SeqNum%r.txt"%(output_icmpv6_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\SeqNum%r.txt
    seq_tcp_file = "%s\\SeqNum%r.txt"%(output_tcp_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\SeqNum%r.txt
    #放 Sequence Number 文件中成對者的文件
    pair_icmp_file = "%s\\Pair%r.txt"%(output_icmp_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\Pair%r.txt
    pair_icmpv6_file = "%s\\Pair%r.txt"%(output_icmpv6_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\Pair%r.txt
    pair_tcp_file = "%s\\Pair%r.txt"%(output_tcp_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\output\\Pair%r.txt
    #放配對成功的Sequence Number 的文件
    result_icmp_file = "%s\\Result%r.txt"%(output_icmp_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\outpu\\Result%r.txt
    result_icmpv6_file = "%s\\Result%r.txt"%(output_icmpv6_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\outpu\\Result%r.txt
    result_tcp_file = "%s\\Result%r.txt"%(output_tcp_dir_Result,i) # D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase\\outpu\\Result%r.txt

    sup.remove_old_file(seq_icmp_file)
    sup.remove_old_file(pair_icmp_file)
    sup.remove_old_file(result_icmp_file)

    sup.remove_old_file(seq_icmpv6_file)
    sup.remove_old_file(pair_icmpv6_file)
    sup.remove_old_file(result_icmpv6_file)

    sup.remove_old_file(seq_tcp_file)
    sup.remove_old_file(pair_tcp_file)
    sup.remove_old_file(result_tcp_file)

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
            print("Network_Layer_Type: %s"%Network_Layer_Type)
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
    
    if Network_Layer_Type == "0800":             
        sup.seq_num_pair(seq_icmp_file,pair_icmp_file)                                                                    # check seq nums are pair or not
        sup.uniq(pair_icmp_file,result_icmp_file)                                                                         # delete 重複的 seq num
        if sup.loss_ratio(seq_icmp_file, result_icmp_file) == '100.0%':
            print("Testcase %r success ratio for ICMP: %s ( %s )"%(i,sup.loss_ratio(seq_icmp_file, result_icmp_file),sup.continuous_number(result_icmp_file)))                                     # 判斷是否連續
        else:
            print("Testcase %r success ratio for ICMP: %s"%(i,sup.loss_ratio(seq_icmp_file, result_icmp_file)))                                     # 判斷是否連續
        with open(result_file, 'a') as fw:
            if sup.loss_ratio(seq_icmp_file, result_icmp_file) == '100.0%':
                fw.write ("Testcase "+ "%s"%i + " success ratio for ICMP: " + sup.loss_ratio(seq_icmp_file, result_icmp_file)+ " ( " + sup.continuous_number(result_icmp_file) + " )\n")
            else:
                fw.write ("Testcase "+ "%s"%i + " success ratio for ICMP: " + sup.loss_ratio(seq_icmp_file, result_icmp_file) + "\n")
        fw.close()
    elif Network_Layer_Type == "86dd":
        sup.seq_num_pair(seq_icmpv6_file,pair_icmpv6_file)                                                                    # check seq nums are pair or not
        sup.uniq(pair_icmpv6_file,result_icmpv6_file)                                                                     # delete 重複的 seq num
        if sup.loss_ratio(seq_icmpv6_file, result_icmpv6_file) == '100.0%':
            print("Testcase %r success ratio for ICMPv6: %s ( %s )"%(i,sup.loss_ratio(seq_icmpv6_file, result_icmpv6_file),sup.continuous_number(result_icmpv6_file)))                                 # 判斷是否連續
        else:
            print("Testcase %r success ratio for ICMPv6: %s"%(i,sup.loss_ratio(seq_icmpv6_file, result_icmpv6_file)))                                 # 判斷是否連續
        with open(result_file, 'a') as fw:
            if sup.loss_ratio(seq_icmpv6_file, result_icmpv6_file) == '100.0%':
                fw.write ("Testcase "+ "%s"%i + " success ratio for ICMPv6: " + "%s"%sup.loss_ratio(seq_icmpv6_file, result_icmpv6_file) + " ( " + sup.continuous_number(result_icmpv6_file) + " )\n")
            else:
                fw.write ("Testcase "+ "%s"%i + " success ratio for ICMPv6: " + "%s"%sup.loss_ratio(seq_icmpv6_file, result_icmpv6_file) + "\n")
        fw.close()
    else:
        print("Testcase %r: No Result."%i)                                 # 判斷是否連續
        with open(result_file, 'a') as fw:
            fw.write ("Testcase "+ "%s"%i + ": No Result." + "\n")
        fw.close()
print("----------------------------------------------------------")