# Control-M Workbench Quickstart Guide

Control-M Workbench is a no-cost, self-service, standalone development environment that is launched in minutes, giving you the autonomy to code, debug, and test jobs in JSON or Python.


## Getting started with Control-M Workbench
In order to get workbench you will need permissions to download Control-M/Enterprise Manager from EPD. 

### Prerequisites

- Docker installed
- 8GB of free memory
- Free ports: 8443 plus any other port used for external agent communication

#### Follow these steps to get an access key:
1.	Connect to EPD: ```https://www.bmc.com/support/resources/product-downloads.html```
2.	In EPD select “Product download tool”
3.	Select “Container Products” from the filters
4.	Click the “Download Container Access Key”, this will download a file that contains the access key to containers.bmc.com

#### Accessing containers.bmc.com:
1.	Ensure that you have docker installed and running.
2. With the user that has permissions to the EPD, run the following (without the brackets):
``` 
docker login containers.bmc.com -u<MyUser>
```
4.	When prompted for a password, paste the key you downloaded in the previous step.

#### Pulling the Workbench Image:
1.	Ensure that you are logged in to containers.bmc.com
2. Run:
```
docker pull containers.bmc.com/bmc/workbench:9.21.220-GA
```
- Note: 9.21.220-GA is the tag for the version of the image. </br>To get the latest Workbench version, modify this to the latest version of Automation API. </br>You can find the latest Automation API version here: <a target="_blank" href="https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_Intro.htm">Automation API</a>


### Get the Workbench image


To start a container, run the following docker command:
```
docker run -dt --cpus=4 -m 8g -p 8443:8443 --hostname=workbench containers.bmc.com/bmc/workbench:9.21.220-GA
```
We recommend explicitly limiting the consumption of memory and CPU on the host. It's recommended to run (adjust memory and CPU parameters according to the limits you wish to set)

## Using Control-M Workbench with Control-M Python Client

