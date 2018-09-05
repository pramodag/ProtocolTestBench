from IPValidatorImpl import *
from OPValidatorImpl import *
from ProtocolImpl import *


class ProtocolFactory():
    def getProtocolImplementation(self, protocolName):
        print("Retriving protocol implementation class: "+str(protocolName))
        if protocolName in globals():
            # targetclass = protocolName.capitalize()
            return globals()[protocolName]()
        elif protocolName in locals():
            targetclass = protocolName.capitalize()
            return locals()[targetclass]()
        else:
            print("No calss definition found for class name: "+protocolName)
            return None

class IPValidatorFactory():
    def getIPValidatorImplementation(self, validatorName):
        print("Retriving input validator class: "+validatorName)
        if validatorName in globals():
            # targetclass = validatorName.capitalize()
            return globals()[validatorName]()

        elif validatorName in locals():
            targetclass = validatorName.capitalize()
            return locals()[targetclass]()
            
        else:
            print("No calss definition found for class name: "+validatorName)
            return None

class OPValidatorFactory():
    def getOPValidatorImplementation(self, validatorName):
        print("Retriving output validator class: "+validatorName)
        if validatorName in globals():
            # targetclass = validatorName.capitalize()
            return globals()[validatorName]()

        elif validatorName in locals():
            # targetclass = validatorName.capitalize()
            return locals()[validatorName]()
            
        else:
            print("No calss definition found for class name: "+validatorName)
            return None