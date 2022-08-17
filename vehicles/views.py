from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VehicleSerializer, ExitVehicleSerializer
from .models import Vehicle, Spot
from levels.models import Level
from pricings.models import Pricing
from .services import select_level_priority, calculate_amount_paid, timestamp, increase_level_available_spot
from django.core.exceptions import ObjectDoesNotExist

# Entrada de veículos no estacionamento
class VehicleView(APIView):
    def post(self, request):
        serializer = VehicleSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Selecionar nível de prioridade
        level_priority = select_level_priority(request.data['vehicle_type'])

        pricing = Pricing.objects.count()

        if level_priority is not None and pricing:
            timestamp_inicial = timestamp()
            
            # Cria a vaga assim que o veículo entra
            spot = Spot.objects.create(
                variety = request.data['vehicle_type'],
                level = level_priority
            )

            # Cria o veículo e o associa a vaga
            vehicle = Vehicle.objects.get_or_create(
                vehicle_type = request.data['vehicle_type'],
                license_plate = request.data['license_plate'],
                arrived_at = timestamp_inicial,
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
    
    def put(self, request, vehicle_id=''): 
        if vehicle_id:

            try:
                timestamp_end = timestamp()
                vehicle = Vehicle.objects.get(id=vehicle_id)

                vehicle.paid_at = timestamp_end

                # Calcula o valor a ser pago pelo veículo
                vehicle.amount_paid = calculate_amount_paid(vehicle.arrived_at, timestamp_end)
                vehicle.save()

                # Seleciona a vaga do veículo
                spot = Spot.objects.get(id=vehicle.spot.id)

                # Aumenta uma vaga disponível no nível
                increase_level_available_spot(vehicle.vehicle_type, spot.level)
                
                # Exclui o veículo da vaga
                spot.delete()

                vehicle = Vehicle.objects.get(id=vehicle_id)

                serializer_data = {
                    "license_plate": vehicle.license_plate,
                    "vehicle_type": vehicle.vehicle_type,
                    "arrived_at": vehicle.arrived_at,
                    "paid_at": vehicle.paid_at,
                    "amount_paid": vehicle.amount_paid,
                    "spot": vehicle.spot
                    }
                
                serializer = ExitVehicleSerializer(serializer_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            except ObjectDoesNotExist:
                return Response({"message": "Invalid vehicle id"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)