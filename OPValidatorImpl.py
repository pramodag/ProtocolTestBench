import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from abc import ABCMeta, abstractmethod
from Util import convertFromBytes
import traceback


class AbstractOPValidatorImpl(metaclass=ABCMeta):
    '''This is the base class for all output validator implementation. All classes which handle
        the output validation has to extend this class else new object can not be created using factory.'''

    def __init__(self):
        pass

    @abstractmethod
    def validate(self, data):
        pass


class ModBusOPValidator(AbstractOPValidatorImpl):
    """This class accepts a json object with the input data and optput from the protocol and validate
    it ti determine if the test case is pass or fail."""

    def __validateDataEntry(self, d):
        """Validates the data and determins test case result.
        This assumes that the json data passed is validated and contains all the required fields.
        If there an any ambiguity the test case result is shown as NA"""
        if(d['access'] == 'r' or (d['access'] == 'rw' and d.get('input') is None)):
            if(d['output'] is None):
                return (d, False, "Output is Null")

            if('enum' in d['type'] or 'bitfield' in d['type'] or (d.get('range') is not None and isinstance(d.get('range'), dict))):
                op = convertFromBytes(d['output'], d['type'])
                d['convertedOP'] = op
                if(not (str(op) in d['range'].keys())):
                    return (d, False, "Response not in range of expected values")
                else:
                    return (d, True, "")
            # TODO: add support for multiple ranges
            if(d.get('range') is not None):
                op = convertFromBytes(d['output'], d['type'])
                d['convertedOP'] = op
                try:
                    rangeArry = str(d.get('range'))
                    rangeArry = rangeArry.split("...")
                    ceiling = float(rangeArry[1])
                    floor = float(rangeArry[0])
                except:
                    return (d, False, "Range format not supported")
                if(floor <= float(op) and float(op) <= ceiling):
                    return (d, True, "")
                else:
                    return (d, False, "Output not in expected range")
            # try data conversion
            try:
                op = convertFromBytes(d['output'], d['type'])
                d['convertedOP'] = op
                return (d, True, "")
            except Exception:
                d['convertedOP'] = None
                return (d, False, "response couldn't be converted to required format")
        elif(d['access'] == 'rw' and d.get('input') is not None):
            d['convertedOP'] = d.get('output')
            if(d["input"] == d["output"]):
                return (d, True, "")
            else:
                return (d, False, "Output is not same as input")
        else:
            d['convertedOP'] = None
            return (d, False, "Unknown error")

    def validate(self, data):
        newTestCases = dict()
        errorMessages = []
        for d in data:
            (tempdata, state, errorMessage) = self.__validateDataEntry(data[d])
            if(state is False):
                result = "Fail"
                errorMessages.append(errorMessage+" for id:"+str(d))
                tempdata['result'] = result
            else:
                tempdata['result'] = "Pass"
            newTestCases[d] = tempdata
        return(newTestCases, errorMessages)
