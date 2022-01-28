from database.adatabase import ADatabase
import pandas as pd
class Comet(ADatabase):
    
    def __init__(self,version):
        super().__init__("comet")
        self.prefix = version
    

    def retrieve_fills(self,user):
        try:
            db = self.client[self.name]
            table = db[f"cloud_{self.prefix}_fills"]
            data = table.find({"username":user},{"_id":0},show_record_id=False).limit(10).sort("_id",-1)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def retrieve_completed_buys(self,user):
        try:
            db = self.client[self.name]
            table = db[f"cloud_{self.prefix}_completed_buys"]
            data = table.find({"username":user},{"_id":0},show_record_id=False).limit(10).sort("_id",-1)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def retrieve_pending_trades(self,user):
        try:
            db = self.client[self.name]
            table = db[f"cloud_{self.prefix}_pending_trades"]
            data = table.find({"username":user},{"_id":0},show_record_id=False).limit(10).sort("_id",-1)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))

    def retrieve_completed_trades(self,user):
        try:
            db = self.client[self.name]
            table = db[f"cloud_{self.prefix}_completed_trades"]
            data = table.find({"username":user},{"_id":0},show_record_id=False).limit(10).sort("_id",-1)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def retrieve_completed_sells(self,user):
        try:
            db = self.client[self.name]
            table = db[f"cloud_{self.prefix}_completed_sells"]
            data = table.find({"username":user},{"_id":0},show_record_id=False).limit(10).sort("_id",-1)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def retrieve_pending_sells(self,user):
        try:
            db = self.client[self.name]
            table = db[f"cloud_{self.prefix}_pending_sells"]
            data = table.find({"username":user},{"_id":0},show_record_id=False).limit(10).sort("_id",-1)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def retrieve_pending_buys(self,user):
        try:
            db = self.client[self.name]
            table = db[f"cloud_{self.prefix}_pending_buys"]
            data = table.find({"username":user},{"_id":0},show_record_id=False).limit(10).sort("_id",-1)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))

    def retrieve_historicals(self,user):
        try:
            db = self.client[self.name]
            table = db[f"cloud_{self.prefix}_historicals"]
            data = table.find({"username":user},{"_id":0},show_record_id=False).limit(10).sort("_id",-1)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def retrieve_iterations(self,user):
        try:
            db = self.client[self.name]
            table = db[f"cloud_{self.prefix}_iterations"]
            data = table.find({"username":user},{"_id":0},show_record_id=False).limit(10).sort("_id",-1)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def retrieve_errors(self,user):
        try:
            db = self.client[self.name]
            table = db[f"cloud_{self.prefix}_errors"]
            data = table.find({"username":user},{"_id":0},show_record_id=False).limit(10).sort("_id",-1)

            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))