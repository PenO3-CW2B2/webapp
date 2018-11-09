from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import HttpResponse
import requests
from django.conf import settings
from bikes import serializers, signals
from bikes.models import Bike, Contract
import datetime

class UserActivationView(APIView):
    """
    Used to verify an email address
    """
    def get (self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        host = request.get_host()
        url = protocol + host + "/" + settings.HOST_PREFIX + "auth/users/activate/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(url, data = post_data)
        if result.status_code == 204:
            return HttpResponse("Accout has been activated succesfully.")
        if result.status_code == 400:
            return HttpResponse("Bad request. Make sure you have copied/enetered the whole URL.")
        if result.status_code == 403:
            return HttpResponse("This account has already been activated.")

class bikeCreateView(generics.CreateAPIView):
    serializer_class = serializers.BikeSerializer
    permission_classes = (IsAdminUser,)


class bikeDeleteView(generics.DestroyAPIView):
    serializer_class = serializers.BikeSerializer
    permission_classes = (IsAdminUser,)

class contractCreateView(generics.CreateAPIView):
    serializer_class = serializers.ContractSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.users
        bike = Bike.objects.get(id=elf.request.data.bike_id)
        contract = serializer.save(user=user, bike=bike)

class userBike(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        bikes = request.user.bike_set().filter(time_end=None or time_end <= datetime.datetime.now())
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data)

class userContracts(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        contracts = request.user.contract_set().all()
        serializer = ContractSerializer(contracts, many=True)
        return Repsone(serializer.data)

class bikeList(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        bikes = Bike.objects.all()
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data)

class bikeDetails(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        bike = Bike.objects.get(id=pk)
        serializer = BikeSerializer(bike)
        return Response(serializer.data)

class contractList(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

class contractDetails(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        contract = Contract.objects.get(id=pk)
        serializer = ContractSerializer(contract)
        return Response(serializer.data)
