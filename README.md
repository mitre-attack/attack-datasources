# ATT&CK Data Sources
As part of the **ATT&CK 2021 Roadmap**, we have defined an initial methodology that will help us improve the definition of current data sources. The idea behind this methodology is to ensure same quality of information among data sources, and provide additional information or metadata related to data sources in order to get a better understanding of them and expedite the identification of relevant data for recommended data sources.

<img src="docs/images/ATTCK_InfoSec_Community.jpg" width=500>

The previous image shows only some of the elements that the methodology brings out such as *data components* and *relationships*, however it represents the main goal of this project: **connect the defensive data in ATT&CK with how operational defenders analyze potential adversaries/ behaviors**.

## **A Methodology to define Data Sources Objects**

<img src="docs/images/Methodology_Data_Sources.jpg" width=500>

The following methodology describes basic steps we followed in order to define ***data sources objects***. Even though this methodology considers the analysis of security telemetry, specific events' names or identification numbers (ids) are not listed within the information provided by ATT&CK. 

### **Identifying Sources of Data**
Documenting security telemetry collected within a network environment will provide us with data and information that should help us to answer to questions such as *why were these security events generated in my environment? (Activity)*, *what operating system supports its generation? (Platform)*, *where were they collected? (Collection Layer)*

<img src="docs/images/process_creation_example.jpg" width=500>

Let's use security event *4688: A new process has been crated* provided by *Microsoft Windows security auditing* as a basic example to understand this step of the methodology. The action that triggered the generation of this event was the creation of a new process (Activity). This security event can be collected by using the built-in event logging application for devices that work with the Windows operating system (Platform). Because we are working with a built-in application, this security event was collected at the host level.

### **Identifying Data Elements**
Data elements help us not only to represent (elements) and describe (attributes) relevant network security concepts, but also to get a better understanding of the interactions (relationships) among them. There is a fundamental rule that we should consider when defining: **there is no one correct way to define data elements**. In other words, the definition of data elements and its attributes will depend on the reality of your organization.

Let's take a look at the *4688: A new process has been crated* security event again. Within the information provided by this event, we have identified network security concepts such as the [*user account*](https://github.com/mitre-attack/attack-datasources/blob/main/contribution/user_account.yml) that requested the creation of the [*process*](https://github.com/mitre-attack/attack-datasources/blob/main/contribution/process.yml), and we also have information of the process which ran the new process. This security event also provides metadata that can help us to describe our data elements. For instance, regarding the user account data element, we have information of its *Logon Id* and the *Domain* it belongs to. Regarding the process data element, we have information of its *Id* and *Token Elevation Type*.

The definition of data elements within the ATT&CK framework migh or might not align with the reality of your organization. However, as a [mid-level model (Figure 5)](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf), you can use ATT&CK as a starting point and customize your definition of data elements.

### **Identifying Relationships Among Data Elements**
By documenting telemetry collected within a netork environment we were able to identify the activity that triggered the generation of security telemetry (*creation of a new process*) and data elements that were involved on this action (*user account* and *process*). Using these concepts as a reference, we can start describing interactions among data elements through relationships. The image below shows some of the relationships that we have identified so far:

<img src="docs/images/relationships_example.jpg" width=500>

We have categorized relationships in *activity* and *information*. Activity relationships are the ones that make reference to the action that triggered the generation of the security event. On the other hand, information relationships are the ones defined based on the metadata provided by the security event. As you can see in the image above, one event can give you security context for more than one relationship. What relationship(s) should we use? It will depend on the use case you are working on.

If we repeat all the steps described so far, we can start identifying different relationships among data elements based on different security events.

<img src="docs/images/more_relationships_example.jpg" width=500>

### **Defining Data Components**
As you can see in the image above, different relationships can be indentified based on information provided by security events. However, some of them describe the same security context. Therefore, we decided to group relationships that are related. *Data components* will help us to categorized relationships among data elements based on the security context they describe (*i.e. Creation, execution, deletion*) and the type of relationships (*Activity and Information*). The following image shows data components defined for the relationships that we have identified previously:

<img src="docs/images/data_components_example.jpg" width=500>

Even though relationships describe interactions among different data elements, grouping them throguh data components allowed us to identify main network security concepts that are described by collected security events such as *Process*, *Command*, and *Network Traffic*. These network security concepts will represent data sources that we can collect data and information from.

<img src="docs/images/data_sources_example.jpg" width=500>

### **Assembling ATT&CK Data Source Objects**
During the development of this methodology we have identified data sources' context that can help us to describe the activity within a network environment. We have decided to formalize all this contex thorugh the definition of **Data Source Objects** within the ATT&CK Object Model. The objects' strcuture is represented in the following image:

