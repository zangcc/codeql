import argparse
import os
import re
import shutil

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
        patterns = [
            re.compile("com.alibaba.nacos:nacos-api(.*)"),           # 匹配 com.alibaba.nacos:nacos-api依赖
            re.compile("com.alibaba.nacos:nacos-client(.*)"), 
            re.compile("com.alibaba.nacos:nacos-common(.*)"), 
            re.compile("org.springframework:spring-beans(.*)"), 
            re.compile("org.springframework:spring-core(.*)"), 
            re.compile("org.springframework:spring-expression(.*)"),
            re.compile("org.springframework:spring-web(.*)"),
            re.compile("org.springframework.vault:spring-vault-core(.*)"),
            re.compile("org.springframework:spring-webmvc(.*)"),
            re.compile("org.springframework.boot:spring-boot-actuator-autoconfigure(.*)"),
            re.compile("org.springframework.boot:spring-boot-starter-web(.*)"),
            re.compile("org.springframework.boot:spring-boot-autoconfigure(.*)"),
            re.compile("org.apache.rocketmq:rocketmq-spring-boot-starter(.*)"),
            re.compile("org.yaml:snakeyaml(.*)"),
            re.compile("com.squareup.okio:okio(.*)"),
            re.compile("org.apache.tomcat.embed:tomcat-embed-core(.*)"),
            re.compile("org.apache.tomcat.embed:tomcat-embed-websocket(.*)"),
            re.compile("org.codehaus.jettison:jettison(.*)"),
            re.compile("org.eclipse.jetty:jetty-client(.*)"),
            re.compile("org.eclipse.jetty:jetty-http(.*)"),
            re.compile("org.eclipse.jetty:jetty-io(.*)"),
            re.compile("org.eclipse.jetty:jetty-server(.*)"),
            re.compile("org.eclipse.jetty:jetty-servlets(.*)"),
            re.compile("org.eclipse.jetty:jetty-util(.*)"),
            re.compile("org.eclipse.jetty:jetty-webapp(.*)"),
            re.compile("org.eclipse.jetty:jetty-xml(.*)"),
            re.compile("decode-uri-component(.*)"),
            re.compile("com.squareup.okio:okio(.*)"),
            re.compile("org.apache.rocketmq:rocketmq-client(.*)"),
            re.compile("org.bouncycastle:bcprov-jdk15on(.*)"),
            re.compile("org.json(.*)"),
            re.compile("org.bouncycastle:bcprov-jdk15to18(.*)"),
            re.compile("org.apache.tomcat.embed:tomcat-embed-core(.*)"),
            re.compile("org.java-websocket:Java-WebSocket(.*)"),
            re.compile("com.fasterxml.jackson.core:jackson-databind(.*)"),
            re.compile("com.h2database:h2(.*)"),
            re.compile("io.undertow:undertow-core(.*)"),
            re.compile("org.postgresql:postgresql(.*)"),
            re.compile("org.apache.dubbo:dubbo(.*)"),
            re.compile("com.baomidou:mybatis-plus(.*)"),
            re.compile("io.netty:netty-all(.*)"),
            re.compile("io.netty:netty-codec(.*)"),
            re.compile("io.netty:netty-handler(.*)"),
            re.compile("com.alibaba:fastjson(.*)"),
            re.compile("org.springframework.boot:spring-boot(.*)"),
            re.compile("com.google.code.gson:gson(.*)"),
            re.compile("org.springframework.security:spring-security-core(.*)"),
            re.compile("org.springframework.security:spring-security-web(.*)"),
            re.compile("nth-check(.*)"),
            re.compile("org.springframework.security:spring-security-config(.*)"),
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
