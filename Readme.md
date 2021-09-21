# Auto-Test System 基礎使用說明  
##### 開發者 : 賴沛冠 Perry Lai
## 一、 架構
---
## 二、使用說明
(一) 運行環境
***
    控制端 : windows    
    測試環境 : Raspberry Pi
(二) 測試前須知
1. 測試用的Pi必須事先在Raspberry Pi安裝的軟體
   * tshark  
        ```
        sudo apt install tshark
        ```
   * dos2unix  
        ```
        sudo apt install dos2unix
        ```
2. 測試前必須做的事情
   *  Raspberry Pi端必須先開啟ssh service  
        ```
        sudo service ssh restart
        ```
3. 使用步驟
    ***
   1. 對fw_config.ini、switch_config.ini、ip_config.ini做設定，同時檢查control_config.ini中的路徑是否都正確
   2. 使用RTKAutoSwitchTool_HCP5_VA_2.1.6.20.0進行fw_config.bin的燒錄，並將燒好的fw放到final_cle_210720 資料夾底下 (與cle同位址)  
      Tool的使用方法將於三-(五)、三-(六)做說明
   3. 確認Raspberry Pi皆已經打開ssh功能
   4. 執行control.py
   5. 等待結果，輸出會放置在testcase/output/Final.txt中

## 三、 文件說明
---
以下以資料夾為順序一一介紹
### (一)  config
測試前必須事先設好的資料。

1. ip_config.ini  
   **_需要使用者自行設定_**  
   設定資訊包括: 
    ```ini
    [Net Namespace Set 1]            # 每輪都必須新增一套新參數
    test_program = icmp.sh           # 要使用的封包type類別，若想要測試ipv6則將此欄改成icmpv6.sh
    NS1_NAME = net0                  # NS1表示要對第一台Pi做設定，NS2表示對第二台做設定
    NS1_VID = 10                     # 目前都是只能從Pi1傳送到Pi2
    NS1_BASE_IF = eth0
    NS1_IP4 = 192.168.1.20
    NS1_MASK4 = 24
    NS1_GW4 = 192.168.1.254
    NS1_IP6 = fd53:7cb8:383:2::10f
    NS1_MASK6 = 64
    NS1_GW6 = fd53:7cb8:383:2::fc10
    NS1_GW_MAC = 00:E0:4C:00:00:01
    NS2_NAME = net1
    NS2_VID = 20
    NS2_BASE_IF = eth0
    NS2_IP4 = 192.168.2.50
    NS2_MASK4 = 24
    NS2_GW4 = 192.168.2.254
    NS2_IP6 = fd53:7cb8:383:5::e
    NS2_MASK6 = 64
    NS2_GW6 = fd53:7cb8:383:5::fc10
    NS2_GW_MAC = 00:E0:4C:00:00:02
    ```
2. fw_config.ini  
   設定好每輪要使用的fw
   ```ini
    [RTKAutoSwitchTool]
    RTKAutoSwitchTool_fw_bin = D:\\CN5SW1\Desktop\\AutoTest Platform\\RTKAutoSwitchTool_VA_2.1.6.16.0\\fw_config.bin

    [fw 1]
    fw = fw_config.bin
   ```
3. switch_config.ini  
   設定好每輪要對Zyxwl Switch做的設定  
   CP = Control Panel 對 Switch port 的接口、PC1/2 = 傳輸用電腦對Switch Port 的接口、normal基本上全部設0、fixed為允許通行(同VID應一起設為fixed)、forbidden為禁止通行
   ```ini
    [setting 1]            # 每輪會使用全新的設定
    HOST=192.168.1.1      
    USER= admin
    PASSWORD= 1234
    PORT= 23
    CP_normal= 0
    CP_fixed= 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28       
    CP_forbidden= 1,2,3,4
    PC1_vlan= 10
    PC1_normal= 0
    PC1_fixed= 1,2
    PC1_forbidden= 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28
    PC2_vlan= 20
    PC2_normal= 0
    PC2_fixed= 3,4
    PC2_forbidden= 1,2,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28
   ```
