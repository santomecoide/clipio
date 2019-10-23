ACCEPTED_TYPES = [
    {'name': 'string', 'default': '', 'py_type': str},
    {'name': 'integer', 'default': 0, 'py_type': int},
    {'name': 'number', 'default': 0.0, 'py_type': float},
    {'name': 'boolean', 'default': False, 'py_type': bool}
]

data = "hola"
data_cast = ACCEPTED_TYPES[1]['py_type'](data)
print(data_cast)
print(type(data_cast))
