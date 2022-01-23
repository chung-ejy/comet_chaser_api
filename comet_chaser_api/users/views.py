
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from database.comet import Comet
import os
from database.comet_chaser import CometChaser
import bcrypt
import json
comet_chaser = CometChaser()
import binascii
import pandas as pd
# Create your views here.
@csrf_exempt
def registerView(request):
    try:
        if request.method == "GET":
            complete = {}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            comet_chaser.cloud_connect()
            info =json.loads(request.body.decode("utf-8"))
            result = {}
            result["username"] = info["username"]
            result["email"] = info["email"]
            existing_users = comet_chaser.retrieve_users(result)
            if existing_users.index.size > 0:
                complete = {"error":"user exists"}
            else:
                result["password"] = bcrypt.hashpw(info["password"].encode(),bcrypt.gensalt())
                result["token"] = binascii.hexlify(os.urandom(20)).decode()
                comet_chaser.store("users",pd.DataFrame([result]))
            comet_chaser.disconnect()
            complete = json.dumps(result)
        else:
            complete = {}
    except Exception as e:
        complete = {}
        print(str(e))
    return JsonResponse(complete,safe=False)