You can use the workbench to test your python workflows with the [ctm-python-client](https://controlm.github.io/ctm-python-client/gettingstarted.html) library.

You can check the tutorials of Control-M Python Client [here](https://controlm.github.io/ctm-python-client/tutorials.html).

## Using Control-M Workbench with Automation API

Control-M Workbench can be a handy tool to test jobs written in JSON using <a target="_blank" href="https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_Intro.htm">Automation API</a>. You can either use the Automation API via curl, postman, or any other REST client or use the Automation API cli. 

### Creating your first job flow

Before you begin use the following steps, as described in [Setting up the prerequisites](https://docs.bmc.com/docs/automation-api/monthly/tutorials-setting-up-the-prerequisites-1116950280.html):
1. Ensure that you installed [Control-M Automation CLI](https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_Installation.htm#Installation-ctm_cli)
2. Set up a workbench environment, use the following command
    ``` 
    ctm environment workbench::add 
    ```
3. Make your workbench environment as default
    ```
    > ctm environment set workbench

    info:    current environment: workbench
    info:    environments: {
      "workbench": {
        "endPoint": "https://localhost:8443/automation-api",
        "user": "workbench"
      }
    }
    ```
  4. Verify the set up by running an API commands
      - Obtain information about the Control-M Servers by running the config servers::get API command:
        ```
        > ctm config servers::get

        [
          {
            "name": "workbench",
            "host": "workbench",
            "state": "Up",
            "desiredState": "Up",
            "message": "Connected",
            "version": "9.0.21.100",
            "OSType": "Linux 711.amzn2.x86_64",
            "status": "0"
          }
        ]
        ```
      - Log in to Control-M Workbench and return a session token by running the session login API command
        ```
        > ctm session login

        {
          "username": "workbench",
          "token": "E14A4F8E45406977B31A1B091E5E04237...",
          "version": "9.21.220"
        }
        ```

#### Step 1 - Create your first job flow
Let's look at the source code in the AutomationAPISampleFlow.json file. By examining the contents of this file, you'll learn about the structure of the job flow and what it should contain.

```
{
    "TestFolderAutomationAPI": {
        "Type": "Folder",
        "RunAs": "workbench",

        "StartJob": {
            "Type": "Job:Command",
            "Command": "echo \"Hello\"",
            "RunAs": "workbench"
        },

        "EndJob": {
            "Type": "Job:Command",
            "Command": "echo \"Bye\"",
            "RunAs": "workbench"
        },

        "Flow": {
            "Type": "Flow",
            "Sequence": ["StartJob", "EndJob"]
        }
    }
}
```

This example contains two [jobs](https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_CodeRef_JobTypes.htm): CommandJob. These jobs are contained within a [folder](https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_CodeRef_Folder.htm#Folder)  named AutomationAPISampleFlow. To define the sequence of job execution, the [Flow](https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_CodeRef_Folder.htm#Flow)  object is used.

#### Step 2 - Verify the code for Control-M
Let's take the <b>AutomationAPISampleFlow.json</b> file, which contains job definitions, and verify that the code within it is valid. To do so, use the [build](https://docs.bmc.com/docs/automation-api/monthly/build-service-1116950325.html) command.  The following example shows the command and a typical successful response.
```
> ctm build AutomationAPISampleFlow.json

[
  {
    "deploymentFile": "AutomationAPISampleFlow.json",
    "successfulFoldersCount": 0,
    "successfulSmartFoldersCount": 1,
    "successfulSubFoldersCount": 0,
    "successfulJobsCount": 2,
    "successfulConnectionProfilesCount": 0,
    "successfulDriversCount": 0,
    "isDeployDescriptorValid": false
  }
]
```
If the code is not valid, an error is returned.

#### Step 3 - Run the source code
Use the [run](https://docs.bmc.com/docs/automation-api/monthly/run-service-1116950330.html) command to run the jobs in the Control-M environment. The returned runId is used to check the job status. The following shows the command and a typical successful response.
```
> ctm run AutomationAPISampleFlow.json

{
  "runId": "b877cd1e-a749-4436-bf00-8b7266e05957",
  "statusURI": "https://localhost:8443/automation-api/run/status/b877cd1e-a749-4436-bf00-8b7266e05957",
  "monitorPageURI": "https://localhost:8443/ControlM/Monitoring/Viewpoints/Viewpoint?selDef=0000000100030014CONTROL-M%2520Name0004LIKE0009workbench0008ORDER_ID0005ILIKE001700001,00002,000030011DELETE_FLAG0004LIKE0005False"
}
```
This code ran successfully and returned the <b>runId</b> of "b877cd1e-a749-4436-bf00-8b7266e05957".

#### Step 4 - Check job status using the runId
The following command shows how to check job status using the <b>runId</b>. Note that when there is more than one job in the flow, the status of each job is checked and returned.

```
> ctm run status b877cd1e-a749-4436-bf00-8b7266e05957

{
  "completion": "Completed",
  "statuses": [
    {
      "jobId": "workbench:00001",
      "folderId": "workbench:",
      "numberOfRuns": 1,
      "name": "TestFolderAutomationAPI",
      "folder": "TestFolderAutomationAPI",
      "type": "Folder",
      "status": "Executing",
      "held": false,
      "deleted": false,
      "cyclic": false,
      "startTime": "Oct 2, 2023, 11:42:59 AM",
      "endTime": "",
      "estimatedStartTime": [
        "20231002114259"
      ],
      "estimatedEndTime": [
        "20231002115420"
      ],
      "orderDate": "231002",
      "ctm": "workbench",
      "description": "",
      "host": "workbench",
      "application": "",
      "subApplication": "",
      "outputURI": "Folder has no output",
      "logURI": "https://workbench:8443/automation-api/run/job/workbench:00001/log"
    },
    {
      "jobId": "workbench:00002",
      "folderId": "workbench:00001",
      "numberOfRuns": 0,
      "name": "StartJob",
      "folder": "TestFolderAutomationAPI",
      "type": "Command",
      "status": "Wait Host",
      "held": false,
      "deleted": false,
      "cyclic": false,
      "startTime": "",
      "endTime": "",
      "estimatedStartTime": [
        "20231002114420"
      ],
      "estimatedEndTime": [
        "20231002114920"
      ],
      "orderDate": "231002",
      "ctm": "workbench",
      "description": "",
      "host": "workbench",
      "application": "",
      "subApplication": "",
      "outputURI": "Job did not run, it has no output",
      "logURI": "https://localhost:8443/automation-api/run/job/workbench:00002/log"
    },
    {
      "jobId": "workbench:00003",
      "folderId": "workbench:00001",
      "numberOfRuns": 0,
      "name": "EndJob",
      "folder": "TestFolderAutomationAPI",
      "type": "Command",
      "status": "Wait Condition",
      "held": false,
      "deleted": false,
      "cyclic": false,
      "startTime": "",
      "endTime": "",
      "estimatedStartTime": [
        "20231002114920"
      ],
      "estimatedEndTime": [
        "20231002115420"
      ],
      "orderDate": "231002",
      "ctm": "workbench",
      "description": "",
      "host": "workbench",
      "application": "",
      "subApplication": "",
      "outputURI": "Job did not run, it has no output",
      "logURI": "https://localhost:8443/automation-api/run/job/workbench:00003/log"
    }
  ],
  "startIndex": 0,
  "itemsPerPage": 25,
  "total": 3,
  "monitorPageURI": "https://localhost:8443/ControlM/Monitoring/Viewpoints/Viewpoint?selDef=0000000100030014CONTROL-M%2520Name0004LIKE0009workbench0008ORDER_ID0005ILIKE001700001,00002,000030011DELETE_FLAG0004LIKE0005False"
}
```

#### Step 5 - View job details through an interactive interface
Control-M Workbench offers an interactive user interface for debugging purposes. Through this interface, you can view various job run details (including, for example, an activity log and statistics for each job). To launch this interface when you run jobs, enter "--interactive" or "-i" at the end of the [run](https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_Services_RunService.htm)  command.
```
> ctm run AutomationAPISampleFlow.json --interactive
{
  "runId": "2d17f02b-196b-4855-9b27-6e1e7e434f7b",
  "statusURI": "https://localhost:8443/automation-api/run/status/2d17f02b-196b-4855-9b27-6e1e7e434f7b",
  "monitorPageURI": "https://localhost:8443/ControlM/Monitoring/Viewpoints/Viewpoint?selDef=0000000100030014CONTROL-M%2520Name0004LIKE0009workbench0008ORDER_ID0005ILIKE001700007,00008,000090011DELETE_FLAG0004LIKE0005False"
}
```
A browser window opens, where you can view and manage your jobs.

### Example of Errors in Automation-API
> Responses (depending on the type of request)

<table>
<tr>
  <td> <b>Code</b> </td> 
  <td> <b>Description</b> </td>
</tr>
<tr>
  <td> 400 </td>
  <td>

  Bad Request
  ```json
  {
    "errors": [
     {
      "message": "string",
      "id": "string",
      "item": "string",
      "file": "string",
      "line": 0,
      "col": 0
     }
  ]
}
  ```

  </td>
</tr>
<tr>
  <td> 500 </td>
  <td>

  Unexpected Internal error
  ```json
  {
    "errors": [
     {
      "message": "string",
      "id": "string",
      "item": "string",
      "file": "string",
      "line": 0,
      "col": 0
     }
  ]
}
  ```

  </td>
</tr>
</table>

### Where to go from here
- To learn more about what you can do with the Control-M Automation API, read through the [Code Reference](https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_CodeRef_Main.htm) and [Automation API Services](https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_Services_Main.htm).  
- Proceed to the next tutorial, where you will learn how to [automate code deployments](https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_Tutorials_Automating_Code_Deployment.htm).
_________________________________

### Deploying an Application Integrator Plugin (version 9.21.100 and above)

From Control-M Workbench version 9.21.100, you can use the Control-M Automation API to deploy Application Integrator files (.ctmai). 

To deploy with the Control-M Automation API CLI uses the following command:
```
ctm deploy jobtype yourfile.ctmai workbench workbench
```
To learn more about Deploying an Application Integrator Plugin, read through the [Code Reference](https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_Services_DeployService.htm#deploy).

### Importing definitions into Control-M Workbench (version 9.21.100 and above)
From Control-M Workbench version 9.21.100, the `workbench::import` API allows you to modify existing job workflows in Control-M by importing them into Workbench where they can be work on locally. This API imports a zip file that contains definitions files into the workbench container. The definitions files can contain jobs, connection profiles, calendars, site standards (.json files), and Application Integrator plugins (.ctmai files).

Note: The workbench import API only accepts zip files. You can package all necessary files and folders into a zip file using the program of your choice or with the `package` service from the Control-M Automation API CLI

To import multiple definitions files with the Control-M Automation API CLI uses the following command:
```
ctm package resources.zip resourcesFolder/
ctm deploy workbench::import resources.zip
```
Additional tutorials for Automation API are available [here](https://documents.bmc.com/supportu/API/Monthly/en-US/Documentation/API_Services_DeployService.htm#deploy6).

### Using with external agents
External agents in Control-M play a crucial role in automating workflows in diverse IT setups. </br>
They allow Control-M to work on various machines, making it a versatile solution for automating tasks across the entire enterprise. </br>
Connecting these external agents to the Control-M Server is a standard method to enhance the capabilities and flexibility of workload automation in a diverse IT environment.

> For example, external agents in cloud environments (AWS, Azure, or Google) enable the automation of tasks, job scheduling, and data processing in the cloud as part of a hybrid or multi-cloud strategy.

To connect one or more external agents to Control-M Workbench, you need to expose the server to agent ports and add the hostnames of the agent machine in the docker command:

```
docker run --hostname workbench  -dt \
    -p 8443:8443 \
    -p <port1>:<port1> \
    -p <port2>:<port2> \
    --add-host "<hostname1>:<ip1>" \
    --add-host "<hostname2>:<ip2>" \
    controlm/workbench:latest
```
Example: 

If you are connecting an agent on a machine with ip: `192.168.0.2` with the hostname `agent` and want to define the server to agent port as 7005, the command is:

```
docker run \
    --hostname workbench  -dt \
    -p 8443:8443 \
    -p 7005:7005 \
    --add-host "agent:192.168.0.2" \
    controlm/workbench:latest
```

## Image details

Control-M Workbench is released every month at the same time as Control-M Automation API. The image contains the latest Control-M Automation API version and is versioned according to the Automation API. 

The version of Control-M/EM in the Control-M Workbench is 9.0.21.100

In addition, the Control-M Workbench includes all released [Integrations](https://docs.bmc.com/docs/ctm_integrations/control-m-integrations-home-994589883.html) at the moment of the image's release.

## Troubleshooting

The Control-M Workbench image is built in a pipeline that performs automatic tests before release. Our image is tested in Linux using Docker version 19.03.4 with 8GB allocated to the container. If you are experiencing issues, check the following:

- There is enough free memory for the container: Control-M Workbench requires a container with at least 8GB of memory. Note that this refers to the container and not the host machine. A machine with 8GB of memory may prove insufficient to run the container properly.

- Ports are free and communication is not blocked by a firewall

- On Windows: Running on Windows is possible with [WSL](https://docs.docker.com/desktop/windows/wsl/). For Docker Desktop users: Ensure that you are allocating enough memory to the container.

Control-M Workbench is meant to be used as an ephemeral environment. Although it is possible to leave it on for a long time, this is not the goal of the workbench; troubleshooting often requires restarting the container. 

Note that there is no persistence of jobs and other definitions. We work according to the Job-as-Code approach. All the jobs and other definitions should be saved as code outside of the Control-M Workbench container. 

Currently, the Change Password option <b>must not be used</b>.
If you change the password and lose access to the Workbench Web interface, re-upload the image to regain access to the Workbench.
regain access to the Workbench. The default password is restored.

If you are experiencing any issues using Control-M Workbench after having performed the troubleshooting described as above, open an [issue](https://github.com/controlm/workbench/issues).


## License

Please read the [Control-M Workbench License](https://aapi-swagger-doc.s3.us-west-2.amazonaws.com/workbench-license/Control-M+Workbench+Terms+of+Use+v07.06.2023+final.pdf) before pulling and using the docker image
