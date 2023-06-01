import sys,subprocess,re,requests,time,json,configparser,os,traceback,hmac,hashlib,urllib,base64
from datetime import datetime

############################################################从配置文件中读取信息############################################################
file    = os.path.join(os.path.dirname(__file__), '/root/tools/config.ini')
con     = configparser.ConfigParser() # 创建配置文件对象
con.read(file, encoding='utf-8') # 读取文件

root_path                         =    str(con.get('DependencyToolConfigInfo', 'root_path'))
codeqlJavaFilesPath               =    str(con.get('DependencyToolConfigInfo', 'codeqlJavaFilesPath'))
codeqlJSFilesPath                 =    str(con.get('DependencyToolConfigInfo', 'codeqlJSFilesPath'))
codeqlcppFilesPath                =    str(con.get('DependencyToolConfigInfo', 'codeqlcppFilesPath'))
trivyFilesPath                    =    str(con.get('DependencyToolConfigInfo', 'trivyFilesPath'))
mavenDir                          =    str(con.get('DependencyToolConfigInfo', 'mavenDir'))
mavenSettingsFile                 =    str(con.get('DependencyToolConfigInfo', 'mavenSettingsFile'))
mavenLocalRepositoryDir           =    str(con.get('DependencyToolConfigInfo', 'mavenLocalRepositoryDir'))
delombokJarFilePath               =    str(con.get('DependencyToolConfigInfo', 'delombokJarFilePath'))
codeqlBinPath                     =    str(con.get('DependencyToolConfigInfo', 'codeqlBinPath'))
javaHome                          =    str(con.get('DependencyToolConfigInfo', 'javaHome'))
javaEnvSetting                    =    str(con.get('DependencyToolConfigInfo', 'javaEnvSetting'))
codeqlDBCreateSuccFlagList        =     con.get('DependencyToolConfigInfo', 'codeqlDBCreateSuccFlagList').split(",")
isAtAll                           = str(con.get('DingdingConfigInfo', 'isAtAll'))
atPersons                         =     con.get('DingdingConfigInfo', 'atPersons').split(",")


###################################工具集###################################

def isCodeqlDBCreateSucc(codeqlDBPath):
    global codeqlDBCreateSuccFlagList
    isSuccess = False
    items = os.listdir(codeqlDBPath) # 获取文件夹中的所有内容
    index = 0
    for target in codeqlDBCreateSuccFlagList:
        if target in items:
            index+=1
            print(index)
    if (index==len(codeqlDBCreateSuccFlagList)):
        isSuccess =True
    return isSuccess

def getCurrentTime():
    now = datetime.now() # 获取当前时间
    format = "%Y-%m-%d" # 定义格式字符串
    time_str = now.strftime(format) # 格式化时间字符串
    return time_str

def getCodeRespName(string):
    pattern = r"/([a-zA-Z-_0-9]+)\.git" # 定义正则表达式模式
    match = re.search(pattern, string) # 使用search方法查找匹配
    if match: # 如果找到匹配
        return match.group().replace(".git","").replace("/","")
    else: # 如果没有找到匹配
        pass

def Signature_Url():
    global file,con
    webhook_url             = str(con.get('DingdingConfigInfo', 'webhook_url')) 
    dingdingSecret          = str(con.get('DingdingConfigInfo', 'secret'))  
    try:
        timestamp = str(round(time.time() * 1000))
        secret_enc = dingdingSecret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, dingdingSecret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        Post_Url = ("%s&timestamp=%s&sign=%s" % (webhook_url, timestamp, sign))
        return Post_Url
    except Exception as e:
        traceback.print_exc()
        pass
# 发送消息
def sendDingMessage(Content,isAtAll,atPersons):
    Post_Url=Signature_Url()
    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    # 构建请求数据
    message ={
        "msgtype": "text",
        "text": {
            "content": Content
        },
        "at": {
            "atMobiles":atPersons,
            "isAtAll": isAtAll
        }
    }
    try:
        info = requests.post(url=Post_Url,data=json.dumps(message),headers=header)
        if json.loads(info.text)['errmsg'] == "ok":
            pass
        else:
            print(json.loads(info.text))
    except Exception as e:
        traceback.print_exc()
        time.sleep(3600)
        msg="Code Scan Monitor机器人挂掉了，先睡眠1小时，如果一小时你依旧看到这条消息，请手工检查一下～"
        sendDingMessage(msg,isAtAll,atPersons)
        pass


