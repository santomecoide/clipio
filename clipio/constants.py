ACCEPTED_TYPES = [
    {'name': 'string', 'default': '', 'py_type': str},
    {'name': 'integer', 'default': 0, 'py_type': int},
    {'name': 'number', 'default': 0.0, 'py_type': float},
    {'name': 'boolean', 'default': 0, 'py_type': int}
]

ACCEPTED_PROTOCOLS = ['coap']
MIN_CRAWLER_DELAY_TIME = 60*60 #1h

ONTOLOGIES = {
    "home": "dogont"
}

METADATA_KEY_WORDS = ["name", "description", "title"]
URL_KEY_WORDS = ["href", "link"]

COAP_PORT = 5683