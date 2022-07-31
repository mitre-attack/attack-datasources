#!/usr/bin/env python

# Author: Jose Rodriguez (@Cyb3rPandaH)

###### Importing Python Libraries
import yaml
yaml.Dumper.ignore_aliases = lambda *args : True

import glob
from os import path

# Libraries to manipulate data
import pandas as pd
from pandas import json_normalize
pd.set_option('display.max_columns', None)

# Libraries to interact with up-to-date ATT&CK content available in STIX format via public TAXII server
from attackcti import attack_client

# Libraries to create CSV file
import csv 

###### Aggregating Data Source Object YAML files from Contribution Folder

print("[+] Accessing data source objects yaml files..")
yaml_files = glob.glob(path.join(path.dirname(__file__),"../..", "contribution", "*.yml"))
yaml_loaded = [yaml.safe_load(open(yaml_file).read()) for yaml_file in yaml_files]

print("[+] Creating data source objects aggregated yaml file..")
with open(f'../attack_data_sources_objects.yaml', 'w') as file:
    yaml.dump(yaml_loaded, file, sort_keys = False)

###### Creating YAML file with (Sub)Techniques to Data Components Mapping

# Getting ATT&CK - Enterprise Matrix
print("[+] Getting ATT&CK - Enterprise form TAXII Server..")

# Instantiating attack_client class
lift = attack_client()
# Getting techniques for windows platform - enterprise matrix
attck = lift.get_enterprise_techniques(stix_format = False)
# Creating Dataframe
attck = json_normalize(attck)
attck = attck[['technique_id','is_subtechnique','technique','tactic','platform','data_sources']]
attck = attck.explode('data_sources').reset_index(drop = True)
attck[['data_source','data_component']] = attck.data_sources.str.split(pat = ": ", expand = True)
attck = attck.drop(columns = ['data_sources'])
attck['data_source'] = attck['data_source'].str.lower()
attck['data_component'] = attck['data_component'].str.lower()

print("[+] Getting ATT&CK Data Sources to Relationships mapping..")
yamlFile = open('../attack_data_sources_objects.yaml', 'r') # Accessing yaml file
dict = yaml.safe_load(yamlFile) # Loading names of data sources into a dictionary object
yamlFile.close() # Closing yaml file

attck_mapping = pd.DataFrame(dict)
attck_mapping = attck_mapping[['name','definition','collection_layers','platforms','contributors','data_components','references']].rename(columns={'platforms':'data_source_platform'})
attck_mapping = attck_mapping.explode('data_components').reset_index(drop = True)

component = attck_mapping['data_components'].apply(pd.Series).rename(columns={'name':'data_component_name'})
attck_mapping = pd.concat([attck_mapping,component], axis = 1).drop(['data_components'], axis = 1)

attck_mapping = attck_mapping.reindex(columns = ['name','definition','collection_layers','data_source_platform','contributors','data_component_name','type','description','relationships','references'])
attck_mapping = attck_mapping.explode('relationships').reset_index(drop = True)

relations = attck_mapping['relationships'].apply(pd.Series)
attck_mapping = pd.concat([attck_mapping,relations], axis = 1).drop(['relationships'], axis = 1)

attck_mapping['data_source'] = attck_mapping['name'].str.lower()
attck_mapping['data_component'] = attck_mapping['data_component_name'].str.lower()
attck_mapping = attck_mapping.drop(['name','data_component_name'], axis = 1)

print("[+] Merging (Sub)Technqiues to Relationships mapping DATAFRAME..")
technique_to_relationships = pd.merge(attck, attck_mapping, how = 'left', on = ['data_source','data_component'])
technique_to_relationships = technique_to_relationships.reindex(columns = ['technique_id','is_subtechnique','technique','tactic','platform','data_source','definition','collection_layers','data_source_platform','contributors','data_component','type','description','source_data_element','relationship','target_data_element','references'])

technique_to_relationships_dict = technique_to_relationships.reset_index().to_dict(orient = 'records')
for x in technique_to_relationships_dict:
    x.pop('index')

technique_to_components_dict = attck.reset_index().to_dict(orient = 'records')
for x in technique_to_components_dict:
    x.pop('index')

print("[+] Creating (Sub)Technqiues to Relationships mapping YAML file..")
with open("../techniques_to_relationships_mapping.yaml", 'w') as yamlfile:
    data = yaml.dump(technique_to_relationships_dict, yamlfile,sort_keys = False, default_flow_style = False)

print("[+] Creating (Sub)Technqiues to Components mapping YAML file..")
with open("../techniques_to_components_mapping.yaml", 'w') as yamlfile:
    data = yaml.dump(technique_to_components_dict, yamlfile,sort_keys = False, default_flow_style = False)

###### Creating CSV file with (Sub)Techniques to Components/Relationships Mapping
print("[+] Creating ATT&CK techniques to relationships mapping CSV file..")

header_fields = ['technique_id','is_subtechnique','technique','tactic','platform','data_source','definition','collection_layers','data_source_platform','contributors','data_component','type','description','source_data_element','relationship','target_data_element','references']
with open('../techniques_to_relationships_mapping.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, header_fields)
    dict_writer.writeheader()
    dict_writer.writerows(technique_to_relationships_dict)

header_fields = ['technique_id','is_subtechnique','technique','tactic','platform','data_source','data_component']
with open('../techniques_to_components_mapping.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, header_fields)
    dict_writer.writeheader()
    dict_writer.writerows(technique_to_components_dict)