4. config.ini  
   放入所有檔案的路徑，包括本地路徑與傳送到客戶端的預設路徑。[ ] 為大分類標籤，底下為項目。  ***需要使用者自行設定**  
   須注意，[Net Namespace Set 1] [Net Namespace Set 2] [switch] [Firmware config]，以上欄位須分別至ip/switch/fw_config.ini中設定，無法直接在control_config.ini中設定
    1. [Control Panel]  
        與control .py有關的檔案路徑與變數值皆存在這裡  
        ***若AutoTest Platform上層的資料夾名稱有變動再改就好了***
        ```ini
        [Control Panel]
        cle = D:\\CN5SW1\\Desktop\\AutoTest Platform\\final_cle_210720\\final_cle_210720
        AutoTest_Path = D:\\CN5SW1\\Desktop\\AutoTest Platform
        ip_list_file = D:\\CN5SW1\\Desktop\\AutoTest Platform\\ip_list.ini
        testcase_path = D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase
        HOST_net0 = 192.168.50.109  # PC1的wifi位址，需要與CP做溝通時用
        USER_net0 = pi
        PORT_net0 = 22
        PASSWORD_net0 = raspberry
        HOST_net1 = 192.168.50.36 # PC2的wifi位址，需要與CP做溝通時用
        USER_net1 = pi
        PORT_net1 = 22
        PASSWORD_net1 = raspberry
        zip_dir_srcPath = D:\\CN5SW1\\Desktop\\AutoTest Platform\\Source Code\\client\\RaspberryPi
        zip_dir_dstname = D:\\CN5SW1\\Desktop\\RaspberryPi.zip
        unzip_dir_srcName = D:\\CN5SW1\\Desktop
        unzip_dir_dstPath = D:\\CN5SW1\\Desktop\\AutoTest Platform\\testcase
        main_client = /home/pi/Desktop/main.sh
        source_code_client = /home/pi/Desktop/RaspberryPi.zip
        main_local = D:\\CN5SW1\\Desktop\\AutoTest Platform\\Source Code\\client\\RaspberryPi\\main.sh
        source_code_local = D:\\CN5SW1\\Desktop\\RaspberryPi.zip
        result_client = /home/pi/Desktop/Result.zip
        result_local = D:\\CN5SW1\\Desktop\\Result
        analyze = D:\\CN5SW1\\Desktop\\AutoTest Platform\\Source Code\\control panel\\packet analyze.py
        ```
    2. [ Client ]  
        要送到客戶端(即測試環境)的檔案路徑。  
        注意在此存放的是本地路徑，因為會先經過壓縮，所以不需要添加客戶端路徑，除非有需要。  
        ***若AutoTest Platform上層的資料夾名稱有變動再改就好了***

        ```ini
        [Client]
        main = D:\\CN5SW1\\Desktop\\AutoTest Platform\\Source Code\\client\\RaspberryPi\\main.sh
        packet_capture = D:\\CN5SW1\\Desktop\\AutoTest Platform\\Source Code\\client\\RaspberryPi\\packet_capture.sh
        packet_offset = D:\\CN5SW1\\Desktop\\AutoTest Platform\\Source Code\\client\\RaspberryPi\\packet_offset.sh
        packet_transfer = D:\\CN5SW1\\Desktop\\AutoTest Platform\\Source Code\\client\\RaspberryPi\\packet_transfer.sh
        set_netns_net0 = D:\\CN5SW1\\Desktop\\AutoTest Platform\\Source Code\\client\\RaspberryPi\\set_netns_net0.sh
        set_netns_net1 = D:\\CN5SW1\\Desktop\\AutoTest Platform\\Source Code\\client\\RaspberryPi\\set_netns_net1.sh
        test_program = icmp.sh # 要使用的測試程式，無法在此修改，需到ip_config.ini設定
        test_program_path = D:\\CN5SW1\\Desktop\\AutoTest Platform\\Source Code\\client\\RaspberryPi\\txt\\test_program.txt
        test_program_folder = D:\\CN5SW1\\Desktop\\AutoTest Platform\\Source Code\\client\\RaspberryPi\\packet_transfer_programs
        packet_ping_num = 500 # 要打的封包數
        packet_catch_num = 20 # 要抓取的封包數
        ```
    3. [ Net Namespace Set 1 ]  
        與第一個VLAN環境設置有關的資訊，會在每一輪測試中從ip_list抓新數據覆蓋，再拿去reset set_netns_net0.sh內的參數。  
        無法由此設定，須至ip_config.ini設定
        ```ini
        NS1_NAME = net0
        NS1_VID = 2
        NS1_BASE_IF = eth0
        NS1_IP4 = 192.168.2.29
        NS1_MASK4 = 24
        NS1_GW4 = 192.168.2.254
        NS1_IP6 = fd53:7cb8:383:2::10f
        NS1_MASK6 = 64
        NS1_GW6 = fd53:7cb8:383:2::fffe
        NS1_GW_MAC = 00:e0:4c:00:00:02
        ```
    4. [ Net Namespace Set 2 ]  
        與第二個VLAN環境設置有關的資訊，會在每一輪測試中從ip_list抓新數據覆蓋，再拿去reset set_netns_net1.sh內的參數。
        無法由此設定，須至ip_config.ini設定
        ```ini
        NS2_NAME = net1
        NS2_VID = 5
        NS2_BASE_IF = eth0
        NS2_IP4 = 192.168.5.59
        NS2_MASK4 = 24
        NS2_GW4 = 192.168.5.254
        NS2_IP6 = fd53:7cb8:383:5::e
        NS2_MASK6 = 64
        NS2_GW6 = fd53:7cb8:383:5::fffe
        NS2_GW_MAC = 00:e0:4c:00:00:05
        ```
    5. [switch]  
        測定作為hub交換機的port屬性設定
        無法由此設定，須至switch_config.ini設定
        ```ini
        HOST = 192.168.1.1
        USER = admin
        PASSWORD = 1234
        PORT = 23
        CP_normal = 0 
        CP_fixed = 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28
        CP_forbidden = 1,2,3,4
        PC1_vlan = 2
        PC1_normal = 0
        PC1_fixed = 1,2
        PC1_forbidden = 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28
        PC2_vlan = 5
        PC2_normal = 0
        PC2_fixed = 34
        PC2_forbidden = 1,2,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28

        ```
    6. [AP]
        對AP做設定，但目前不會用到
        ```
        HOST = 192.168.50.1
        USER = admin
        PASSWORD = admin123
        PORT = 21
        ```
    7. [Firmware config]
        對fw做設定，無法由此設定，須至fw_config.ini設定
        ```
        Firmware_config = fw_config.bin
        ```

