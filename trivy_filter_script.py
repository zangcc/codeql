import argparse
import shutil
import sys,subprocess,re,requests,time,json,configparser,os,traceback,hmac,hashlib,urllib,base64,os.path

file    = os.path.join(os.path.dirname(__file__), '/root/tools/config.ini')
con     = configparser.ConfigParser() # 创建配置文件对象
con.read(file, encoding='utf-8') # 读取文件

trivy_List        =     con.get('filterScriptConfigInfo', 'filterRegularRulesOfTrivy').split(",")
patterns = []


def read_txt_files(folder_path):
    matched_lines = []

    def Match(line):
        patterns = [
            re.compile("(.*.)"),                # 匹配 所有
        ]
        for pattern in patterns:
            if pattern.search(line):
                return True
        return False

    def NotMatch(line):
        for list in trivy_List:
            patterns.append(re.compile(list))

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
    output_folder = os.path.join(output_folder, 'new_trivy')
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
