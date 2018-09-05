'''
This class acts as entry point to the application.
This will
    *Call parser to read and combine multiple json config files to one single testcase file(json)
    *get appropriate communication protocol implementation
    *execute testcases and store results
    *Evaluates the test cases and prints op
'''
from Parser import parse
import time
import sys
import json
import pickle
import webbrowser
import os.path
from Factory import ProtocolFactory, OPValidatorFactory, IPValidatorFactory
from Util import *

# from IPValidatorImpl import AbstractIPValidatorImpl

# Initialization and config stuff
protocolConfigFilePath = "./Model/Fronious_Spec.json"
protocolConfigFilePath = os.path.abspath(protocolConfigFilePath)
# read the config file for protocol info
protocolConfigFile = open(protocolConfigFilePath, "r")
SUTConfig = json.loads(protocolConfigFile.read(-1))
type(SUTConfig)
opPath = os.path.abspath(os.path.join(protocolConfigFilePath, os.pardir))
testcases = parse(SUTConfig, opPath)
print(type(testcases))
ipValFactory = IPValidatorFactory()
validator = ipValFactory.getIPValidatorImplementation(
    SUTConfig['header']['IPValidatorImplClass'])
(testcases, isValid, errormessages) = validator.validate(testcases)
op = open(opPath+"/op.json", "w")
op.write(json.dumps(testcases))
op.close()
if(isValid is False):
    for errMsg in errormessages:
        print(errMsg)
    sys.exit()
else:
    print("Input validation successfull")


protocolFactory = ProtocolFactory()
protocol = protocolFactory.getProtocolImplementation(
    str(SUTConfig['header']['ProtocolImplClass']))

print("connectionArguments:")
print(str(SUTConfig['header']['connection']))


kwargs = SUTConfig['header']['connection']
protocol.connect(**kwargs)
op = open("Model/validatedOP.json", "w")
for testcaseId in testcases:
    # request(self, address, value, size=1, access="RO"):
    testcase = testcases[testcaseId]
    #print(str(testcase['address']) +" "+str(testcase.get("value")) +" "+str(testcase.get('length')) +" "+str(testcase['access']))
    time1 = time.time()
    o_p = protocol.request(**testcase)
    time2 = time.time()
    testcases[testcaseId]['output'] = o_p
    testcases[testcaseId]['executionTime'] = round(time2-time1, 3)
    op.write(testcaseId+":"+str(o_p)+"\n")
op.close()
# op validator code

# print(testcases)

pickle.dumps(testcases)
opValidtorFactory = OPValidatorFactory()
opValidator = opValidtorFactory.getOPValidatorImplementation(
    str(SUTConfig['header']['OPValidatorClass']))
(testcases, OPerrormessages) = opValidator.validate(testcases)

for arg in testcases:
    print(str(testcases[arg].get('convertedOP')) + ": "+str(
        testcases[arg].get('result'))+" : "+str(testcases[arg].get('executionTime')))
# prepare output
table = []
for key in testcases.keys():
    table.append({'Id': key, 'Description': testcases.get(key).get('description'), 'Output': testcases.get(key).get(
        'convertedOP'), 'Result': testcases.get(key).get('result'), 'Execution Time': testcases.get(key).get('executionTime'), 'Address': testcases.get(key).get('address'),
        'Raw output': testcases.get(key).get('output')})

print("Error mesages:"+str(errormessages))

writeHTML(table, ['Id', 'Address', 'Description',
                  'Execution Time', 'Raw output', 'Output', 'Result'])

webbrowser.open('./Model/result.html')