### (二) Source Code - control panel
1. control .py

   主要執行程式，負責設定fw、設定switch、設定 set_netns、初始化所有資料夾、更新所有相關文件的變數值、將要傳送到目標的檔案壓縮、傳送、等Client測試完畢後取回資料、最後呼叫分析程式，並繼續下一組ip的設定與傳送。  
   
   ***若您是一般使用者，除了第一行config_file位址可能需要修改之外，其餘皆不需要進行更動**
    # 定義變數
    會將config.ini中的變數value load到這裡的變數
   ```py =
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
    ```
    # 初始化所有testcase Result資料夾
    ```py =
    testcase_file_num = len([name for name in os.listdir(testcase_path) if os.path.isdir(os.path.join(testcase_path, name))])
    for i in range(testcase_file_num-1):
        i=i+1
        Result_dir = "%s\\testcase\\Result%r" %(sup.config_file(control_config, "Control Panel", "AutoTest_Path"),i)
        shutil.rmtree(Result_dir)
        if not os.path.isdir(Result_dir):
            os.mkdir(Result_dir)
    ```
    # 主程式
    ```py =
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
    fw_bin = sup.config_file(control_config, "Firmware config", "Firmware_config") # 這是待測Fw檔名
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
    sup.switch_portset(HOST,USER,PASSWORD,PORT,'1',CP_normal,CP_fixed,CP_forbidden) # switch 對 CP default 的 vlan 就是 1 
    sup.switch_portset(HOST,USER,PASSWORD,PORT,PC1_vlan,PC1_normal,PC1_fixed,PC1_forbidden)
    sup.switch_portset(HOST,USER,PASSWORD,PORT,PC2_vlan,PC2_normal,PC2_fixed,PC2_forbidden)
    # 把所有寫死的參數全部改成從config抓取變數，包含set_netns.sh(另寫一支子程式呼叫set_netns並修改參數)
    HOST_net0 = sup.config_file(control_config, "Control Panel", "HOST_net0")
    USER_net0 = sup.config_file(control_config, "Control Panel", "USER_net0")
    PASSWORD_net0 = sup.config_file(control_config, "Control Panel", "PASSWORD_net0")
    PORT_net0 = sup.config_file(control_config, "Control Panel", "PORT_net0")
    HOST_net1 = sup.config_file(control_config, "Control Panel", "HOST_net1")
    USER_net1 = sup.config_file(control_config, "Control Panel", "USER_net1")
    PASSWORD_net1 = sup.config_file(control_config, "Control Panel", "PASSWORD_net1")
    PORT_net1 = sup.config_file(control_config, "Control Panel", "PORT_net1")
    
    ### 將檔案壓縮存到特定位址 ###
    sup.zip_dir(zip_dir_srcPath,zip_dir_dstname)
    ### 將壓縮檔案傳送到client並進行指令控制 ###
    sup.paramiko_net0(HOST_net0,USER_net0,PASSWORD_net0,PORT_net0,source_code_local,source_code_client)
    sup.paramiko_net1(HOST_net1,USER_net1,PASSWORD_net1,PORT_net1,source_code_local,source_code_client)
    sup.paramiko_link(HOST_net0,USER_net0,PASSWORD_net0,PORT_net0,main_local,main_client,source_code_local,source_code_client,result_client,result_local,i)
    ### 解壓縮client蒐集到的封包 ###
    sup.unzip_dir("%s\\Result%s.zip" %(sup.config_file(control_config, "Control Panel", "unzip_dir_srcName"),int(i/2)+1),"%s\\Result%s"%(sup.config_file(control_config, "Control Panel", "unzip_dir_dstPath"),int(i/2)+1))
    ```

    # 呼叫分析子程式
    ```py =
    commandText = "python "+'"' + analyze + '"'
    os.system(commandText)
    ```