inputParameter1 = str(sys.argv[1])
inputParameter2 = str(sys.argv[2])

finalCMD                        = ""
projectRootPath                 = str(root_path) + str(getCodeRespName(inputParameter1))
replaceFileContenCmd            = "find . -maxdepth 1 -type f -name '*.txt' -exec sed -i '' 's#path##g' {} \;".replace("path",root_path)
DependencyCheckOutputName       = str(getCurrentTime())+"_"+str(getCodeRespName(inputParameter1))+"_DependencyCheck扫描结果.html"
DependencyCheckCmd              = "sudo dependency-check.sh --project 'myproject' -s  scanPath   -n  --out outPutname".replace("myproject",getCodeRespName(inputParameter1)).replace("outPutname",DependencyCheckOutputName).replace("scanPath",projectRootPath)+";"
gitCloneCmd                     =  "cd " + str(root_path) + ";"+ inputParameter1 +";"
codeqlOutName                   =  ""
###################################工具集###################################
if inputParameter2 == "java":
    lombokCommands          = ['javaHome -jar delombokJarFilePath delombok -n --onlyChanged . -d "delombok"'.replace("javaHome",javaHome).replace("delombokJarFilePath",delombokJarFilePath),'find "delombok" -name \'*.java\' -exec sed \'/Generated by delombok/d\' -i \'{}\' \';\'','find "delombok" -name \'*.java\' -exec sed \'/import lombok/d\' -i \'{}\' \';\'','cp -r "delombok/." "./"','rm -rf "delombok"']
    lombokCommands          = " ; ".join(lombokCommands)
    cmd                     = inputParameter1 # 获取第一个参数
    codeqlOutName           = str(getCurrentTime())+"_"+str(getCodeRespName(cmd))+"_codeql扫描结果.txt"
    cdToRootCmd             = "cd " + str(root_path) + str(getCodeRespName(cmd)) + ";"
    lombokCmd               = cdToRootCmd   +   lombokCommands   + ";"
    codeqlCreateCmd         = "javaEnvSetting  ;codeqlBinPath database create codeqldatabase --language=java --command='mavenDir/bin/mvn    -gs mavenSettingsFile  clean install   -Dmaven.test.skip -Dmaven.repo.local=mavenLocalRepositoryDir' --overwrite".replace("mavenSettingsFile",mavenSettingsFile).replace("mavenLocalRepositoryDir",mavenLocalRepositoryDir).replace("codeqlBinPath",codeqlBinPath).replace("mavenDir",mavenDir)+";"
    codeqlScanCmd           = "for file in codeqlJavaFilesPath*.ql; do sudo codeqlBinPath query run --database=codeqldatabase \"$file\">>codeqlOutName; done".replace("codeqlOutName",codeqlOutName).replace("codeqlJavaFilesPath",codeqlJavaFilesPath).replace("codeqlBinPath",codeqlBinPath)+";"
    finalCMD                = (lombokCmd+codeqlCreateCmd+codeqlScanCmd)

elif inputParameter2 == "js" or inputParameter2 == "javascript":
    cmd                     = inputParameter1 # 获取第一个参数
    codeqlOutName           = str(getCurrentTime())+"_"+str(getCodeRespName(cmd))+"_codeql扫描结果.txt"
    cdToRootCmd             = "cd " + str(root_path) + str(getCodeRespName(cmd)) + ";"
    codeqlCreateCmd         = cdToRootCmd  + "codeqlBinPath database create codeqldatabase --language=javascript  --overwrite".replace("codeqlBinPath",codeqlBinPath)+";"
    codeqlScanCmd           = "for file in codeqlJSFilesPath*.ql; do sudo codeqlBinPath query run --database=codeqldatabase \"$file\">>codeqlOutName; done".replace("codeqlOutName",codeqlOutName).replace("codeqlJSFilesPath",codeqlJSFilesPath).replace("codeqlBinPath",codeqlBinPath)+";"
    finalCMD                = (codeqlCreateCmd+codeqlScanCmd)

