
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from dotenv import load_dotenv
load_dotenv()
historian_key = os.getenv("HISTORIANKEY")

# Create your views here.
@csrf_exempt
def backtestView(request):
    try:
        if request.method == "GET":
            headers = {"Content-Type":"application/json"}
            headers["x-api-key"] = historian_key
            results = requests.get(f"https://comethistorian.herokuapp.com/api/backtest/",headers=headers)
            complete = results.json()
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            headers = {"Content-Type":"application/json"}
            headers["x-api-key"] = historian_key
            info =json.loads(request.body.decode("utf-8"))["params"]
            info["key"] = historian_key
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