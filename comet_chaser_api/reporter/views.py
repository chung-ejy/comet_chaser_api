
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from database.comet import Comet
import os
from dotenv import load_dotenv
load_dotenv()
roster_key = os.getenv("ROSTERKEY")
comet = Comet()

# Create your views here.
@csrf_exempt
def reporterView(request):
    try:
        headers = {"Content-Type":"application/json"}
        headers["x-api-key"] = roster_key
        if request.method == "GET":
            version = request.GET.get("version")
            username = request.GET.get("username")
            data_request = request.GET.get("data_request")
            comet.cloud_connect()
            params = {
                "version":version,
                "username":username
            }
            results = requests.get(f"https://cometreporter.herokuapp.com/api/{data_request}/",headers=headers,params=params).json()["trade_params"]
            complete = {"data":results}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":

            info =json.loads(request.body.decode("utf-8"))["params"]
            info["key"] = roster_key
            info["start"] = info["start"].split("T")[0]
            info["end"] = info["end"].split("T")[0]
            params = json.dumps(info).encode("utf-8")
            results = requests.post(f"https://comethistorian.herokuapp.com/api/backtest/",headers=headers,data=params)
            complete = results.json()
        else:
            complete = {}
    except Exception as e:
        complete = {}
        print(str(e))
    return JsonResponse(complete,safe=False)