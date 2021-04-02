#!/usr/bin/env python

import yaml
import glob
from os import path


yaml_files = glob.glob(path.join(path.dirname(__file__), "*.yml"))
yaml_loaded = [yaml.safe_load(open(yaml_file).read()) for yaml_file in yaml_files]

with open('attack_data_sources.yaml', 'w') as file:
    yaml.dump(yaml_loaded, file, sort_keys = False)
