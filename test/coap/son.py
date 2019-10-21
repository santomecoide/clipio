from father import Father

class Son(Father):
    def __init__(self):
        super(Son, self).__init__("el nombre")

    def render_GET(self, request):
        data = {
            "primero": "hola k ase"
        }
        self.payload = str(data)
        print("hijo")
        return self