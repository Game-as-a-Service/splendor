from domain.resource import Resource

class ResourceUserCase(Resource):
    def __init__(self,data=None):
        super().__init__()
        if data:
            self.map_from_json(data)

    def map_from_json(self, json_data):
        self.diamond = json_data['diamond']
        self.sapphire = json_data['sapphire']
        self.emerald = json_data['emerald']
        self.ruby = json_data['ruby']
        self.onyx = json_data['onyx']
        self.gold = json_data['gold']
    
