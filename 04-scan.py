import sys,subprocess,re,requests,time,json,configparser,os,traceback,hmac,hashlib,urllib,base64,os.path
from datetime import datetime

############################################################从配置文件中读取信息############################################################
file    = os.path.join(os.path.dirname(__file__), '/root/tools/config.ini')
con     = configparser.ConfigParser() # 创建配置文件对象
con.read(file, encoding='utf-8') # 读取文件

root_path                         =    str(con.get('DependencyToolConfigInfo', 'root_path'))
scanResFileNamePath               =    root_path + "/" + "scanRes.txt"
codeqlJavaFilesPath               =    str(con.get('DependencyToolConfigInfo', 'codeqlJavaFilesPath'))
codeqlJSFilesPath                 =    str(con.get('DependencyToolConfigInfo', 'codeqlJSFilesPath'))
codeqlcppFilesPath                =    str(con.get('DependencyToolConfigInfo', 'codeqlcppFilesPath'))
trivyFilesPath                    =    str(con.get('DependencyToolConfigInfo', 'trivyFilesPath'))
codeqlConfigPath                  =    str(con.get('DependencyToolConfigInfo', 'codeqlConfigPath'))
mavenDir                          =    str(con.get('DependencyToolConfigInfo', 'mavenDir'))
mavenSettingsFile                 =    str(con.get('DependencyToolConfigInfo', 'mavenSettingsFile'))
mavenLocalRepositoryDir           =    str(con.get('DependencyToolConfigInfo', 'mavenLocalRepositoryDir'))
delombokJarFilePath               =    str(con.get('DependencyToolConfigInfo', 'delombokJarFilePath'))
codeqlBinPath                     =    str(con.get('DependencyToolConfigInfo', 'codeqlBinPath'))
javaHome                          =    str(con.get('DependencyToolConfigInfo', 'javaHome'))
javaHomeDir                       =    javaHome.replace("bin/java","")
javaEnvSetting                    =    "export JAVA_HOME=javaHomeDir;export PATH=$JAVA_HOME/bin:$PATH;export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar".replace("javaHomeDir",javaHomeDir)
findFileExtensionList             =     con.get('DependencyToolConfigInfo', 'findFileExtension').split(",")
findKeywordsList                  =     con.get('DependencyToolConfigInfo', 'findKeywords').split(",")
findCommand                       =     str(con.get('DependencyToolConfigInfo', 'findCommand'))
codeqlDBCreateSuccFlagList        =     con.get('DependencyToolConfigInfo', 'codeqlDBCreateSuccFlagList').split(",")
isAtAll                           = str(con.get('DingdingConfigInfo', 'isAtAll'))
atPersons                         =     con.get('DingdingConfigInfo', 'atPersons').split(",")


###################################工具集###################################

def writeContent2File(content,filePath):
    # 以读模式打开文件
    with open(str(filePath), 'a') as f:
        f.write(str(content)+"\n")

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

def getGitCommandList(gitCommand): 
    gitCommand       =  gitCommand.split(" ")
    gitCommand       = [x for x in gitCommand if x != '']
    return gitCommand

def getCodeRespName(string):
    if " -b " in string:
        string = re.sub(r"\s+", " ", string)
        # print(string.split(" "))
        string = string.split(" ")[2]
        
    if ":" in string:
        tempList    = string.split("/")
        projectName = tempList[len(tempList)-1].replace(".git","")
        return projectName 

    else:
        tempStr     = re.sub(r"\s+", " ", string)
        tempStr     = tempStr.split(" ")[0]
        tempStr     = re.sub(r"/+", "/", tempStr)
        tempList    = tempStr.split("/")
        projectName = tempList[len(tempList)-1]
        return projectName

def excuteFindCommandRes2File(projectPath,findResOutputFilePath):
    global findFileExtensionList,findKeywordsList,findCommand
    for findFileExtension in findFileExtensionList:
        for findKeywords in findKeywordsList:
            echoCommand = "echo  '[-] Try to find Keywords: findKeywords in *.findFileExtension files of Projetc: projectPath' >>findResOutputFilePath".replace("findKeywords",findKeywords).replace("findFileExtension",findFileExtension).replace("projectPath",projectPath).replace("findResOutputFilePath",findResOutputFilePath)
            tempFindCommand = findCommand.replace("findFileExtension",findFileExtension).replace("findKeywords",findKeywords).replace("findResOutputFilePath",findResOutputFilePath).replace("projectPath",projectPath)
            print("[+] excute command "+ echoCommand)
            subprocess.call(echoCommand, shell=True) # 返回退出码
            print("[+] excute command "+ tempFindCommand)
            subprocess.call(tempFindCommand, shell=True) # 返回退出码

