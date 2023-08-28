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
mavenDir                          =    str(con.get('DependencyToolConfigInfo', 'mavenDir'))
mavenSettingsFile                 =    str(con.get('DependencyToolConfigInfo', 'mavenSettingsFile'))
mavenLocalRepositoryDir           =    str(con.get('DependencyToolConfigInfo', 'mavenLocalRepositoryDir'))
delombokJarFilePath               =    str(con.get('DependencyToolConfigInfo', 'delombokJarFilePath'))
codeqlBinPath                     =    str(con.get('DependencyToolConfigInfo', 'codeqlBinPath'))
javaHome                          =    str(con.get('DependencyToolConfigInfo', 'javaHome'))
javaHomeDir                       =    javaHome.replace("bin/java","")
javaEnvSetting                    =    "export JAVA_HOME=javaHomeDir;export PATH=$JAVA_HOME/bin:$PATH;export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar".replace("javaHomeDir",javaHomeDir)
codeqlDBCreateSuccFlagList        =     con.get('DependencyToolConfigInfo', 'codeqlDBCreateSuccFlagList').split(",")
isAtAll                           = str(con.get('DingdingConfigInfo', 'isAtAll'))
atPersons                         =     con.get('DingdingConfigInfo', 'atPersons').split(",")


###################################工具集###################################

def writeContent2File(content,filePath):
    # 以读模式打开文件
    with open(filePath, 'a') as f:
        f.write(content+"\n")

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
    if "git" in string and "clone" in string:
        pattern = r"/([a-zA-Z-_0-9]+)\.git" # 定义正则表达式模式
        match = re.search(pattern, string) # 使用search方法查找匹配
        if match: # 如果找到匹配
            return match.group().replace(".git","").replace("/","")
        else: # 如果没有找到匹配
            pass
    elif os.path.isabs(str(string).replace(" ","")):
        if "-b" in str(string):
            string = string.split(" ")[0]
        stringList = string.replace("//","/").replace(" ","").split("/")
        if stringList[-1] == "":
            projectName        = stringList[-2]
        else:
            projectName        = stringList[-1]
        return projectName

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

