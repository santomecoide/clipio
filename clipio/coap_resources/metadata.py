import json
from coapthon.resources.resource import Resource

class Metadata(Resource):
    def __init__(self, name="metadata"):
        super(Metadata, self).__init__(name)
        self.payload = "Metadata Resource"

    def render_GET(self, request):
        with open('metadata.json') as fp:
            data = json.load(fp)
            self.payload = str(data)
            return self