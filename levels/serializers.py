from rest_framework import serializers
from vehicles.serializers import SpotSerializer


class LevelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    fill_priority = serializers.IntegerField()
    available_spots = serializers.DictField(child=serializers.IntegerField() ,read_only=True)