def getBranchName(gitCommand):
    gitCommandStr = str(gitCommand)
    gitCommand    = getGitCommandList(gitCommand)
    branchName    = ""
    try:
        if "git" in gitCommandStr:
            if "/" in gitCommand[4]:
                gitCommand[4] = gitCommand[4].replace("/","%252F")
            branchName    = gitCommand[4] 
        else:
            if " -b" in gitCommandStr:
                branchName = str(gitCommand[2])
            else:
                branchName = "master"
    except:
        if "gitlab" in gitCommandStr:
            branchName             =   "main"
        elif "phabricator" in gitCommandStr:
            branchName             =   "master"
        elif "github" in gitCommandStr:
            branchName             =   "main"
                
        pass
    finally:
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
    DependencyCheckOutputName       = str(getCurrentTime())+"_"+str(getCodeRespName(inputParameter1))+"_"+getBranchName(str(inputParameter1))+"_DependencyCheck扫描结果.html"
    DependencyCheckCmd              = "sudo dependency-check.sh --project 'myproject' -s  scanPath   -n  --out outPutname".replace("myproject",getCodeRespName(inputParameter1)).replace("outPutname",DependencyCheckOutputName).replace("scanPath",projectRootPath)+";"
    gitCloneCmd                     =  "cd " + str(root_path) + "; sudo  rm -rf "+ str(getCodeRespName(inputParameter1)) + ";"+inputParameter1 +";"
    codeqlOutName                   = str(getCurrentTime())+"_"+str(getCodeRespName(inputParameter1))+"_"+getBranchName(str(inputParameter1))+"_codeql扫描结果.txt"
    codeqlScanCmd                   = ""
    ###################################工具集###################################
    if inputParameter2 == "java":
        lombokCommands          = ['javaHome -jar delombokJarFilePath delombok -n --onlyChanged . -d "delombok"'.replace("javaHome",javaHome).replace("delombokJarFilePath",delombokJarFilePath),'find "delombok" -name \'*.java\' -exec sed \'/Generated by delombok/d\' -i \'{}\' \';\'','find "delombok" -name \'*.java\' -exec sed \'/import lombok/d\' -i \'{}\' \';\'','cp -r "delombok/." "./"','rm -rf "delombok"']
        lombokCommands          = " ; ".join(lombokCommands)
        cmd                     = inputParameter1 # 获取第一个参数
        cdToRootCmd             = "cd " + str(root_path) + str(getCodeRespName(cmd)) + ";"
        lombokCmd               = cdToRootCmd   +   lombokCommands   + ";"
        codeqlCreateCmd         = "javaEnvSetting  ;codeqlBinPath database create codeqldatabase --language=java --command='mavenDir/bin/mvn    -gs mavenSettingsFile  clean install   -Dmaven.test.skip -Dmaven.repo.local=mavenLocalRepositoryDir' --overwrite".replace("mavenSettingsFile",mavenSettingsFile).replace("mavenLocalRepositoryDir",mavenLocalRepositoryDir).replace("codeqlBinPath",codeqlBinPath).replace("mavenDir",mavenDir)+";"
        codeqlScanCmd           = "for file in codeqlJavaFilesPath*.ql; do sudo codeqlBinPath query run --database=codeqldatabase \"$file\">>codeqlOutName; done".replace("codeqlOutName",codeqlOutName).replace("codeqlJavaFilesPath",codeqlJavaFilesPath).replace("codeqlBinPath",codeqlBinPath)+";"
        codeqlFinalCMD          = (lombokCmd+codeqlCreateCmd+codeqlScanCmd)

    elif inputParameter2 == "js" or inputParameter2 == "javascript":
        cmd                     = inputParameter1 # 获取第一个参数
        cdToRootCmd             = "cd " + str(root_path) + str(getCodeRespName(cmd)) + ";"
        codeqlCreateCmd         = cdToRootCmd  + "codeqlBinPath database create codeqldatabase --language=javascript  --overwrite".replace("codeqlBinPath",codeqlBinPath)+";"
        codeqlScanCmd           = "for file in codeqlJSFilesPath*.ql; do sudo codeqlBinPath query run --database=codeqldatabase \"$file\">>codeqlOutName; done".replace("codeqlOutName",codeqlOutName).replace("codeqlJSFilesPath",codeqlJSFilesPath).replace("codeqlBinPath",codeqlBinPath)+";"
        codeqlFinalCMD          = (codeqlCreateCmd+codeqlScanCmd)

    elif inputParameter2 == "c" or inputParameter2 == "cpp" or inputParameter2 == "c++" :
        cmd                     = inputParameter1 # 获取第一个参数
        cdToRootCmd             = "cd " + str(root_path) + str(getCodeRespName(cmd)) + ";"
        codeqlCreateCmd         = cdToRootCmd  + "codeqlBinPath database create codeqldatabase --language=cpp  --command='bash /root/tools/build.sh'   --overwrite".replace("codeqlBinPath",codeqlBinPath)+";"
        codeqlScanCmd           = "for file in codeqlcppFilesPath*.ql; do sudo codeqlBinPath query run --database=codeqldatabase \"$file\">>codeqlOutName; done".replace("codeqlOutName",codeqlOutName).replace("codeqlcppFilesPath",codeqlcppFilesPath).replace("codeqlBinPath",codeqlBinPath)+";"
        codeqlFinalCMD          = (codeqlCreateCmd+codeqlScanCmd)
    

    msg="++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++运行下面命令：++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\nfinaCMD \n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++运行上面面命令：++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"

    trivyOutPutFilename         =  str(getCurrentTime())+"_"+str(getCodeRespName(inputParameter1))+"_"+ getBranchName(str(inputParameter1)) +"_trivy扫描结果.txt"
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