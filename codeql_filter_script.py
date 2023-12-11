import os
import re
import configparser
import argparse

def filter_files(input_folder, output_folder, config_file):
    # Read config file
    config = configparser.ConfigParser()
    config.read(config_file)
    filter_rules = config.get('filterScriptConfigInfo', 'filterRegularRulesOfCodeQl').split(',')

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_filepath = os.path.join(input_folder, filename)
            output_filepath = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_report.txt")

            with open(input_filepath, 'r', encoding='utf-8') as infile, \
                 open(output_filepath, 'w', encoding='utf-8') as outfile:

                for line in infile:
                    if re.search(r'https://(.*)|Try to find Keywords(.*)', line):
                        include_line = True
                        for rule in filter_rules:
                            if re.search(rule, line):
                                include_line = False
                                break
                        if include_line:
                            outfile.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter and process text files in a folder.")
    parser.add_argument("-f", "--folder", required=True, help="Input folder path")
    args = parser.parse_args()

    input_folder = args.folder
    output_folder = "new_codeql"
    config_file = "/root/tools/config.ini"

    filter_files(input_folder, output_folder, config_file)
    print("Filtering completed. Check the 'new_codeql' folder for results.")
