from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VehicleSerializer
from .models import Vehicle, Spot
from levels.models import Level
from pricings.models import Pricing
from .services import select_level_priority
import ipdb

class VehicleView(APIView):
    def post(self, request):
        serializer = VehicleSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        level_priority = select_level_priority(request.data['vehicle_type'])

        pricing = Pricing.objects.count()

        if level_priority is not None and pricing:
            spot = Spot.objects.create(
                variety = request.data['vehicle_type'],
                level = level_priority
            )

            vehicle = Vehicle.objects.get_or_create(
                vehicle_type = request.data['vehicle_type'],
                license_plate = request.data['license_plate'],
                arrived_at = "2021-01-25T17:16:25.727541Z",
                paid_at = None,
                amount_paid = None,
                spot = spot
            )[0]
            
            serializer_data = {
                    "id": vehicle.id,
                    "license_plate": vehicle.license_plate,
                    "vehicle_type": vehicle.vehicle_type,
                    "arrived_at": vehicle.arrived_at,
                    "paid_at": vehicle.paid_at,
                    "amount_paid": vehicle.amount_paid,
                    "spot": {
                    "id": spot.id,
                    "variety": spot.variety,
                    "level_name": spot.level.name
                        }
                    }
            
            serializer = VehicleSerializer(serializer_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_404_NOT_FOUND)