2. sup .py

   所有API都放在這裡，將此文件與主程式放在同一個資料夾底下，要使用時import sup 即可。  
   以下會一一介紹。
    # 自訂義config parser，這段不用動
    ```py
    class myconf(configparser.ConfigParser):
        def __init__(self,defaults=None):
            configparser.ConfigParser.__init__(self,defaults=None)
        def optionxform(self, optionstr):
            return optionstr
    ```
    # 壓縮
    使用方法 : sup.zip_dir ( 要被壓縮的檔案 , 壓縮檔的路徑 )
   ```py =
    def zip_dir(srcPath,dstname):
        zipHandle=zipfile.ZipFile(dstname,'w',zipfile.ZIP_DEFLATED)
        for dirpath,dirs,files in os.walk(srcPath):
            for filename in files:
                zipHandle.write(os.path.join(dirpath,filename)) #檔名路徑必須完整
                print (filename+" zip succeeded")
        zipHandle.close
    ```
    # 解壓縮 
    使用方法 : sup.unzip_dir ( 要被解壓縮的檔案 , 要解壓縮的路徑 )
   ```py =
    def unzip_dir(srcname,dstPath):
        zipHandle=zipfile.ZipFile(srcname,"r")
        for filename in zipHandle.namelist():
            print (filename)
        zipHandle.extractall(dstPath) #解壓到指定目錄
        zipHandle.close()
   ```
    # 從指定config中取得資料
    使用方法 : sup.config_file ( 設定檔 , 大標題 , 小標題 )
   ```py =
    def config_file(_config_file_, offset1, offset2):
        config = configparser.ConfigParser()
        config.read(_config_file_)
        # 取得設定值
        return(config[offset1][offset2])
   ```
    # 列出所有區段的大標題
    使用方法 : sup.config_file_all_title( 設定檔 )
   ```py =
    def config_file_all_title(_config_file_):
        config = myconf()
        config.read(_config_file_)
        return(config.sections())
   ```
    # 列出指定標題區段下所有設定值
    使用方法 : sup.config_file_all_contents(_設定檔_, 大標題 )
   ```py =
    def config_file_all_contents(_config_file_, _title_):
        config = configparser.ConfigParser()
        config.read(_config_file_)
        i=0
        a={}
        for k in config[_title_]:
            a[i]=("{}: {}".format(k, config[_title_][k]))
            i=i+1
        return a
   ```
    # 將ip_config.ini內容取代control_config.ini  
    使用方法 : sup.alter_ip_to_config( control_config.ini , ip_config.ini , 迴圈數 )
   ```py =
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

   ```
   # 將sw_config.ini內容取代control_config.ini
    使用方法 : sup.alter_sw_to_config(_config_file_, _switch_file_,i)
   ```py
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
    ```
    # 將fw_config.ini內容取代control_config.ini
    使用方法 : sup.alter_fw_to_config(_config_file_, _fw_file_,i)
    ```PY
    config = myconf()
    config.read(_config_file_, encoding="utf-8")
    config['Firmware config']['Firmware_config'] = config_file(_fw_file_, 'fw %s'%i, 'fw')
    config.write(open(_config_file_, "w"))
    ```
    # 直接改變config.ini某欄參數數值  
    使用方法 : sup.alter_parameter_to_config( 設定檔 , 大標題 , 小標題, 要改的數值 )
   ```py =
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
   ```
    # 將config.ini內容取代set_netns_net0.sh  
    使用方法 : sup.alter_config_to_set_netns_net0( 設定檔 , set_netns_net0.sh )
   ```py =
    def alter_config_to_set_netns_net0(_config_file_,_alter_file_):
        def alter(_config_file_, offset1, offset2, _alter_file_, count, field):
            file_data = ""
            f = open(_alter_file_,'r')
            lines = f.readlines()[count]
            old_str = lines.split('=')
            #print ("old_str: "+str(old_str[field]))
            new_str = config_file(_config_file_, offset1, offset2)
            #print ("new_str: "+str(new_str)+"\n")

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
        alter(_config_file_, "Net Namespace Set 1", "NS1_GW_MAC" , _alter_file_, 16, 1)   # NS1_GW_MAC
        alter(_config_file_, "Net Namespace Set 2", "NS2_NAME"   , _alter_file_, 18, 1)    # NS1_NAME    # NS2
        alter(_config_file_, "Net Namespace Set 2", "NS2_VID"    , _alter_file_, 19, 1)    # NS1_VID
        alter(_config_file_, "Net Namespace Set 2", "NS2_BASE_IF", _alter_file_, 20, 1)    # NS1_BASE_IF
        alter(_config_file_, "Net Namespace Set 2", "NS2_IP4"    , _alter_file_, 21, 1)   # NS1_IP4
        alter(_config_file_, "Net Namespace Set 2", "NS2_MASK4"  , _alter_file_, 22, 1)   # NS1_MASK4
        alter(_config_file_, "Net Namespace Set 2", "NS2_GW4"    , _alter_file_, 23, 1)   # NS1_GW4
        alter(_config_file_, "Net Namespace Set 2", "NS2_IP6"    , _alter_file_, 24, 1)   # NS1_IP6
        alter(_config_file_, "Net Namespace Set 2", "NS2_MASK6"  , _alter_file_, 25, 1)   # NS1_MASK6
        alter(_config_file_, "Net Namespace Set 2", "NS2_GW6"    , _alter_file_, 26, 1)   # NS1_GW6
        alter(_config_file_, "Net Namespace Set 2", "NS2_GW_MAC" , _alter_file_, 27, 1)   # NS1_GW_MAC

   ```
    # 將config.ini內容取代set_netns_net1.sh   
    使用方法 : sup.alter_config_to_set_netns_net1( 設定檔 , set_netns_net1.sh )
    ```py =
    def alter_config_to_set_netns_net1(_config_file_,_alter_file_):
        def alter(_config_file_, offset1, offset2, _alter_file_, count, field):
            file_data = ""
            f = open(_alter_file_,'r')
            lines = f.readlines()[count]
            old_str = lines.split('=')
            #print ("old_str: "+str(old_str[field]))
            new_str = config_file(_config_file_, offset1, offset2)
            #print ("new_str: "+str(new_str)+"\n")

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
        alter(_config_file_, "Net Namespace Set 1", "NS1_GW_MAC" , _alter_file_, 16, 1)   # NS1_GW_MAC
        alter(_config_file_, "Net Namespace Set 2", "NS2_NAME"   , _alter_file_, 18, 1)    # NS1_NAME    # NS2
        alter(_config_file_, "Net Namespace Set 2", "NS2_VID"    , _alter_file_, 19, 1)    # NS1_VID
        alter(_config_file_, "Net Namespace Set 2", "NS2_BASE_IF", _alter_file_, 20, 1)    # NS1_BASE_IF
        alter(_config_file_, "Net Namespace Set 2", "NS2_IP4"    , _alter_file_, 21, 1)   # NS1_IP4
        alter(_config_file_, "Net Namespace Set 2", "NS2_MASK4"  , _alter_file_, 22, 1)   # NS1_MASK4
        alter(_config_file_, "Net Namespace Set 2", "NS2_GW4"    , _alter_file_, 23, 1)   # NS1_GW4
        alter(_config_file_, "Net Namespace Set 2", "NS2_IP6"    , _alter_file_, 24, 1)   # NS1_IP6
        alter(_config_file_, "Net Namespace Set 2", "NS2_MASK6"  , _alter_file_, 25, 1)   # NS1_MASK6
        alter(_config_file_, "Net Namespace Set 2", "NS2_GW6"    , _alter_file_, 26, 1)   # NS1_GW6
        alter(_config_file_, "Net Namespace Set 2", "NS2_GW_MAC" , _alter_file_, 27, 1)   # NS1_GW_MAC

   ```
    # 替換功能  
    使用方法 : sup.alter( 要改的檔案 , 行數 , 列數 , 設定檔 , 大標題 , 小標題)
   ```py =
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

   ```
    # 用cle燒fw
    使用方法 : sup.cle_set(cle, fw):
    ```py
    cmd = '''D: & \
    cd %s & \
    cle.exe spi erase all & \
    cle.exe spi update %s & \
    ''' %(cle,fw)
    if fw != '':
        os.system(cmd)
    ```
    # 透過ssh傳送PC1的設定腳本到目標機器並自動執行設定 (目標限定Linux環境) 
    使用方法 : sup.paramiko_net0(HOST,USER,PASSWORD,PORT,本地檔案位址,目標檔案位址)
   ```py =
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

   ```
    # 透過ssh傳送PC2的設定腳本到目標機器並自動執行設定 (目標限定Linux環境) 
    使用方法 : sup.paramiko_net1(HOST,USER,PASSWORD,PORT,本地檔案位址,目標檔案位址)
   ```py =
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
        sudo rm set_netns.sh error.txt RaspberryPi.zip
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
    
   ```
    # 透過ssh傳送主程式到目標機器並自動執行 (目標限定Linux環境)  
    使用方法 : sup.paramiko_link(HOST,USER,PASSWORD,PORT,本地端 main.sh 路徑 , 客戶端 main.sh 路徑 ,本地程式路徑,客戶端程式路徑,客戶端結果存放路徑,本地結果存放路徑,loop次數)
   ```py =
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
   ```
    # 非待測 switch 設定  
    使用方法 : sup.switch_set(HOST,USER,PASSWORD,PORT)
   ```py =
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

   ```
    # 將ip list內容以空白為分隔方式儲存  
    使用方法 : sup.ip_field( ip_list設定檔位址 , 行數, 欄位)
   ```py =
    def ip_field(_ip_list_file_, count, field):
        f = open(_ip_list_file_,'r')
        lines = f.readlines()[count]
        str = lines.split(' ')
        return str[field]

   ```
    # 移動檔案的功能  
    使用方法 : sup.movefile(檔案原始位置,檔案目標位址)
   ```py =
    def movefile(srcfile,dstfile):
        if not os.path.isfile(srcfile):
            print ("%s not exist!" %srcfile)
        else:
            fpath=os.path.split(dstfile)    #分离文件名和路径
            if not os.path.exists(fpath):
                os.makedirs(fpath)                #创建路径
            shutil.move(srcfile,dstfile)          #移动文件
            print ("move %s -> %s" %srcfile,dstfile)

   ```
    # 複製檔案的功能  
    使用方法 : sup.copyfile(原始檔案,目標位址)
   ```py =
    def copyfile(srcfile,dstfile):
        if not os.path.isfile(srcfile):
            print ("%s not exist!" %srcfile)
        else:
            fpath=os.path.split(dstfile)    #分离文件名和路径
            if not os.path.exists(fpath):
                os.makedirs(fpath)                #创建路径
            shutil.copyfile(srcfile,dstfile)      #复制文件
            print ("copy %s -> %s" %(srcfile,dstfile))

   ```
    # 自設定要顯示的欄位及長度  
    使用方法 : sup.field_define( 讀取檔案 , 字元數, 長度, 模式 1是回傳bit段落 0是關閉文件)
   ```py =
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

   ```
    # 將ipv4 address變成10進位  
    使用方法 : sup.ip_addr(2進位的ipv4位址)
    ```py =
    def ip_addr(ip):
        IP_1 = ip[0]+ip[1]; IP_2 = ip[2]+ip[3]; IP_3 = ip[4]+ip[5]; IP_4 = ip[6]+ip[7]
        IP = f"{int(IP_1, 16)}.{int(IP_2, 16)}.{int(IP_3, 16)}.{int(IP_4, 16)}"
        return IP

    ```
    # 判斷路徑資料夾下有多少檔案(不含資料夾)  
    使用方法 : sup.file_num(資料夾位址)
   ```py =
    def file_num(path):
        num_files = len([f for f in os.listdir(path)
                        if os.path.isfile(os.path.join(path, f))])
        return num_files

   ```
    # 判斷任意Seqence Number是否重複出現  
    使用方法 : sup.seq_num_pair(放置SeqNum.txt的位址,Pair.txt的位址)
   ```py =
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
            if (pair == 2):
                with open(pair_file, 'a') as fs:                   
                    fs.write (seq_num+"\n")

   ```
    # 將文件中的重複字串刪除  
    使用方法 : sup.uniq(放置Pair.txt.txt的位址,Result.txt的位址)
   ```py =
    def uniq(src_path,dst_path):
        if os.path.exists("tmp.txt"): # 先刪掉暫存檔
            if os.path.isfile("tmp.txt"):
                os.remove("tmp.txt")
        with open(src_path, 'a') as fr:
            print("", file=fr)
        with open(src_path, 'r') as fr:    # 打開需要處理的檔案和放入重新整理資料的檔案
            with open("tmp.txt", 'w') as fw:
                # 刪除重複的
                print (''.join(list(set([i for i in fr]))), file = fw)
                print("", file = fw)
        with open("tmp.txt", "r") as f:
            data = f.readlines()
            data.sort()
            for i in range(len(data)):
                with open(dst_path, "a") as f:
                    if data[i].split():               
                        print (data[i].split("\n")[0], file = f)
                    else:
                        print ("", end='', file = f)
        f1 = open(src_path, 'r')
        f2 = open("tmp3.txt", 'w')
        lines = f1.readlines()
        for line in lines:
            line = line.strip()
            if line.split():
                f2.writelines(line+"\n")
            else:
                f2.writelines("")
        f1 = open(src_path, 'w')
        f2 = open("tmp3.txt", 'r')
        lines = f2.readlines()
        for line in lines:
            line = line.strip()
            if line.split():
                f1.writelines(line+"\n")
            else:
                f1.writelines("")
 
    ```
    # 移除不會自動覆蓋內容內容的文件，如不存在文件也不會跳錯誤通知
    使用方法 : sup.remove_old_file(檔案位址)
    ```py =
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)
    else:
        print("", end='')


    ```
    # 回傳有多少%是loss的  
    使用方法 : sup.loss_ratio(seq_num_file, pair_file)
    ```py =
    with open(seq_num_file, "r") as f:
        seq_num = f.readlines()
    with open(result_file, "r") as f:
        pair_num = f.readlines()
    ratio = (len(pair_num)*2)/len(seq_num)
    return str(ratio*100)+'%'


    ```
    # 判斷是否為連續數字  
    使用方法 : sup.continuous_number(Result.txt)
    ```py =
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
                        if loss_next - loss_first != 1: # 每行都跟上一行相減，若差值不是1表示非連續
                            for j in range(loss_first+1,loss_next):
                                print ("Loss "+hex(j))               # 列出loss的部分
                                loss = loss+1                # loss的記數 + 1
                                # 這裡可以放置其他要對loss的內容作的處置
                if loss == 0:
                    a="No loss."
                    return a
                else:
                    a="loss"
                    return a
   ```
    # 設定switch  
    使用方法 : sup.switch_portset(HOST,USER,PASSWORD,PORT,'1',要設定成normal的port,要設定成fixed的port,要設定成forbidden的port)
    ```py =
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
    ```