<img src="docs/images/Data_Source_Object.png" width=500>

## **How Data Source Objects Can Support Security Operations?**

### **Representation of Adversary Behavior**
Data components gives us context of the activity or metadata related to network security concepts recommended as data sources by the ATT&CK framework.

For instance, let's say the *Process* data source is recommended for the detection of *T1543.003 Create or Modifiy System Process / Windows Service* technique. Without any other security context, the first question that might come to your mind is *what information about a process is required?*. The following image shows some of the available option by using components:

<img src="docs/images/process_data_components_example.jpg" width=500>

Each data component represents activity and/or information generated within a network environment because of actions or behaviors performed by a user or a potential adversary. The ATT&CK framework (v9) now provides data components that can help you to represent specific actions or behaviors related to a technique. According to the framework, the **creation of processes** and **execution of operating system's API calls** are a good starting point from a Process perspective.

<img src="docs/images/attck_T1543-003.jpg" width=500>

### **Identification of Relevant Security Events**
At the beginning of this document, we mentioned that the main goal of this project was to **connect the defensive data in ATT&CK with how operational defenders analyze potential adversaries/ behaviors**. Even though the scope of this project does not consider mapping security events to data components and relationships, we believe that the information provided by data source objects can help you to identify relevant security data that should be collected in your environemnt in order to expedite the development of effective detections.

<img src="docs/images/Sub_Technique_Data_Components.jpg" width=500>

For example, the framework considers *Process/Process Creation* s a recommended data source for *T1543.003 Create or Modifiy System Process / Windows Service* technique. The mos important  question here is *What security events logs can give me context about the creation of a process?*. For Windows platform environments, Security Auditing event 4688 and Sysmon event 1 can help us to cover this data source recommendation. The image above shows an example of security events mapped to other recommended data sources for the same technique.

## **Where are the New Data Sources Objects Stored?**
V9 of the ATT&CK framework contains only data components as part of the new metadata for sata sources. However, you can find our current Data Source Objects [here](https://github.com/mitre-attack/attack-datasources/tree/main/contribution). We are storing this new metadata using YAML files, but in the future it will be store within our TAXII Server in STIX format.

```yaml
name: Process
definition: Information about instances of computer programs that are being executed by at least one thread.
collection_layers:
  - host
platforms:
  - Windows
  - Linux
  - macOS
contributors: 
  - ATT&CK
  - CTID
data_components:
  - name: process creation
    type: activity
    description: A process was created.
    relationships:
      - source_data_element: user
        relationship: created
        target_data_element: process
      - source_data_element: process
        relationship: created
        target_data_element: process
  - name: OS api execution
    type: activity
    description: A process executed operating system api functions.
    relationships:
      - source_data_element: process
        relationship: executed
        target_data_element: api call
references:
  - https://docs.microsoft.com/en-us/windows/win32/procthread/processes-and-threads
```

## **How can you Consume Data Source Objects Content?**
The idea of storing all this data using **YAML** files is to facilitate the consumption of data source objects content until we move everything to our TAXII Server. So, feel free to use any tool that can handle yaml files and that is available for you. We have prepared a Jupyter notebook using libraries such attackcti, pandas, and yaml to give you an example of how can you gather up-to-date ATT&CK knowledge and YAML files' content, so you can merge all this information. You can find the notebook in the following link.

- [Adding more security context to the data source piece of ATT&CK - Notebook](https://github.com/mitre-attack/attack-datasources/blob/main/DataSourcesDefinition.ipynb)

## **How Can You Contribute?**
We love feedback!! Hopefully, the explanation of our methodology provided in this document helps you to undertand the structure of a data source object and gives you an idea on how to come up with new content. Take a look at the current data source objects [here](https://github.com/mitre-attack/attack-datasources/tree/main/contribution), propose or improve data relationships, components, and data sources, and submit a pull request!!

## References

* [Defining ATT&CK Data Sources, Part I: Enhancing the Current State](https://medium.com/mitre-attack/defining-attack-data-sources-part-i-4c39e581454f)
* [Defining ATT&CK Data Sources, Part II: Operationalizing the Methodology](https://medium.com/mitre-attack/defining-attack-data-sources-part-ii-1fc98738ba5b)
* [Data Sources, Containers, Cloud, and More: What’s New in ATT&CK v9?](https://medium.com/mitre-attack/attack-april-2021-release-39accaf23c81)
* [ATT&CK 2021 Roadmap](https://medium.com/mitre-attack/att-ck-2021-roadmap-68bab3886fa2)
* [T1543.003 - Create or Modify System Process: Windows Service](https://attack.mitre.org/techniques/T1543/003/)
* [Microsoft Windows Security Auditing - Event 4688: A new process has been created](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4688)

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
