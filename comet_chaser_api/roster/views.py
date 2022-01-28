
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from database.comet_roster import CometRoster
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
comet_roster = CometRoster()
header_key = os.getenv("ROSTERKEY")
# Create your views here.
@csrf_exempt
def rosterView(request):
    try:
        comet_roster.cloud_connect()
        if request.method == "GET":
            version = request.GET.get("version")
            username = request.GET.get("username")
            data_request = request.GET.get("data_request")
            params = {
                "version":version,
                "username":username
            }
            if data_request == "bot_status":
                user = request.GET.get("username")
                bot_status = comet_roster.get_bot_status(user)
                complete = {"bot_status":bot_status.to_dict("records")[0]}
            else:
                complete = comet_roster.retrieve("roster").to_dict("records")
        elif request.method == "PUT":
            info =json.loads(request.body.decode("utf-8"))
            user = info["username"]
            if info["data_request"] == "keys":
                update = comet_roster.update_roster(user,info)
                info["acknowledge"] = update.acknowledged
                complete = info[["username","acknowledge"]]
            elif info["data_request"] == "bot_status":
                update = comet_roster.update_roster(user,info)
                info["acknowledge"] = update.acknowledged
                complete = info
        elif request.method == "POST":
            info =json.loads(request.body.decode("utf-8"))
            result = {}
            result["username"] = info["username"]
            result["live"] = False
            result["test"] = False
            keys = {}
            keys["username"] = info["username"]
            keys["apikey"] = ""
            keys["passphrase"] = ""
            keys["secret"] = ""
            keys["adnboxapikey"] = ""
            keys["sandboxpassphrase"] = ""
            keys["sandboxsecret"] = ""
            trade_params = {
                "signal":5
                ,"req":5
                ,"retrack_days":30
                ,"value":True,
                "conservative":False,
                "entry_strategy":"standard"
                ,"exit_strategy":"hold"
                ,"positions":5
                ,"username":info["username"]
                ,"version":"live"
                ,"whitelist_symbols":["BTC","ETH"]
                ,"date":datetime.now()
            }
            test_trade_params = {
                "signal":5
                ,"req":5
                ,"retrack_days":30
                ,"value":True,
                "conservative":False,
                "entry_strategy":"standard"
                ,"exit_strategy":"hold"
                ,"positions":5
                ,"username":info["username"]
                ,"version":"live"
                ,"whitelist_symbols":["BTC"]
                ,"date":datetime.now()
            }
            comet_roster.store("roster",pd.DataFrame([result]))
            comet_roster.store("coinbase_credentials",pd.DataFrame([keys]))
            comet_roster.store("live_trading_params",pd.DataFrame([trade_params]))
            comet_roster.store("test_trading_params",pd.DataFrame([test_trade_params]))
            complete = result
        else:
            complete = {}
        comet_roster.disconnect()
    except Exception as e:
        complete = {}
        print(str(e))
    return JsonResponse(complete,safe=False)