elif inputParameter2 == "c" or inputParameter2 == "cpp" or inputParameter2 == "c++" :
    cmd                     = inputParameter1 # 获取第一个参数
    codeqlOutName           = str(getCurrentTime())+"_"+str(getCodeRespName(cmd))+"_codeql扫描结果.txt"
    cdToRootCmd             = "cd " + str(root_path) + str(getCodeRespName(cmd)) + ";"
    codeqlCreateCmd         = cdToRootCmd  + "codeqlBinPath database create codeqldatabase --language=cpp  --command='bash /root/code/build.sh'   --overwrite".replace("codeqlBinPath",codeqlBinPath)+";"
    codeqlScanCmd           = "for file in codeqlcppFilesPath*.ql; do sudo codeqlBinPath query run --database=codeqldatabase \"$file\">>codeqlOutName; done".replace("codeqlOutName",codeqlOutName).replace("codeqlcppFilesPath",codeqlcppFilesPath).replace("codeqlBinPath",codeqlBinPath)+";"
    finalCMD                = (codeqlCreateCmd+codeqlScanCmd)
   

msg="++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++运行下面命令：++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\nfinaCMD \n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++运行上面面命令：++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"

trivyOutPutFilename         =  str(getCurrentTime())+"_"+str(getCodeRespName(inputParameter1))+"_trivy扫描结果.txt"
trivyCmd                    =  " "+trivyFilesPath + "trivy fs " + projectRootPath + " --offline-scan   -o " + trivyOutPutFilename + ";"
codeqlDatabasePath          =  root_path + "/" + str(getCurrentTime())+"_"+str(getCodeRespName(inputParameter1))+"_codeqldatabase"
mvCodeqlDatabaseDirCmd1     =  "mv " + projectRootPath + "/codeqldatabase " + codeqlDatabasePath+";"
mvCodeqlDatabaseDirCmd2     =  "mv " + codeqlDatabasePath + " " + root_path +str(getCodeRespName(inputParameter1)) +"/"+ str(getCurrentTime())+"_"+str(getCodeRespName(inputParameter1))+"_codeqldatabase;"
finalCMD                    =  (gitCloneCmd+finalCMD+mvCodeqlDatabaseDirCmd1 + trivyCmd + mvCodeqlDatabaseDirCmd2 + replaceFileContenCmd).replace("javaEnvSetting",javaEnvSetting)
# finalCMD                    =  gitCloneCmd + "sudo bash -c '''" + finalCMD + "'''"
msg                         =  msg.replace("finaCMD",finalCMD)
print(msg)
startTime                   = time.time()
returned_value              = subprocess.call(finalCMD, shell=True) # 返回退出码
print('returned value:', returned_value)
endTime                     = time.time()
totalTime                   =  str((endTime-startTime)/60) + "min"
trivyOutPutFilePath         = root_path + str(getCodeRespName(inputParameter1)) + "/"+trivyOutPutFilename
codeqlOutFilePath           = root_path + str(getCodeRespName(inputParameter1)) + "/"+codeqlOutName
scanResultPath              = trivyOutPutFilePath + "\n" + codeqlOutFilePath
if isCodeqlDBCreateSucc(codeqlDatabasePath):
    msg                         = "[扫描项目]:getCodeRespName\n[扫描状态]:✅\n[扫描耗时]:".replace("getCodeRespName",str(getCodeRespName(inputParameter1))) +totalTime + "\n[扫描结果]: \nscanResultPath".replace("scanResultPath",scanResultPath)
else:
    msg                         = "[扫描项目]:getCodeRespName\n[扫描状态]:❌\n[失败原因]:codeql数据库创建失败!\n[扫描耗时]:".replace("getCodeRespName",str(getCodeRespName(inputParameter1))) +totalTime + "\n[扫描结果]: \nscanResultPath".replace("scanResultPath",scanResultPath)
sendDingMessage(msg,isAtAll,atPersons)