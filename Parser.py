'''A python script to parse the json configuration data, validate them and combine 
it into one big configuration file which can be used for testing.'''

import json
import os.path


def parse(SUTConfig, opPath):
   
    testCaseFiles = []
    for s in SUTConfig['header']['docLinks']:
        testCaseFiles.append(json.loads(open(s, "r").read(-1)))
    uniqueIds = set()
    # create a big set of all ids
    for obj in testCaseFiles:
        uniqueIds = uniqueIds.union(set(obj.keys()))
    # create them into a bigger json obj
    testCases = {}

    for id in uniqueIds:
        tempdict = {}
        for file in testCaseFiles:
            if(id in file.keys()):
                for k in file[id].keys():
                    tempdict[k] = file[id][k]
        testCases[id] = tempdict
    if(os.path.exists(opPath)):
        op = open(opPath+"/op.json", "w")
        op.write(json.dumps(testCases))
        op.close()
    else:
        print("OP path "+opPath+" dosen't exists. No data written to file")
    return testCases
