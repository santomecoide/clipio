from datetime import datetime
import ast

from tinydb import TinyDB, Query
from coapthon.resources.resource import Resource

class UpdateEcaState(Resource):
    def __init__(self, name="update_eca_state"):
        super(UpdateEcaState, self).__init__(name)
        self.payload = "Uodate Eca State Resource"

    def __update_state(self, state):
        def transform(doc):
            doc["properties"]["state"]["const"] = state
            doc["modified"] = str(datetime.now())
        return transform

    def render_PUT(self, request):
        eca_db = TinyDB("ecadb.json")
        
        data = ast.literal_eval(request.payload)
        eca_db.update(
            self.__update_state(data["state"]), 
            Query().id == data["id"]
        )
        
        eca_db.close()
        return self