def getBranchName(gitCommand):
    branchName = "main"
    if " -b " in gitCommand:
        if ":" in gitCommand:
            tempStr = re.sub(r"\s+", " ", gitCommand)
            # print(tempStr.split(" "))
            if "phabricator" in gitCommand:
                branchName = tempStr.split(" ")[4].replace("/","%252F")
            else:
                branchName = tempStr.split(" ")[4]
        elif os.path.isabs(str(gitCommand).replace(" ","")):
            # print(string)
            if " -b " in str(gitCommand):
                tempStr     = re.sub(r"\s+", " ", gitCommand)
                branchName  =tempStr.split(" ")[2]

    else:
        if "gitlab" in gitCommand:
            branchName             =   "main"
        elif "phabricator" in gitCommand:
            branchName             =   "master"
        elif "github" in gitCommand:
            branchName             =   "main"  
    return branchName   




def getReplaceCommand(gitCommand,projectRootPath):
    gitCommandStr    = str(gitCommand)
    gitCommand       = getGitCommandList(gitCommand)

    replaceCommand   = "find . -maxdepth 1 -type f -name '*.txt' -exec sed -i '' -e 's#projectRootPath#repositoryAddress#g' -e 's#\$\$#repositoryType#g' {} \;"
    branchName       = getBranchName(gitCommandStr)

    if "gitlab" in gitCommandStr:
        if "git@gitlab" in gitCommandStr:
            repositoryAddress   =   gitCommand[2].replace("git@","https://").replace(":","/").replace(".git","")+ "/-/blob/" + str(branchName) + "/"
            repositoryAddress   =   repositoryAddress.replace("///","://")
        elif "https://gitlab" in gitCommandStr:
            repositoryAddress   =   gitCommand[2].replace(".git","") + "/-/blob/" + str(branchName)  +"/"
        
        replaceCommand          =   replaceCommand.replace("projectRootPath",projectRootPath).replace("repositoryAddress",repositoryAddress).replace("repositoryType","\#L")
        
    elif "github" in gitCommandStr:
        if "https://github" in gitCommandStr:
            repositoryAddress   =   gitCommand[2].replace(".git","") + "/tree/" + str(branchName)  +"/"
        elif "git@github" in gitCommandStr:
            repositoryAddress   =   gitCommand[2].replace(":","/").replace("git@","https://").replace(":","/").replace(".git","")+ "/tree/" + str(branchName) + "/"
            repositoryAddress   =   repositoryAddress.replace("///","://")

        replaceCommand          =   replaceCommand.replace("projectRootPath",projectRootPath).replace("repositoryAddress",repositoryAddress).replace("repositoryType","\#L")


    elif "phabricator" in gitCommandStr:
        repositoryAddress   = gitCommand[2].replace("ssh://git@","https://")
        repositoryAddress   = re.sub(r"/(\d+)/.*", r"/\1/replaceFlag", repositoryAddress)
        repositoryAddress   = repositoryAddress.replace("replaceFlag","/browse/" + str(branchName) + "/")

        replaceCommand        =replaceCommand.replace("projectRootPath",projectRootPath).replace("repositoryAddress",repositoryAddress).replace("repositoryType","\$")
    
    return replaceCommand


try:
    inputParameter3  = str(sys.argv[3])#决定是否要进行codeql扫描,默认进行codeql扫描
except Exception as e:
    traceback.print_exc()
    inputParameter3  = ""
    pass


    
