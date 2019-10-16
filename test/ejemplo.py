from tinydb import TinyDB
from tinydb import Query

def your_operation(your_arguments):
    def transform(doc):
        doc["properties"]["state"]["const"] = your_arguments
    return transform

User = Query()
eca_db = TinyDB("ecadb.json")
eca_db.update(your_operation(0), Query().id == 1)

print(eca_db.all())