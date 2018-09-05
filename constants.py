SUNSPEC_MODULE_PATH = "./Model/smdx"
dataTypeLength = {'float': 1, 'float32': 2, 'float64': 4, 'int': 1, 'enum': 1, 'acc32': 2, 'acc64': 4, 'bitfield16': 1,
                  'bitfield32': 2, 'enum16': 1, 'int16': 1, 'int32': 2, 'sunssf': 1, 'uint16': 1, 'uint32': 2, 'uint64': 4, 'pad': 1}
conversionTable = {'uint16': 'H', 'sunssf': 'h', 'enum16': 'h', 'string': 's', 'str': 's',
                   'bitfield16': 'H', 'bitfield32': 'I', 'acc32': 'I', 'int16': 'h', 'pad': 'H'}