#
3. packet_analyze .py  
   將傳送回本地的封包進行分析並顯示測試結果。
    # 定義路徑
    ```py =
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
    ```
    # 寫入最終結果的文件
    ```py
    result_file = "%s\\Final.txt"%(output)
    sup.remove_old_file(result_file)
    ```
    # 初始化所有資料夾
    ```py =
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
    ```
    # 取得新測資並清除舊文件
    ``` py =
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

        Network_Layer_Type = 0
    ```
    # 對同一包Result下的所有packet分析
    ```py =
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
                        fw.write ("Network Layer Type: "+Network_Layer_Type+" ("+Network_Layer_Type+")"+"\n")
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
                        fw.write ("Network Layer Type: "+Network_Layer_Type+" ("+Network_Layer_Type+")"+"\n")
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
     
    ```
    # 將所有封包整理輸出最後結果
    最後的output可在testcase>output>(封包類型)>Result(index)>output(index).txt中  
    若是analyze.py判斷封包皆無損失，則會在terminal顯示No loss.
    ``` py =
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
    ```
#
### (三) Source Code - Client
基本上不用改動，除非想要新增自己寫的打封包程式，這可能會需要更動部份其他程式架構
1. set_netns_net0.sh : PC1環境設定
2. set_netns_net1.sh : PC2環境設定
3. set_netns.sh : 提供給main.sh抓取資料，不分PC1或2
4. main .sh : 主要執行程式
5. packet_transfer.sh : 呼叫打封包程式
6. packet_capture.sh : 抓取封包
7. packet_offset.sh : 將封包處理成可供分析用
8. packet_transfer_programs   
   (1) icmp.sh : 在背景打ICMP封包
   (2) icmpv6.sh : 在背景打ICMPv6封包
   (3) tcp.sh : 在背景打TCP封包
