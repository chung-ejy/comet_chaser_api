
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from dotenv import load_dotenv
load_dotenv()
roster_key = os.getenv("ROSTERKEY")

# Create your views here.
@csrf_exempt
def rosterView(request):
    try:
        headers = {"Content-Type":"application/json"}
        headers["x-api-key"] = roster_key
        if request.method == "GET":
            version = request.GET.get("version")
            username = request.GET.get("username")
            data_request = request.GET.get("data_request")
            params = {
                "version":version,
                "username":username
            }
            if data_request == "trade_params":
                results = requests.get(f"https://cometroster.herokuapp.com/api/trade_params/",headers=headers,params=params).json()["trade_params"]
                results["value"] = str(results["value"])
                results["conservative"] = str(results["conservative"])
                complete = {k:results[k] for k in results.keys() if k not in ["pv","days","trades","date","username","version","sleep_time"]}
            elif data_request == "bot_status":
                params["data_request"] = data_request
                results = requests.get(f"https://cometroster.herokuapp.com/api/roster/",headers=headers,params=params)
                complete = results.json()
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "PUT":
            info =json.loads(request.body.decode("utf-8"))["params"]
            params = json.dumps(info).encode("utf-8")
            results = requests.put(f"https://cometroster.herokuapp.com/api/roster/",headers=headers,data=params).json()
            complete = results
        elif request.method == "POST":
            info =json.loads(request.body.decode("utf-8"))["params"]
            params = json.dumps(info).encode("utf-8")
            results = requests.post(f"https://cometroster.herokuapp.com/api/trade_params/",headers=headers,data=params).json()
            complete = info
        else:
            complete = {}
    except Exception as e:
        complete = {}
        print(str(e))
    return JsonResponse(complete,safe=False)