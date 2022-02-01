
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from database.comet_historian import CometHistorian
from comet_utils.backtester.backtester import Backtester as bt
from comet_utils.processor.processor import Processor as p
load_dotenv()
header_key = os.getenv("HISTORIANKEY")
# Create your views here.
comet_historian = CometHistorian()
@csrf_exempt
def backtestView(request):
    try:
        comet_historian.cloud_connect()
        key = comet_historian.retrieve("historian_key").iloc[0]["key"]
        if request.method == "GET":
            if key == header_key:
                symbols = comet_historian.get_symbols("coinbase")
                complete = symbols
            else:
                complete = {"errors":"incorrect_key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            info = json.loads(request.body.decode("utf-8"))["params"]
            if header_key == key:
                start = datetime.strptime(info["start"].split("T")[0],"%Y-%m-%d")
                end = datetime.strptime(info["end"].split("T")[0],"%Y-%m-%d")
                for key in info.keys():
                    if key in ["req","signal","retrack_days","positions"]:
                        info[key] = int(info[key])
                comet_historian.cloud_connect()
                comet_historian.store("backtest_request",pd.DataFrame([info]))
                prices = comet_historian.retrieve("alpha_prices")
                prices = p.column_date_processing(prices)
                try:
                    trades = bt.backtest(start,end,info,prices)
                    complete = {"trades":trades.to_dict("records")
                    ,"analysis":[]
                    }
                except Exception as e:
                    complete = {"trades":[],"errors":"no trades"}
            else:
                complete = {"trades":[],"errors":"incorrect key"}
        else:
            complete = {}
        comet_historian.disconnect()
    except Exception as e:
        complete = {"trades":[],"errors":str(e)}
    return JsonResponse(complete,safe=False)