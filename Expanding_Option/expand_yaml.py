#!/usr/bin/env python

import yaml

yamlFile = yaml.safe_load(open('attack_data_sources.yaml').read())

for yf in yamlFile:
    file_name = yf['name'].lower().replace(" ","_")

    print(f"[+] Writing YAML dump for {file_name}")
    with open(f'{file_name}.yml', 'w') as file:
        yaml.dump(yf, file)
