
import pandas as pd
import requests
from datetime import date, timedelta, datetime
from comet_utils.coinbase.coinbase_wallet_auth import CoinbaseWalletAuth

class Coinbase(object):
    def __init__(self,live):
        self.live = True
        if self.live:
            self.base_url = "https://api.exchange.coinbase.com"
        else:
            self.base_url = "https://api-public.sandbox.exchange.coinbase.com"
        
    @classmethod
    def get_currencies(self,key,secret,passphrase):
        auth = CoinbaseWalletAuth(key, secret, passphrase)
        url =  f"{self.base_url}/products"
        r = requests.get(url,auth=auth)
        return r.json()

    @classmethod
    def get_current_price(self,key,secret,passphrase,crypto):
        auth = CoinbaseWalletAuth(key,secret,passphrase)
        product_id = f'{crypto}-USD'
        url =  f"{self.base_url}/products/{product_id}/ticker"
        r = requests.get(url, auth=auth)
        return r.json()
    
    @classmethod
    def get_timeframe_prices(self,key,secret,passphrase,crypto,start,end,timeframe):
        try:
            auth = CoinbaseWalletAuth(key,secret,passphrase)
            product_id = f'{crypto}-USD'
            start = end - timedelta(days=timeframe)
            url =  f"{self.base_url}/products/{product_id}/candles"            
            params = {"granularity":86400,
                     "start":start.strftime("%Y-%m-%d"),
                     "end":end.strftime("%Y-%m-%d")}
            r = requests.get(url, auth=auth,params=params)
            if len(r.json()) > 0:
                results = pd.DataFrame(r.json(),columns=["timestamp", "low", "high", "open", "close","volume"])
                results["date"] = [str(date.fromtimestamp(x)) for x in results["timestamp"]]
                results["crypto"] = crypto
                return results
            else:
                return pd.DataFrame([{}])
        except Exception as e:
            print(product_id,start,end,str(e))
            return product_id,start,end,str(e)

    @classmethod
    def get_prices(self,key,secret,passphrase,crypto,start,end):
        try:
            auth = CoinbaseWalletAuth(key,secret,passphrase)
            product_id = f'{crypto}-USD'
            url =  f"{self.base_url}/products/{product_id}/candles"            
            params = {"granularity":86400,
                     "start":start.strftime("%Y-%m-%d"),
                     "end":end.strftime("%Y-%m-%d")}
            r = requests.get(url, auth=auth,params=params)
            if len(r.json()) > 0:
                results = pd.DataFrame(r.json(),columns=["timestamp", "low", "high", "open", "close","volume"])
                results["date"] = [str(date.fromtimestamp(x)) for x in results["timestamp"]]
                results["crypto"] = crypto
                return results
            else:
                return pd.DataFrame([{}])
        except Exception as e:
            print(product_id,start,end,str(e))
            return product_id,start,end,str(e)
    
    @classmethod
    def get_accounts(self,key,secret,passphrase):
        try:
            auth = CoinbaseWalletAuth(key,secret,passphrase)
            api_url = "	https://api.exchange.coinbase.com/accounts"
            r = requests.get(api_url, auth=auth)
            results = pd.DataFrame(r.json())
            results["balance"] = results["balance"].astype(float)
            return results
        except Exception as e:
            print(str(e))
            return str(e)

    
    @classmethod
    def get_orders(self,key,secret,passphrase):
        try:
            auth = CoinbaseWalletAuth(key,secret,passphrase)
            url = "	https://api.exchange.coinbase.com/orders"
            params = {"sorting":"desc"
                    ,"status":"open"
                    ,"sortedBy":"created_at"
                    ,"limit":100}
            r = requests.get(url, auth=auth, params=params)
            results = pd.DataFrame(r.json())
            return results
        except Exception as e:
            print(str(e))
            return str(e)
    
    @classmethod
    def get_fill(self,key,secret,passphrase,crypto):
        try:
            auth = CoinbaseWalletAuth(key,secret,passphrase)
            url = "	https://api.exchange.coinbase.com/fills"
            product_id = f'{crypto}-USD'
            params = {
                # "sorting":"desc"
                #     ,"status":"pending"
                #     ,"sortedBy":"created_at"
                    "product_id":product_id,
                    "limit":100}
            r = requests.get(url, auth=auth, params=params)
            # results = pd.DataFrame(r.json())
            return r.json()
        except Exception as e:
            print(str(e))
            return str(e)
    @classmethod
    def create_fill_report(self,key,secret,passphrase,start,end):
        payload = {
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "type": "fills",
        "format": "csv",
        "product_id": "ALL"
        }
        url = f"{self.base_url}/reports"
        auth = CoinbaseWalletAuth(key,secret,passphrase)
        r = requests.post(url, auth=auth, json=payload)
        return r.json()
        
    @classmethod
    def get_fill_report(self,key,secret,passphrase):
        url = f"{self.base_url}/reports"
        auth = CoinbaseWalletAuth(key,secret,passphrase)
        params = {
                    "type":"fills",
                    "limit":100
                }
        r = requests.get(url, auth=auth, params=params)
        return r.json()
    
    @classmethod
    def place_buy(self,key,secret,passphrase,crypto,buy_price,size):
        auth = CoinbaseWalletAuth(key,secret,passphrase)
        url = "	https://api.exchange.coinbase.com/orders"
        product_id = f'{crypto}-USD'
        payload = {
            "product_id": product_id,
            "type": "limit",
            "side": "buy",
            "stp": "dc",
            "time_in_force": "GTC",
            "cancel_after": "day",
            "post_only": "false",
            "price":buy_price,
            "size":size
        }
        response = requests.post(url,auth=auth,json=payload)
        return response.json()
    
    @classmethod
    def cancel_order(self,key,secret,passphrase,order_id):
        auth = CoinbaseWalletAuth(key,secret,passphrase)
        url = "	https://api.exchange.coinbase.com/orders"
        params = {
            "order_id":order_id
        }
        response = requests.delete(url,auth=auth,params=params)
        return response

    @classmethod
    def place_sell(self,key,secret,passphrase,product_id,sell_price,size):
        auth = CoinbaseWalletAuth(key,secret,passphrase)
        url = "	https://api.exchange.coinbase.com/orders"
        payload = {
            "product_id": product_id,
            "type": "limit",
            "side": "sell",
            "stp": "dc",
            "time_in_force": "GTC",
            "cancel_after": "day",
            "post_only": "false",
            "price":round(sell_price,2),
            "size":round(size,6)
        }
        response = requests.post(url,auth=auth,json=payload)
        return response.json()