from coapthon.resources.resource import Resource
from semantic_index import SemanticIndex

class Context(Resource):
    def __init__(self, name="context"):
        super(Context, self).__init__(name)
        self.payload = "Context Resource"

        self.__si = SemanticIndex(load_graph=False)
        self.__si.load()

    def render_POST(self, request):
        return self