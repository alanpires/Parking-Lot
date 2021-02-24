from rest_framework import serializers


class SpotSerializer(serializers.Serializer):
    available_bike_spots = serializers.IntegerField()
    available_car_spots = serializers.IntegerField()


class LevelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    fill_priority = serializers.IntegerField()
    available_spots = SpotSerializer(read_only=True)
