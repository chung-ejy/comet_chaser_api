
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from database.comet import Comet
import os
from dotenv import load_dotenv
load_dotenv()
historian_key = os.getenv("HISTORIANKEY")
comet = Comet()

# Create your views here.
@csrf_exempt
def backtestView(request):
    try:
        if request.method == "GET":
            params = request.GET.get("data_request")
            comet.cloud_connect()
            if params == "symbols":
                final = comet.retrieve_symbols()
                complete = {"symbols":list(final["crypto"].unique())}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            headers = {"Content-Type":"application/json"}
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