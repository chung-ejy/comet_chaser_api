from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
import requests
import os
from dotenv import load_dotenv
load_dotenv()
roster_key = os.getenv("ROSTERKEY")
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request, *args, ** kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            headers = {"Content-type":"application/json",
                        "x-api-key":roster_key}
            user_dict = UserSerializer(user,context=self.get_serializer_context()).data
            params = {"username":user_dict["username"]}
            requests.post(f"https://cometroster.herokuapp.com/api/roster/",headers=headers,data=params)
            return Response({
                "user":user_dict,
                "token": AuthToken.objects.create(user)[1]
            })
        else:
            return Response({
                "error":"username or email already registered"
            })

class LoginApi(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request, *args, ** kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data
            return Response({
                "user":UserSerializer(user,context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            })
        else:
            return Response({
                "error":"invalid_credentials"
            })

class UserApi(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user