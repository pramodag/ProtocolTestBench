import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu, modbus_tcp
from abc import ABCMeta, abstractmethod


class AbstractProtocolImpl(metaclass=ABCMeta):
    '''This is the base class for all communication protocol implementation. All classes which handle 
        the communication has to extend this class else new object can not be created using factory.'''

    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def request(self):
        pass

class ModbusRTUServer(AbstractProtocolImpl):
    '''This is an implementation class for Modbus RTU protocol'''

    def __init__(self, baudrate=9600, byteRequest=8, parity='N', stopbits=1, xonxoff=0, timeout=5.0):
        self.baudrate = baudrate
        self.bytesize = byteRequest
        self.parity = parity
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.timeout = timeout
        self.typeLenDict = {'type16': 2, 'type32': 1}

    def connect(self, port, slaveId):
        self.slaveId = slaveId
        logger = modbus_tk.utils.create_logger("console")
        # Connect to the slave
        master = modbus_rtu.RtuMaster(serial.Serial(
            port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.xonxoff))
        master.set_timeout(self.timeout)
        master.set_verbose(True)
        self.master = master
        logger.info("connected")
        return master

    def request(self, address, registerType, noOfReg, value, access="RO"):
        if(self.master is None):
            raise ConnectionError(
                "No ModbusRTU master found. Use connect method before request")

        if(noOfReg == 0 and registerType == ""):
            raise ValueError(
                "Number of registers and registers type both can not be empty. Either of them is required.")

        if(noOfReg == 0):
            noOfReg = self.typeLenDict[registerType]

        if(access == "RO"):
            return self.master.execute(self.slaveId, cst.READ_HOLDING_REGISTERS, address, noOfReg)

        if(access == "RW"):
            if(noOfReg == 1):
                return self.master.execute(self.slaveId, cst.WRITE_SINGLE_REGISTER, address, value)
            elif(noOfReg > 1):
                return self.master.execute(self.slaveId, cst.WRITE_MULTIPLE_REGISTERS, address, noOfReg, value)
            else:
                raise(ValueError("Ilegal value for number of registers"))


class ModbusTCPMaster(AbstractProtocolImpl):
    '''This is an implementation class for Modbus RTU protocol'''

    def __init__(self):
        pass

    def connect(self, ip="localhost", port=502, timeout_in_sec=5.0):
        logger = modbus_tk.utils.create_logger("console")
        # Connect to the slave
        master=modbus_tcp.TcpMaster(host=ip, port=port, timeout_in_sec=timeout_in_sec  )
        master.set_verbose(True)
        self.master = master
        logger.info("connected")
        return True

    def request(self, **kwargs ):
        #assiging arguments from calling function
        address=kwargs['address']
        value=kwargs.get('value')
        length=kwargs.get('len')
        access=kwargs.get('access')
        print("arguments address:"+str(address)+" len:"+str(length)+" acess:"+access)
        if(self.master is None):
            raise ConnectionError(
                "No ModbusTCP master found. Use connect method before request")

        if(access == "r"):
            return self.master.execute(1, cst.READ_HOLDING_REGISTERS, int(address)-1, int(length) )

        if(access == "rw"):
            if(value is None):
                return self.master.execute(1, cst.READ_HOLDING_REGISTERS, int(address)-1, int(length) )
            else:
                if(length == 1):
                    return self.master.execute(1, cst.WRITE_SINGLE_REGISTER, int(address)-1, int(value) )
                elif(length > 1):
                    return self.master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, int(address)-1, int(value) )
                else:
                    raise(ValueError("Ilegal value for number of registers"))
