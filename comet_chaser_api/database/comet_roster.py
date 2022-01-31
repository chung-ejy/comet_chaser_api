from database.adatabase import ADatabase
import pandas as pd
from cryptography.fernet import Fernet
import os
header_key = os.getenv("ROSTERKEY")
encryption_key = os.getenv("ENCRYPTIONKEY")

class CometRoster(ADatabase):
    
    def __init__(self):
        super().__init__("comet_roster")
    
    def get_user_trade_params(self,version,user):
        try:
            db = self.client[self.name]
            table = db[f"{version}_trading_params"]
            data = table.find({"username":user},{"_id":0},show_record_id=False).limit(10)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"roster",str(e))
    
    def get_secrets(self,user):
        try:
            db = self.client[self.name]
            table = db["coinbase_credentials"]
            data = table.find({"username":user},{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"roster",str(e))
    
    def update_roster(self,user,params):
        try:
            db = self.client[self.name]
            table = db["roster"]
            data = table.update_one({"username":user},{"$set":params})
            return data
        except Exception as e:
            print(self.name,"roster",str(e))
    
    def update_keys(self,user,params):
        try:
            db = self.client[self.name]
            table = db["coinbase_credentials"]
            fernet = Fernet(encryption_key.encode())
            encoded_keys = {}
            for key in params.keys():
                if "key" in key or "secret" in key or "pass" in key:
                    encoded_keys[key] =  fernet.encrypt(params[key].encode())
            data = table.update_one({"username":user},{"$set":encoded_keys})
            return data
        except Exception as e:
            print(self.name,"roster",str(e))
    
    def update_subscription(self,user,params):
        try:
            db = self.client[self.name]
            table = db["paypal_subscriptions"]
            data = table.update_one({"username":user},{"$set":params})
            return data
        except Exception as e:
            print(self.name,"roster",str(e))
    
    def get_bot_status(self,user):
        try:
            db = self.client[self.name]
            table = db["roster"]
            data = table.find({"username":user},{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"roster",str(e))
    
    def get_subscription(self,user):
        try:
            db = self.client[self.name]
            table = db["paypal_subscriptions"]
            data = table.find({"username":user},{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"roster",str(e))
    
    def get_all_subscription(self):
        try:
            db = self.client[self.name]
            table = db["paypal_subscriptions"]
            data = table.find({},{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"roster",str(e))
    