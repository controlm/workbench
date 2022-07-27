# ================
# Simple code snippet to get started with Control-M Workbench
# and Control-M Python Client
# This code requires the python client library installed
# Check it on https://controlm.github.io/ctm-python-client/tutorials.html
# ================

from ctm_python_client.core.workflow import *
from aapi import *


workflow = Workflow.workbench()

jobs = workflow.chain([
    JobCommand('StartJob', 'echo "Hello"'),
    JobCommand('EndJob', 'echo "Bye"')
], inpath='TestFolderPythonClient')

# use open_in_browser to open automatically the Control-M Web Monitoring interface
run = workflow.run(open_in_browser=True)
