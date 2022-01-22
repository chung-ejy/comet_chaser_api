from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http.response import JsonResponse
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from database.comet import Comet
import os
from dotenv import load_dotenv
load_dotenv()
comet = Comet()

@csrf_exempt
def liveView(request):
    try:
        if request.method == "GET":
            params = request.GET.get("data_request")
            comet.cloud_connect()
            if params == "trade_params":
                final = comet.retrieve("cloud_trading_params").round(decimals=2)
                final["value"] = [str(x) for x in final["value"]]
                final["conservative"] = [str(x) for x in final["conservative"]]
                complete = final[[x for x in final.columns if x not in ["pv","days","trades"]]].to_dict("records")
            elif params == "historicals":    
                final = comet.retrieve(f"cloud_{params}").round(decimals=2)[["time","crypto","signal","velocity","inflection","p_sign_change","price","bid","ask"]]
                final["time"] = pd.to_datetime(final["time"])
                final.sort_values("time",inplace=True)
                final["time"] = [str(x).split(".")[0] for x in final["time"]]
                final["p_sign_change"] = [str(x) for x in final["p_sign_change"]]
                complete = final.iloc[::-1].head(10).to_dict("records")
            elif params == "iterations":    
                final = comet.retrieve(f"cloud_{params}").round(decimals=2)
                final["date"] = pd.to_datetime(final["date"])
                final.sort_values("date",inplace=True)
                final["live"] = [str(x) for x in final["live"]]
                final["value"] = [str(x) for x in final["value"]] 
                final["conservative"] = [str(x) for x in final["conservative"]]  
                complete = final[[x for x in final.columns if x not in ["fee","minimum_rows","live"]]].iloc[::-1].head(10).to_dict("records")
            elif params == "errors":    
                final = comet.retrieve(f"cloud_{params}").round(decimals=2)
                complete = final[["date","status","message"]].iloc[::-1].head(10).to_dict("records")
            elif params == "all_orders":
                buys = comet.retrieve("cloud_completed_buys").round(decimals=2)
                sells = comet.retrieve("cloud_completed_sells").round(decimals=2)
                pending_buys = comet.retrieve("cloud_pending_buys").round(decimals=2)
                pending_sells = comet.retrieve("cloud_pending_sells").round(decimals=2)
                pending_buys["status"] = "pending"
                pending_sells["status"] = "pending"
                pending_buys["order_id"] = pending_buys["id"]
                if pending_sells.index.size > 0:
                    pending_sells["order_id"] = pending_sells["id"]
                buys["status"] = "complete"
                sells["status"] = "complete"
                final = pd.concat([buys,sells,pending_buys,pending_sells]).groupby(["product_id","order_id","status","side"]).agg({"created_at":"first","price": "mean", "size": "sum"}).reset_index()
                final["created_at"] = pd.to_datetime(final["created_at"])
                final.sort_values("created_at",inplace=True)
                final["created_at"] = [str(x).split(".")[0] for x in final["created_at"]]
                final["order_id"] = [str(x).split("-")[0] for x in final["order_id"]]
                complete = final[[x for x in final.columns if x != "order_id"]].round(decimals=4).iloc[::-1].head(10).to_dict("records")
            elif params == "all_trades":
                try:
                    trades = comet.retrieve("cloud_completed_trades").round(decimals=2)
                    pending_trades = comet.retrieve("cloud_pending_trades").round(decimals=2)
                    pending_trades["status"] = "pending"
                    trades["status"] = "complete"
                    final = pd.concat([trades,pending_trades])
                    # .groupby(["product_id","order_id","sell_id","side"]).agg({"created_at":"first","price": "mean", "size": "sum"}).reset_index()
                    final["date"] = pd.to_datetime(final["date"])
                    final.sort_values("date",inplace=True)
                    final["date"] = [str(x).split(".")[0] for x in final["date"]]
                    complete = final[["date","product_id","status","sell_price","size","price"]].round(decimals=4).iloc[::-1].head(10).to_dict("records")
                except:
                    complete = [{}]
            else:
                complete = comet.retrieve(f"cloud_{params}").round(decimals=2).iloc[::-1].head(10).to_dict("records")
            comet.disconnect()
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