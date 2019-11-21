ACCEPTED_TYPES = [
    {'name': 'string', 'default': '', 'py_type': str},
    {'name': 'integer', 'default': 0, 'py_type': int},
    {'name': 'number', 'default': 0.0, 'py_type': float},
    {'name': 'boolean', 'default': 0, 'py_type': int}
]
ACCEPTED_ONTOLOGIES_TAGS = ['home']
ACCEPTED_MQTT_QOS = [0, 1, 2]
ACCEPTED_CRAWLER_PROTOCOLS = ['coap']

MIN_CRAWLER_DELAY_TIME = 3600 #1h

DEFAULT_COAP_PORT = 5683

URL_KEY_WORDS = ["href", "link"]
METADATA_KEY_WORDS = ["name", "description", "title"]

ONTOLOGY_QUERY = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?class ?label
    WHERE { 
        ?class a owl:Class .
        ?class rdfs:label ?label
        FILTER (lang(?label) = 'en')
    }
"""

CONTEXT_DB_PATH = "generated/contextdb.json"
ECA_DB_PATH = "generated/ecadb.json"
METADATA_PATH = "generated/metadata.json"
COMPONENTS_PATH = "generated/components.json"