# Defining ATT&CK Data Sources
As part of the revamping process of **ATT&CK data sources**, we have defined an initial methodology that will help us improve the definition of current data sources. The idea behind this methodology is to ensure same quality of information among data sources, and provide additional information or metadata related to data sources in order to get a better understanding of them. 

<img src="images/Methodology_Data_Sources.jpg" width=500>

You can find a more detailed explanation of this methodology here:

* [Defining ATT&CK Data Sources, Part I: Enhancing the Current State](https://medium.com/mitre-attack/defining-attack-data-sources-part-i-4c39e581454f)
* [Defining ATT&CK Data Sources, Part II: Operationalizing the Methodology](https://medium.com/mitre-attack/defining-attack-data-sources-part-ii-1fc98738ba5b)

## Data Source Object
Currently, data sources are metadata provided for each (sub)technique. However, in order to be able to add metadata to each data source, we have proposed the definition of a data source object as part of the ATT&CK model.

<img src="images/Data_Source_Object.png" width=500>

## Relationships & Sub Data Sources
As part of the new metadata provided by ATT&CK data sources, we proposed the following concepts: **relationships** and **data components**. These concepts will help us to represent adversary behavior from a data perspective. In addition, they might be good reference to start mapping telemetry collected in your environment to specific sub(techniques) and/or tactics.

<img src="images/Sub_Technique_Data_Components.jpg" width=500>

## Where can you find Data Sources Objects?
We are storing this new metadata using YAML files, so you can access this content programatically.

```yaml
- name: Service
  definition: Information about software programs that run in the background and typically start with the operating system.
  collection_layers:
    - host
  platforms:
    - Windows
  contributors: 
    - ATT&CK
  data_components:
    - name: service creation
      type: activity
      relationships:
        - source_data_element: user
          relationship: created
          target_data_element: service
  references:
    - https://docs.microsoft.com/en-us/dotnet/framework/windows-services/introduction-to-windows-service-applications
    - https://www.linux.com/news/introduction-services-runlevels-and-rcd-scripts/
```

In the image above, you can see the structure of the **Service** data source as an example of the content you will find within each YAML file.

Based on our initial research, we have identified relationships such as: A **user** has **created** a **Service**

We are grouping these type of relationships within the data component: **Service Creation**.

## How can we consume this information?
The idea of storing all this data using **YAML** files is to facilitate the consumption of data sources definition content. So, feel free to use any tool that can handle yaml files and that is available for you. We have prepared a Jupyter notebook using libraries such attackcti, pandas, and yaml to give you an example of how can you gather up to date ATT&CK knowledge and YAML files' content, so you can merge all this information. You can find the notebook in the following link.

- [Adding more security context to the data source piece of ATT&CK - Notebook](./DataSourcesDefinition.ipynb)

Something you need to consider when consuming the data within each YAML file is that some of the names of current data sources has been changed based on the propoed methodology. We are also providing a YAML file showing current and proposed data sources names. The structure of the YAML files is showed below: On the left, you can see the current names of data sources and on the right you can see the proposed name.

```yaml
Sensor health and status: Sensor log
Access tokens: Access token
PowerShell logs: Powershell log
API monitoring: API
Application logs: Application log
File monitoring: File
Authentication logs: Logon session
Named Pipes: Named pipe
Process monitoring: Process
Process use of network: Process
Process command-line parameters: Process
DLL monitoring: Module
Loaded DLLs: Module
Windows Registry: Windows registry
DNS records: DNS record
Digital certificate logs: Digital certificate log
WMI Objects: WMI object
Services: Service
DNS records: DNS
```

## Have we defined each data source within ATT&CK?
The initial scope of this research considered the Enterprise matrix, the Windows platform, the host collection layer and free telemetry such as Sysmon logs. Therefore, there are a lot of opportunities for you to contribute to the data sources piece of ATT&CK.



## Notice

©2020 Copyright The MITRE Corporation. ALL RIGHTS RESERVED.

Approved for Public Release; Distribution Unlimited. Public Release Case Number 20-2841

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This project makes use of ATT&CK®

[ATT&CK Terms of Use](https://attack.mitre.org/resources/terms-of-use/)
