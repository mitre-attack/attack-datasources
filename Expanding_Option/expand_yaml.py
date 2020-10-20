#!/usr/bin/env python

# Author: Jose Rodriguez (@Cyb3rPandaH)
# License: GNU General Public License v3 (GPLv3)

import yaml

yamlFile = yaml.safe_load(open('attack_data_sources.yaml').read())

for yf in yamlFile:
    file_name = yf['name'].lower().replace(" ","_")

    print(f"[+] Writing YAML dump for {file_name}")
    with open(f'{file_name}.yml', 'w') as file:
        yaml.dump(yf, file)
