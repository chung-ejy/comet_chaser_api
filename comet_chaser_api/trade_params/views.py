from django.shortcuts import render
from django.http.response import JsonResponse
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from database.comet_roster import CometRoster
import os
from dotenv import load_dotenv
load_dotenv()
header_key = os.getenv("HISTORIANKEY")
comet_roster = CometRoster()
@csrf_exempt
def tradeParamsView(request):
    try:
        comet_roster.cloud_connect()
        key = comet_roster.retrieve("roster_key").iloc[0]["key"]
        if request.method == "GET":
            user = request.GET.get("username")
            version = request.GET.get("version")
            data_request = request.GET.get("data_request")
            if key == header_key:
                if data_request == "user":
                    trade_params = comet_roster.get_user_trade_params(version,user)
                    trade_params["date"] = pd.to_datetime(trade_params["date"])
                    trade_params.sort_values("date",ascending=False,inplace=True)
                    results = trade_params.to_dict("records")[0]
                    results["value"] = str(results["value"])
                    results["conservative"] = str(results["conservative"])
                    complete = {k:results[k] for k in results.keys() if k not in ["pv","days","trades","date","username","version","sleep_time"]}
                else:
                    trade_params = comet_roster.retrieve(f"{version}_trading_params")
                    complete = {"trade_params":trade_params.to_dict("records")}
            else:
                complete = {"trade_params":{},"errors":"incorrect key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            info = json.loads(request.body.decode("utf-8"))["params"]
            version = info["version"]
            info["date"] = datetime.now()
            comet_roster.store(f"{version}_trading_params",pd.DataFrame([info]))
            complete = info
        else:
            complete = {}
        comet_roster.disconnect()
    except Exception as e:
        complete = {"roster":[],"errors":str(e)}
    return JsonResponse(complete,safe=False)