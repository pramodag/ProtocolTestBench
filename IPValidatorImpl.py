import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from abc import ABCMeta, abstractmethod
import constants as myc
from xml.dom.minidom import parse
import xml.dom.minidom
import Util


class AbstractIPValidatorImpl(metaclass=ABCMeta):
    """This is the base class for all output validator implementation. All classes which handle
    the output validation has to extend this class else new object can not be created using factory."""

    def __init__(self):
        pass

    @abstractmethod
    def validate(self, data):
        """Validates all the input configuration data for any configuration errors and if there are any config errors
        then it will return false with the errors"""
        pass


class ModBusIPValidator(AbstractIPValidatorImpl):
    """This class accepts a json object with the configuration data and validate it for any configuration errors"""

    def __validateDataEntry(self, d):
        """Validates single data entry. This is done to allow customization. If user wants to extend the implementation
        then they can just implement the required custom validations and pass the object to super class for remaining
        validations """

        # print("Type of D:" + str(type(d)))
        # Error conditions
        # if(d.get("id") == None):
        #     return (d, False, "ID can not be null")
        # Setting explicit defaults
        if(Util.isWhiteSpaceorNone(d.get("len")) or d.get("len") == 0):
            d["len"] = myc.dataTypeLength.get(
                d.get("type"))
        if(Util.isWhiteSpaceorNone(d.get("access"))):
            d["access"] = "r"
        # Checking for conditions
        if(Util.isWhiteSpaceorNone(d.get("address"))):
            return (d, False, "Address not mentioned")

        if(d.get("len", "") == "" or d.get("len") == 0):
            return (d, False, "Size not found for data type "+d.get("type", ""))

        if(d.get("type") == "enum" and Util.isWhiteSpaceorNone(d.get("range"))):
            return (d, False, "No range specified for enum type")

        if(not (d.get("access") == "r" or d.get("access") == "rw" or d.get("access") == "w")):
            return (d, False, "Invalied access type specified")

        if((d.get("access") == "w") and d.get("input") is None):
            return (d, False, "Input can not be null for write request")

        return(d, True, "")

    def validate(self, data):
        newTestCases = dict()
        errorMessages = []
        isValid = True
        for d in data:
            (tempdata, state, errorMessage) = self.__validateDataEntry(data[d])
            if(state is False):
                isValid = False
                errorMessages.append(errorMessage+" for id:"+str(d))
            newTestCases[d] = tempdata
        return(newTestCases, isValid, errorMessages)


class SunSpecIPValidator(AbstractIPValidatorImpl):
    """This class accepts a json object with the SunSpec protocl configuration data which contain module id and startting address
    and parses into tool specific format.
    """

    def __validateDataEntry(self, d):
        # print(str(d.get("sunspec_model_id")) +
        #       "    "+str(d.get("starting_address")))
        if(d.get("sunspec_model_id") == None or d.get("starting_address") == None):
            return(d, False, "starting_address and sunspec_model_id can not be empty")
        filePath = myc.SUNSPEC_MODULE_PATH + '/smdx_' + \
            '{:05}'.format(d["sunspec_model_id"])+'.xml'
        xmlDoc = xml.dom.minidom.parse(filePath)
        xmlElements = xmlDoc.documentElement
        model = xmlElements.getElementsByTagName("model")[0]
        stringPoints = xmlElements.getElementsByTagName(
            "strings")[0].getElementsByTagName("point")
        if(int(model.getAttribute("id")) == d["sunspec_model_id"]):
            points = model.getElementsByTagName("point")
            schema = {}
            for point in points:
                temp = {}
                temp['address'] = d["starting_address"] + \
                    int(str(point.getAttribute("offset")).strip())
                temp['type'] = point.getAttribute("type")
                temp['len'] = point.getAttribute("len")
                temp['mandatory'] = point.getAttribute("mandatory")
                temp['access'] = point.getAttribute("access")
                if(temp['type'] == 'enum16' or temp['type'] == 'enum32' or temp['type'] == 'bitfield16' or temp['type'] == 'bitfield32'):
                    symbols = point.getElementsByTagName("symbol")
                    range = {}
                    for s in symbols:
                        range[s.firstChild.nodeValue] = s.getAttribute('id')
                    temp['range'] = range

                for p in stringPoints:
                    if(p.getAttribute('id') == point.getAttribute("id")):
                        try:
                            temp['description'] = str(p.getElementsByTagName(
                                'description')[0].firstChild.nodeValue)
                        except:
                            temp['description'] = ""
                        try:
                            temp['label'] = str(p.getElementsByTagName(
                                'label')[0].firstChild.nodeValue)
                        except:
                            temp['label'] = ""
                schema[str(point.getAttribute("id"))] = temp

        else:
            return(d, False, "Module "+str(d["sunspec_model_id"])+" not found!!!")

        return(schema, True, "")

    def validate(self, data):
        newTestCases = dict()
        errorMessages = []
        isValid = True
        for d in data:
            if(data[d].get("sunspec_model_id") is not None):
                (tempdata, state, errorMessage) = self.__validateDataEntry(
                    data[d])
                if(state is False):
                    isValid = False
                    errorMessages.append(errorMessage+" for id:"+str(d))
                else:
                    for td in tempdata:
                        if(not (td in newTestCases) ):
                            newTestCases[td] = tempdata[td]
                    # newTestCases.update(tempdata)
            else:
                newTestCases[d] = data[d]
        modbusValidator = ModBusIPValidator()
        (validatedTestCases, isValid1, errMsgs) = modbusValidator.validate(newTestCases)
        if(not isValid or not isValid1):
            isValid = False
        return(validatedTestCases, isValid, errorMessages + errMsgs)
