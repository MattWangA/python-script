from resource.script import script
import os
import json
import  GenerateTopAPACCallsTemplate.main as main

@script.route('/')
def GenerateTopCalls():
    main.main()
