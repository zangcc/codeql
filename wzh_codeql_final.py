import argparse
import os
import re
import shutil

def read_txt_files(folder_path):
    matched_lines = []

    def Match(line):
        patterns = [
            re.compile("https://(.*)"),                # 匹配 https://
            re.compile("Try to find Keywords(.*)"),   # 匹配 Try to find Keywords
        ]
        for pattern in patterns:
            if pattern.search(line):
                return True
        return False

    def NotMatch(line):
        patterns = [
            re.compile("console\.log(.*)"),           # 匹配 console.log
            re.compile("log\.(approval|mpc)\.debug"), # 匹配 log.approval.debug 和 log.mpc.debug
            re.compile("ExternalAPIsUsedWithUntrustedData(.*)"),  # 匹配 ExternalAPIsUsedWithUntrustedData
            re.compile("with untrusted data from (.*)"),           # 匹配 with untrusted data from param
            re.compile("打印了可能存在敏感信息的变量: getWorkspaceKey(.*)"),           # 匹配 打印了可能存在敏感信息的变量: getWorkspaceKey
            re.compile("打印了可能存在敏感信息的变量: requestBody(.*)"),           # 匹配 打印了可能存在敏感信息的变量: requestBody
            re.compile("打印了可能存在敏感信息的变量: paramMap(.*)"),           # 匹配 打印了可能存在敏感信息的变量: paramMap
            re.compile("打印了可能存在敏感信息的变量: pushMessageParam(.*)"),           # 匹配 打印了可能存在敏感信息的变量: pushMessageParam
            re.compile("打印了可能存在敏感信息的变量: requestParam(.*)"),           # 匹配 打印了可能存在敏感信息的变量: requestParam
            re.compile("打印了可能存在敏感信息的变量: param(.*)"),           # 匹配 打印了可能存在敏感信息的变量: param
            re.compile("打印了可能存在敏感信息的变量: workspaceKey(.*)"),           # 匹配 打印了可能存在敏感信息的变量: worksapceKey
            re.compile("workspaceKey(.*)"), 
            re.compile("打印了可能存在敏感信息的变量: worksapceKey(.*)"),           # 匹配 打印了可能存在敏感信息的变量: worksapceKey
            re.compile("worksapceKey(.*)"), 
            re.compile("打印了可能存在敏感信息的变量: userKey(.*)"),           # 匹配 打印了可能存在敏感信息的变量: userKey
            re.compile("打印了可能存在敏感信息的变量: jsonParam(.*)"),           # 匹配 打印了可能存在敏感信息的变量: jsonParam
            re.compile("打印了可能存在敏感信息的变量: parameter(.*)"),
            re.compile("打印了可能存在敏感信息的变量: dingdingParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: tradeCancelParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: submitTradeParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: auditRecordKey(.*)"),
            re.compile("打印了可能存在敏感信息的变量: userParam(.*)"), 
            re.compile("打印了可能存在敏感信息的变量: userQueryParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: auditParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: jobKey(.*)"),    
            re.compile("打印了可能存在敏感信息的变量: txKey(.*)"), 
            re.compile("打印了可能存在敏感信息的变量: getParam(.*)"),  
            re.compile("打印了可能存在敏感信息的变量: el.machinePubkey(.*)"),   
            re.compile("打印了可能存在敏感信息的变量: signParams(.*)"),
            re.compile("打印了可能存在敏感信息的变量: tokenType(.*)"), 
            re.compile("打印了可能存在敏感信息的变量: updateParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: updateRecord(.*)"),
            re.compile("打印了可能存在敏感信息的变量: recordParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: engineVersionParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: lockCacheKey(.*)"),
            re.compile("打印了可能存在敏感信息的变量: cacheKey(.*)"),
            re.compile("打印了可能存在敏感信息的变量: extPubKey(.*)"),   
            re.compile("打印了可能存在敏感信息的变量: oldExtPubKey(.*)"),
            re.compile("打印了可能存在敏感信息的变量: getAuthPublicKey(.*)"),
            re.compile("打印了可能存在敏感信息的变量: redisKey(.*)"),
            re.compile("打印了可能存在敏感信息的变量: updateParam2(.*)"),
            re.compile("打印了可能存在敏感信息的变量: insertParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: partyRecordParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: resultStatus(.*)"),
            re.compile("打印了可能存在敏感信息的变量: redisCacheKey(.*)"),
            re.compile("打印了可能存在敏感信息的变量: partyRecord(.*)"),
            re.compile("打印了可能存在敏感信息的变量: mpcTaskManagerParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: mpcRegisterAddrParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: getRelationsKey(.*)"),
            re.compile("打印了可能存在敏感信息的变量: getKeyServerExtPubKey(.*)"),
            re.compile("打印了可能存在敏感信息的变量: channelKey(.*)"),
            re.compile("user-provided value(.*)"), 
            re.compile("打印了可能存在敏感信息的变量: auditParamPolicyParam(.*)"),
            re.compile("打印了可能存在敏感信息的变量: getUserKey(.*)"),
            re.compile("打印了可能存在敏感信息的变量: getTxKey(.*)"),
            re.compile("打印了可能存在敏感信息的变量: getAuditRecordKey(.*)"),
            re.compile("logger.debug(.*)"),
            re.compile("log.debug(.*)"),
            re.compile("传入的参数: txType(.*)"),
            re.compile("传入的参数: tokenType(.*)"),
            re.compile("传入的参数: curveType(.*)"),
            re.compile("传入的参数: publicKey(.*)"),
            re.compile("传入的参数: userKey(.*)"),   
            re.compile("传入的参数: workspaceKey(.*)"), 
            re.compile("传入的参数: timestamp(.*)"), 
            re.compile("传入的参数: workspacceKey(.*)"),
            re.compile("Round3BCMessage(.*)"),          #2023-10.11
            re.compile("ecdsa_vault(.*)"), 
            re.compile("eddsa_vault(.*)"), 
            re.compile("eddsa_vault(.*)"), 
            re.compile("StrArray.elements(.*)"), 
            re.compile("composite_key.Party(.*)"), 
            re.compile("Round2P2PMessage(.*)"), 
            re.compile("Round1BCMessage(.*)"), 
            re.compile("Round0BCMessage(.*)"), 
            re.compile("Round2BCMessage(.*)"), 
            re.compile("Round1P2PMessage(.*)"), 
            re.compile("multi_party_ecdsa(.*)"), 
            re.compile("multi_party_eddsa(.*)"),

            
        ]
        for pattern in patterns:
            if pattern.search(line):
                return True
        return False

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='UTF-8') as f:
                lines = f.readlines()
                for line in lines:
                    if Match(line) and not NotMatch(line):
                        matched_lines.append((file_name, line))

    return matched_lines

def write_txt_files(matched_lines, output_folder):
    output_folder = os.path.join(output_folder, 'new_codeql')
    os.makedirs(output_folder, exist_ok=True)

    for file_name, line in matched_lines:
        output_filename = file_name.replace('.txt', '_report.txt')
        output_filepath = os.path.join(output_folder, output_filename)
        with open(output_filepath, 'a') as f:
            f.write(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', required=True, help='输入的文件夹路径')
    args = parser.parse_args()

    input_folder = args.folder

    matched_lines = read_txt_files(input_folder)
    write_txt_files(matched_lines, input_folder)
