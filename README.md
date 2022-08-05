# Control-M Workbench Quickstart Guide

Control-M is a no-cost, self-service, standalone development environment that is launched in minutes, giving you the autonomy to code, debug, and test jobs in JSON or Python.

Control-M Workbench is published as [docker image](https://hub.docker.com/repository/docker/controlm/workbench). 

This repository contains examples of usages, a quickstart guide, and snippets you can use freely. They are provided as is, but we are open for contributions and issue reporting.

## Starting with Control-M Workbench


### Requirements

- Docker installed
- 8GB of free memory
- Free ports: 8443 + any other port used for external agent communication


To start a container run the docker command:
```
docker run -dt \
    -p 8443:8443 \
    --hostname=workbench \
    controlm/workbench:latest
```


### Using with external agents

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

If connecting an agent on a machine with ip: `192.168.0.2` with hostname `agent` and define the server to agent port as 7005, the command is:

```
docker run \
    --hostname workbench  -dt \
    -p 8443:8443 \
    -p 7005:7005 \
    --add-host "agent:192.168.0.2" \
    controlm/workbench:latest
```

## Using Control-M Workbench with Automation API

Control-M Workbench can be a handy tool to test jobs written in JSON using [Automation API](https://docs.bmc.com/docs/automation-api/monthly/tutorials-1116950277.html). You can either use the Automation API via curl, postman or any other REST client or use the Automation API cli. To define a workbench environment in the cli simply run the command:
```
ctm environment workbench::add
```
You can do a quickstart test using the [quickstart snippet](snippets/quickstart.json):

```
ctm environment set workbench
ctm run quickstart.json -i
```

You can check the tutorials of Automation API [here](https://docs.bmc.com/docs/ctmapimonthly/tutorials-1116950277.html)

## Using Control-M Workbench with Control-M Python Client

You can use the workbench to test your python workflows with the [ctm-python-client](https://github.com/controlm/ctm-python-client) library. To get started with a workflow for workbench simply create a workflow like this:
```python
workflow = Workflow.workbench()
```

You can do a quickstart test using the [quickstart snippet](snippets/quickstart.py):

```
python quickstart.py
```

You can check the tutorials of Control-M Python Client [here](https://controlm.github.io/ctm-python-client/tutorials.html)

## Troubleshooting

Control-M Workbench image is built in a pipeline which performs automatic tests before release. Our image is tested in Linux using Docker version 19.03.4 with 8GB allocated to the container. If you are experiencing issues, check the following:

- There is enough free memory for the container: Control-M Workbench requires a container with at least 8GB of memory, please note that this refers to the container and not the host machine. A machine with 8GB of memory may prove insufficient to run the container properly.

- Ports are free and communication is not blocked by firewall

- Note on Windows: Runing on Windows is possible with [WSL](https://docs.docker.com/desktop/windows/wsl/). For Docker Desktop users: Please make sure you are allocating enough memory to the container.

Control-M Workbench is meant to be used as an ephemeral environment. Although is possible to leave it on for long period of time, this is not the goal of workbench and troubleshooting often requires restarting the container. 

Note that there is no persistance of jobs and other definitions. We work according to the Job as Code approach. All the jobs and other definitions should be saved as code outside of the Control-M Workbench container. 

If you are experiencing any issues using Control-M Workbench after having done the troubleshooting described as above, open an [issue](https://github.com/controlm/workbench/issues).

## License

Please read the [Control-M Workbench License](https://aapi-swagger-doc.s3.us-west-2.amazonaws.com/workbench-license/Control-M+Workbench+Terms+of+Use+v.07.20.2022.pdf) before pulling and using the docker image
