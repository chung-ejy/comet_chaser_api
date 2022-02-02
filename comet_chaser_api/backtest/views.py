
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
                comet_historian.store("backtest_request",pd.DataFrame([info]))
                prices = comet_historian.retrieve("alpha_prices")
                models = comet_historian.retrieve("alpha_models")
                prices = p.column_date_processing(prices)
                try:
                    trades = bt.backtest(start,end,info,prices,models)
                    analysis = []
                    for position in range(int(info["positions"])):
                        spot_trades = trades[trades["position"]==position]
                        if spot_trades.index.size > 0:
                            initial = 100 / int(info["positions"])
                            for delta in spot_trades["delta"]:
                                initial = initial * (1+delta)
                            spot_trades["hpr"] = spot_trades["sell_date"] - spot_trades["date"]
                            spot_trades["days"] = [x.days for x in spot_trades["hpr"]]
                            days = spot_trades["days"].mean()
                            analysis.append({"signal":info["signal"]
                                            ,"req":info["req"]
                                            ,"trades":spot_trades.index.size
                                            ,"pv":initial,"days":days
                                            ,"retrack_days":info["retrack_days"]
                                            ,"value":info["value"]
                                            ,"conservative":info["conservative"]
                                            ,"entry_strategy":info["entry_strategy"]
                                            ,"exit_strategy":info["exit_strategy"]
                                            ,"positions":info["positions"]
                                            ,"position":position
                                            ,"api":"alpha"
                                            })
                        else:
                            initial = 100 / int(info["positions"])
                            spot_trades["hpr"] = 0
                            days = 0
                            analysis.append({"signal":info["signal"]
                                            ,"req":info["req"]
                                            ,"trades":spot_trades.index.size
                                            ,"pv":initial,"days":days
                                            ,"retrack_days":info["retrack_days"]
                                            ,"value":info["value"]
                                            ,"conservative":info["conservative"]
                                            ,"entry_strategy":info["entry_strategy"]
                                            ,"exit_strategy":info["exit_strategy"]
                                            ,"positions":info["positions"]
                                            ,"position":position
                                            ,"api":"alpha"
                                            })
                    a = pd.DataFrame(analysis)
                    final_analysis = a.pivot_table(index=["api","conservative","value","entry_strategy","exit_strategy","signal","retrack_days","req","positions"],columns="position",values="pv").reset_index()
                    final_analysis.fillna(100 / int(info["positions"]),inplace=True)
                    final_analysis["pv"] = [sum([row[1][i] if i in row[1].keys() else 0 for i in range(info["positions"])]) for row in final_analysis.iterrows()]
                    complete = {"trades":trades.to_dict("records")
                    ,"analysis":final_analysis.to_dict("records")
                    }
                except Exception as e:
                    complete = {"trades":[],"errors":"no trades","analysis":[]}
            else:
                complete = {"trades":[],"errors":"incorrect key","analysis":[]}
        else:
            complete = {}
        comet_historian.disconnect()
    except Exception as e:
        complete = {"trades":[],"errors":str(e)}
    return JsonResponse(complete,safe=False)