9. txt  
   test_program.txt : 存放packet_transfer.sh要呼叫的打封包程式

### (四) tastcase
放置所有封包資料與回傳結果的地方，Result1~10表示10輪測試，若少於10輪則不影響，多於則需手動增加資料夾數量  
output資料夾存放經分析後的Result，依照封包類型分裝，其中outputxx為每包封包解析後的結果，SeqNum.txt為每個封包的編號，Pair.txt是過渡文件，Result.txt為有成對的編號，即表示request有收到reply
所有測試結果pass ornot以及它們的成功率都放在output資料夾最外側的Final.txt

### (五) RTKAutoSwitchTool_HCP5_VA_2.1.6.20.0
生產fw的工具，用法如下
打開RTKAutoSwitchTool_HCP5_VA_2.1.6.20.0.exe
選9075AVA
Make image mode
switch
import image file (此步驟為將fw和config結合成fw_config.bin)
選取要燒錄的json
Make image file
選Firmware/v4.94
OK
Binary file success
此時外頭的fw_config.bin會被更新
複製後丟到cle資料夾中
記得結束後重開switch

### (六) final_cle_210720
將 fw 燒進 DUT switch 的工具，用法為把switch tool做好的fw_config.bin丟到folder底下取代掉，接著spi erase all把flash清光，然後spi update fw_config.bin

### (七) Document
放置各種文件
