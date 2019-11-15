ACCEPTED_TYPES = [
    {'name': 'string', 'default': '', 'py_type': str},
    {'name': 'integer', 'default': 0, 'py_type': int},
    {'name': 'number', 'default': 0.0, 'py_type': float},
    {'name': 'boolean', 'default': 0, 'py_type': int}
]

ACCEPTED_QOS = [0, 1, 2]

ACCEPTED_PROTOCOLS = ['coap']

MIN_CRAWLER_DELAY_TIME = 60*60 #1h

METADATA_KEY_WORDS = ["name", "description", "title"]
URL_KEY_WORDS = ["href", "link"]

COAP_PORT = 5683

ACCEPTED_ONTOLOGIES_TAGS = ['home']

ONTOLOGY_QUERY = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?class ?label
    WHERE { 
        ?class a owl:Class .
        ?class rdfs:label ?label
        FILTER (lang(?label) = 'en')
    }
"""