
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from datetime import date, timedelta, datetime
from base64 import b64encode
class Paypal(object):
    def __init__(self,live):
        self.live = live
        self.base_url = "https://api-m.sandbox.paypal.com/v1/"

    def get_token(self,client_id,secret):
        auth=HTTPBasicAuth(client_id, secret)
        headers = {
            "Accept": "application/json",
        }
        data ={
            "grant_type":"client_credentials"
        }
        url =  f"{self.base_url}oauth2/token"
        r = requests.post(url,headers=headers,auth=auth,data=data)
        return r.json()["access_token"]

    def activate_subscription(self,client_id,secret,sub_id):
        token = str(self.get_token(client_id,secret))
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        url =  f"{self.base_url}billing/subscriptions/{sub_id}/activate"
        data = {
            "reason": "Reactivating the subscription"
                }
        r = requests.post(url,headers=headers,params=data)
        return r

    def cancel_subscription(self,client_id,secret,sub_id):
        token = self.get_token(client_id,secret)
        print(token)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        data = {
            "reason": "Dissatisfied with service"
            }
        url =  f"{self.base_url}billing/subscriptions/{sub_id}/cancel"
        print(url)
        print(headers)
        r = requests.post(url, headers=headers,params=data)
        return r