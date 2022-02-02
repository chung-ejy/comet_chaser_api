from database.adatabase import ADatabase
import pandas as pd

class CometHistorian(ADatabase):
    
    def __init__(self):
        super().__init__("comet_historian")
    
    def get_symbols(self,api):
        try:
            db = self.client[self.name]
            table = db[f"{api}_prices"]
            data = table.find({}).distinct("crypto")
            return list(data)
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def retrieve_model(self,symbol):
        try:
            db = self.client[self.name]
            table = db[f"coinbase_models"]
            data = table.find({"symbol":symbol},{})
            return list(data)
        except Exception as e:
            print(self.name,"fills",str(e))