try:
    startTime                   = time.time()
    inputParameter1 = str(sys.argv[1])
    inputParameter2 = str(sys.argv[2])

    finalCMD                        = ""
    projectRootPath                 = str(root_path) + str(getCodeRespName(inputParameter1)) + "/"
    replaceFileContenCmd            =   "cd " + projectRootPath +";"+ getReplaceCommand(inputParameter1,projectRootPath)
    DependencyCheckOutputName       = str(getCurrentTime())+"_"+str(getCodeRespName(inputParameter1))+"_"+getBranchName(str(inputParameter1)).replace("/","%252F")+"_DependencyCheck扫描结果.html"
    DependencyCheckCmd              = "sudo dependency-check.sh --project 'myproject' -s  scanPath   -n  --out outPutname".replace("myproject",getCodeRespName(inputParameter1)).replace("outPutname",DependencyCheckOutputName).replace("scanPath",projectRootPath)+";"
    gitCloneCmd                     =  "cd " + str(root_path) + "; sudo  rm -rf "+ str(getCodeRespName(inputParameter1)) + ";"+inputParameter1 +";"
    codeqlOutName                   = str(getCurrentTime())+"_"+str(getCodeRespName(inputParameter1))+"_"+getBranchName(str(inputParameter1)).replace("/","%252F")+"_codeql扫描结果.txt"
    codeqlScanCmd                   = ""
    ###################################工具集###################################
    if inputParameter2 == "java":
        lombokCommands          = ['javaHome -jar delombokJarFilePath delombok -n --onlyChanged . -d "delombok"'.replace("javaHome",javaHome).replace("delombokJarFilePath",delombokJarFilePath),'find "delombok" -name \'*.java\' -exec sed \'/Generated by delombok/d\' -i \'{}\' \';\'','find "delombok" -name \'*.java\' -exec sed \'/import lombok/d\' -i \'{}\' \';\'','cp -r "delombok/." "./"','rm -rf "delombok"']
        lombokCommands          = " ; ".join(lombokCommands)
        cmd                     = inputParameter1 # 获取第一个参数
        cdToRootCmd             = "cd " + str(root_path) + str(getCodeRespName(cmd)) + ";"
        lombokCmd               = lombokCommands   + ";"
        lombokCmd               = "" # 官方已经支持lombok，所以这里的命令设置为空
        codeqlCreateCmd         = "javaEnvSetting  ;codeqlBinPath database create codeqldatabase --language=java --command='mavenDir/bin/mvn    -gs mavenSettingsFile  clean install   -Dmaven.test.skip -Dmaven.repo.local=mavenLocalRepositoryDir' --overwrite  --codescanning-config=codeqlConfigPath".replace("codeqlConfigPath",codeqlConfigPath).replace("mavenSettingsFile",mavenSettingsFile).replace("mavenLocalRepositoryDir",mavenLocalRepositoryDir).replace("codeqlBinPath",codeqlBinPath).replace("mavenDir",mavenDir)+";"
        codeqlScanCmd           = "for file in codeqlJavaFilesPath*.ql; do sudo codeqlBinPath query run --database=codeqldatabase \"$file\">>codeqlOutName; done".replace("codeqlOutName",codeqlOutName).replace("codeqlJavaFilesPath",codeqlJavaFilesPath).replace("codeqlBinPath",codeqlBinPath)+";"
        codeqlFinalCMD          = (cdToRootCmd + lombokCmd+codeqlCreateCmd+codeqlScanCmd)

    elif inputParameter2 == "js" or inputParameter2 == "javascript":
        cmd                     = inputParameter1 # 获取第一个参数
        cdToRootCmd             = "cd " + str(root_path) + str(getCodeRespName(cmd)) + ";"
        codeqlCreateCmd         = cdToRootCmd  + "codeqlBinPath database create codeqldatabase --language=javascript  --overwrite  --codescanning-config=codeqlConfigPath".replace("codeqlConfigPath",codeqlConfigPath).replace("codeqlBinPath",codeqlBinPath)+";"
        codeqlCreateCmd         = codeqlCreateCmd.replace("codeql-v2.14.5","codeql-v2.13.1") # codeql-v2.13.1版本创建js有问题，暂时使用2.13.1来创建js
        codeqlScanCmd           = "for file in codeqlJSFilesPath*.ql; do sudo codeqlBinPath query run --database=codeqldatabase \"$file\">>codeqlOutName; done".replace("codeqlOutName",codeqlOutName).replace("codeqlJSFilesPath",codeqlJSFilesPath).replace("codeqlBinPath",codeqlBinPath)+";"
        codeqlFinalCMD          = (codeqlCreateCmd+codeqlScanCmd)

    elif inputParameter2 == "c" or inputParameter2 == "cpp" or inputParameter2 == "c++" :
        cmd                     = inputParameter1 # 获取第一个参数
        cdToRootCmd             = "cd " + str(root_path) + str(getCodeRespName(cmd)) + ";"
        codeqlCreateCmd         = cdToRootCmd  + "codeqlBinPath database create codeqldatabase --language=cpp  --command='bash /root/tools/build.sh'   --overwrite  --codescanning-config=codeqlConfigPath".replace("codeqlConfigPath",codeqlConfigPath).replace("codeqlBinPath",codeqlBinPath)+";"
        codeqlScanCmd           = "for file in codeqlcppFilesPath*.ql; do sudo codeqlBinPath query run --database=codeqldatabase \"$file\">>codeqlOutName; done".replace("codeqlOutName",codeqlOutName).replace("codeqlcppFilesPath",codeqlcppFilesPath).replace("codeqlBinPath",codeqlBinPath)+";"
        codeqlFinalCMD          = (codeqlCreateCmd+codeqlScanCmd)
    

    msg="++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++运行下面命令：++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\nfinaCMD \n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++运行上面面命令：++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"

    trivyOutPutFilename         =  str(getCurrentTime())+"_"+str(getCodeRespName(inputParameter1))+"_"+ getBranchName(str(inputParameter1)).replace("/","%252F") +"_trivy扫描结果.txt"
    trivyOutPutFilePath         = root_path + str(getCodeRespName(inputParameter1)) + "/"+trivyOutPutFilename
    trivyCmd                    =  " "+trivyFilesPath  + " " + projectRootPath + " -o " + trivyOutPutFilePath + ";"
    codeqlDatabasePath          =  root_path + "/" + str(getCurrentTime())+"_"+str(getCodeRespName(inputParameter1))+"_codeqldatabase"
    mvCodeqlDatabaseDirCmd1     =  "rm -rf "+ codeqlDatabasePath + ";mv " + projectRootPath + "/codeqldatabase " + codeqlDatabasePath+";"
    mvCodeqlDatabaseDirCmd2     =  "rm -rf "+ root_path +str(getCodeRespName(inputParameter1)) +"/codeqldatabase" +";mv " + codeqlDatabasePath + " " + root_path +str(getCodeRespName(inputParameter1)) +"/codeqldatabase;"

    if "git" in inputParameter1 and "clone" in inputParameter1:
        if inputParameter3 == "":
            finalCMD                    =  (gitCloneCmd+codeqlFinalCMD+mvCodeqlDatabaseDirCmd1 + trivyCmd + mvCodeqlDatabaseDirCmd2 + replaceFileContenCmd).replace("javaEnvSetting",javaEnvSetting)
        else:
            finalCMD                    =  (gitCloneCmd + trivyCmd + replaceFileContenCmd).replace("javaEnvSetting",javaEnvSetting)


    elif os.path.isabs(str(inputParameter1).replace(" ","")):
        if inputParameter3 == "":
            finalCMD                    =  ("cd " + str(inputParameter1) + ";" + codeqlScanCmd +trivyCmd + replaceFileContenCmd).replace("javaEnvSetting",javaEnvSetting)
        else:
            finalCMD                    =  ("cd " + str(inputParameter1) + ";" +trivyCmd + replaceFileContenCmd).replace("javaEnvSetting",javaEnvSetting)


    # finalCMD                    =  gitCloneCmd + "sudo bash -c '''" + finalCMD + "'''"
    msg                         =  msg.replace("finaCMD",finalCMD)
    print(msg)
    returned_value              = subprocess.call(finalCMD, shell=True) # 返回退出码
    print('returned value:', returned_value)
