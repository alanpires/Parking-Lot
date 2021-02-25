from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VehicleSerializer
from .models import Vehicle


class VehicleView(APIView):
    def post(self, request):
        serializer = VehicleSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        vehicle = Vehicle.objects.get_or_create(
            vehicle_type = request.data['vehicle_type'],
            license_plate = request.data['licence_plate']
        )[0]