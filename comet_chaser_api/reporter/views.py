
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
def reporterView(request):
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
            results = requests.get(f"https://cometreporter.herokuapp.com/api/{data_request}/",headers=headers,params=params).json()
            complete = {"data":results}
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