# commands for dev2

commands = {
    'www': {
        'opcode': 'http://www/',
        'read': True,
        'write': False,
        'shng_type': 'str',
        'dev_type': 'raw',
        'read_cmd': '$C'
    },
    'ac': {
        'opcode': 'http://192.168.2.234/dump1090-fa/data/aircraft.json',
        'read': True,
        'write': False,
        'shng_type': 'dict',
        'dev_type': 'raw',
        'read_cmd': '$C'
    },
    'knx': {
        'opcode': 'http://192.168.2.231:8384/ws/items/d.stat.knx.last_data',
        'read': True,
        'write': False,
        'shng_type': 'str',
        'dev_type': 'raw',
        'read_cmd': '$C'
    },
    'lit': {
        'opcode': 'http://$P:host::$P:port:/ws/items/garage.licht',
        'read': True,
        'write': True,
        'shng_type': 'bool',
        'dev_type': 'shng_ws',
        'read_cmd': '$C',
        'write_cmd': '$C/$V',
        'read_data': {'dict': ['value']}
    }
}
