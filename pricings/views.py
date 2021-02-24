from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import PricingSerializer
from rest_framework.response import Response
from .models import Pricing
from rest_framework import status


class PricingView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        serializer = PricingSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.is_superuser and request.user.is_staff:
            pricing = Pricing.objects.get_or_create(
                a_coefficient = request.data['a_coefficient'],
                b_coefficient = request.data['b_coefficient']
            )[0]

            serializer = PricingSerializer(pricing)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)