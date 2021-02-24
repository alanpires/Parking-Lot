from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LevelSerializer
from .models import Level, Spot
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class LevelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LevelSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.is_staff and request.user.is_superuser:

            spot = Spot.objects.get_or_create(
                available_bike_spots = request.data['bike_spots'],
                available_car_spots = request.data['car_spots']
            )[0]
        
            level = Level.objects.get_or_create(
                name = request.data['name'],
            )[0]

            level.fill_priority = request.data['fill_priority']
            level.available_spots = spot
            level.save()

            serializer = LevelSerializer(level)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        levels = Level.objects.all()
        serializer = LevelSerializer(levels, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