except Exception as e:
    traceback.print_exc()
    pass
finally:
    endTime                     = time.time()
    totalTime                   =  str((endTime-startTime)/60) + "min"
    trivyOutPutFilePath         = root_path + str(getCodeRespName(inputParameter1)) + "/"+trivyOutPutFilename
    codeqlOutFilePath           = root_path + str(getCodeRespName(inputParameter1)) + "/"+codeqlOutName
    scanResultPath              = trivyOutPutFilePath + "\n" + codeqlOutFilePath
    codeqlDatabasePath          = root_path +str(getCodeRespName(inputParameter1)) +"/codeqldatabase"
    excuteFindCommandRes2File(projectRootPath,codeqlOutFilePath)
    if inputParameter3 == "":
        if isCodeqlDBCreateSucc(codeqlDatabasePath):
            msg                         = "[扫描项目]:getCodeRespName\n[分支名称]:branchName\n[扫描状态]:✅\n[扫描耗时]:".replace("branchName",getBranchName(inputParameter1)).replace("getCodeRespName",str(getCodeRespName(inputParameter1))) +totalTime + "\n[扫描结果]: \nscanResultPath".replace("scanResultPath",scanResultPath)
            tempContent                 = trivyOutPutFilePath + "\n" +codeqlOutFilePath
            writeContent2File(tempContent,scanResFileNamePath)
        else:
            msg                         = "[扫描项目]:getCodeRespName\n[分支名称]:branchName\n[扫描状态]:❌\n[失败原因]:codeql数据库创建失败!\n[扫描耗时]:".replace("branchName",getBranchName(inputParameter1)).replace("getCodeRespName",str(getCodeRespName(inputParameter1))) +totalTime + "\n[扫描结果]: \nscanResultPath".replace("scanResultPath",scanResultPath)
    else:
        msg                         = "[扫描项目]:getCodeRespName\n[分支名称]:branchName\n[扫描状态]:✅\n[扫描耗时]:".replace("branchName",getBranchName(inputParameter1)).replace("getCodeRespName",str(getCodeRespName(inputParameter1))) +totalTime + "\n[扫描结果]: \nscanResultPath".replace("scanResultPath",trivyOutPutFilePath)
        writeContent2File(trivyOutPutFilePath,scanResFileNamePath)
    
    sendDingMessage(msg,isAtAll,atPersons)