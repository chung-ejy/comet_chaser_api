from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http.response import JsonResponse
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from database.comet_historian import CometHistorian
from comet_utils.analyzer.entry_strategy import EntryStrategy as entry_strat
from comet_utils.analyzer.exit_strategy import ExitStrategy as exit_strat
from comet_utils.processor.processor import Processor as p
import os
from dotenv import load_dotenv
load_dotenv()
comet_historian = CometHistorian()

@csrf_exempt
def analysisView(request):
    try:
        comet_historian.cloud_connect()
        key = comet_historian.retrieve("historian_key").iloc[0]["key"]
        if request.method == "GET":
            complete = {}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            info = json.loads(request.body.decode("utf-8"))
            if info["key"] == key:
                merged = info["data"]
                side = info["side"]
                if side == "exit":
                    order = info["order"]
                    req = float(info["req"] / 100)
                    exit_strategy = info["exit_strategy"]
                    rec = exit_strat.exit_analysis(exit_strategy,order,pd.DataFrame(merged),req)
                    complete = {"rec":rec}
                elif side == "entry":
                    signal = float(info["signal"] / 100)
                    value = info["value"]
                    conservative = info["conservative"]
                    entry_strategy = info["entry_strategy"]
                    rec = entry_strat.entry_analysis(entry_strategy,pd.DataFrame(merged),signal,value,conservative)
                    complete = {"rec":rec.drop("_id",axis=1,errors="ignore").to_dict("records")}
            else:
                complete = {"rec":{},"errors":"incorrect key"}
        else:
            complete = {}
        comet_historian.disconnect()
    except Exception as e:
        complete = {"rec":{},"errors":str(e)}
        print(str(e))
    return JsonResponse(complete,safe=False)