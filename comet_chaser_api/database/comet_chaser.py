from database.adatabase import ADatabase
import pandas as pd
class CometChaser(ADatabase):
    
    def __init__(self):
        super().__init__("comet_chaser")
    
    def retrieve_users(self,params):
        try:
            db = self.client[self.name]
            table = db["users"]
            data = table.find(params,{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))