
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from dotenv import load_dotenv
from database.comet import Comet
import pandas as pd
load_dotenv()
header_key = os.getenv("ROSTERKEY")
# Create your views here.

@csrf_exempt
def iterationView(request):
    try:
        header_key = request.headers["x-api-key"]
        if request.method == "GET":
            version = request.GET.get("version")
            comet = Comet(version)
            comet.cloud_connect()
            reporter_key = comet.retrieve("reporter_key").iloc[0]["key"]
            if header_key == reporter_key:
                username = request.GET.get("username")
                final = comet.retrieve_iterations(username).round(decimals=2)
                comet.disconnect()
                if final.index.size > 0:
                    final["date"] = pd.to_datetime(final["date"])
                    final.sort_values("date",inplace=True)
                    final["value"] = [str(x) for x in final["value"]] 
                    final["conservative"] = [str(x) for x in final["conservative"]]  
                    complete = final[[x for x in final.columns if x not in ["fee","minimum_rows","live"]]].iloc[::-1].head(10).to_dict("records")
                else:
                    complete = []
            else:
                complete = {"error":"incorrect_key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            complete = {}
        else:
            complete = {}
    except Exception as e:
        complete = {}
        print(str(e))
    return JsonResponse(complete,safe=False)

@csrf_exempt
def orderView(request):
    try:
        header_key = request.headers["x-api-key"]
        if request.method == "GET":
            version = request.GET.get("version")
            username = request.GET.get("username")
            comet = Comet(version)
            comet.cloud_connect()
            reporter_key = comet.retrieve("reporter_key").iloc[0]["key"]
            if header_key == reporter_key:
                buys = comet.retrieve_completed_buys(username).round(decimals=2)
                sells = comet.retrieve_completed_sells(username).round(decimals=2)
                pending_buys = comet.retrieve_pending_buys(username).round(decimals=2)
                pending_sells = comet.retrieve_pending_sells(username).round(decimals=2)
                pending_buys["status"] = "pending"
                pending_sells["status"] = "pending"
                if pending_buys.index.size >0:
                    pending_buys["order_id"] = pending_buys["id"]
                if pending_sells.index.size > 0:
                    pending_sells["order_id"] = pending_sells["id"]
                buys["status"] = "complete"
                sells["status"] = "complete"
                final = pd.concat([buys,sells,pending_buys,pending_sells])
                if final.index.size > 0:
                    final = final.groupby(["product_id","order_id","status","side"]).agg({"created_at":"first","price": "mean", "size": "sum"}).reset_index()
                    final["created_at"] = pd.to_datetime(final["created_at"])
                    final.sort_values("created_at",inplace=True)
                    final["created_at"] = [str(x).split(".")[0] for x in final["created_at"]]
                    final["order_id"] = [str(x).split("-")[0] for x in final["order_id"]]
                    complete = final[[x for x in final.columns if x != "order_id"]].round(decimals=4).iloc[::-1].head(10).to_dict("records")
                else:
                    complete = []
            else:
                complete = {"error":"incorrect_key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            complete = {}
        else:
            complete = {}
    except Exception as e:
        complete = {}
        print(str(e))
    return JsonResponse(complete,safe=False)

@csrf_exempt
def tradeView(request):
    try:
        if request.method == "GET":
            version = request.GET.get("version")
            username = request.GET.get("username")
            comet = Comet(version)
            comet.cloud_connect()
            reporter_key = comet.retrieve("reporter_key").iloc[0]["key"]
            if header_key == reporter_key:
                    trades = comet.retrieve_completed_trades(username).round(decimals=2)
                    pending_trades = comet.retrieve_pending_trades(username).round(decimals=2)
                    pending_trades["status"] = "pending"
                    trades["status"] = "complete"
                    final = pd.concat([trades,pending_trades])
                    if final.index.size > 0:
                        final["date"] = pd.to_datetime(final["date"])
                        final.sort_values("date",inplace=True)
                        final["date"] = [str(x).split(".")[0] for x in final["date"]]
                        complete = final[["date","product_id","status","sell_price","size","price"]].round(decimals=4).iloc[::-1].head(10).to_dict("records")
                    else:
                        complete = []
            else:
                complete = {"error":"incorrect_key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            complete = {}
        else:
            complete = {}
    except Exception as e:
        complete = {}
        print(str(e))
    return JsonResponse(complete,safe=False)