from rest_framework import serializers


class SpotSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    variety = serializers.CharField(read_only=True)
    level_name = serializers.CharField()


class VehicleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    license_plate = serializers.CharField()
    vehicle_type = serializers.CharField()
    arrived_at = serializers.CharField(read_only=True)
    paid_at = serializers.CharField(read_only=True)
    amount_paid = serializers.IntegerField(read_only=True)
    spot = SpotSerializer(read_only=True)