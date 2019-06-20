from resource.script import script
import os
import json


@script.route('/')
def GenerateTopCalls():
    os.system('scriptfile/GenerateTopCalls/GenerateTopCallsTemplate.bat')
    return json.dumps({"status":0,"data":"success"})