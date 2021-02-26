from levels.models import Level
from pricings.models import Pricing
from datetime import datetime
from django.utils import timezone

def decrease_level_available_spot(type_vehicle, level_selected):
    if type_vehicle == "car":
        level_selected.available_car_spots -= 1
        level_selected.save()
    elif type_vehicle == "bike":
        level_selected.available_bike_spots -= 1
        level_selected.save()


def increase_level_available_spot(type_vehicle, level_selected):
    if type_vehicle == "car":
        level_selected.available_car_spots += 1
        level_selected.save()
    elif type_vehicle == "bike":
        level_selected.available_bike_spots += 1
        level_selected.save()


def list_levels_type_vehicle(type_vehicle, levels):
    if type_vehicle == "car":
        list_levels = [level for level in levels if level.available_car_spots > 0]

    elif type_vehicle == "bike":
        list_levels = [level for level in levels if level.available_bike_spots > 0]
    
    return list_levels


def select_level_priority(type_vehicle):
    levels = Level.objects.all()
    
    if levels.count() == 0:
        return None

    list_levels = list_levels_type_vehicle(type_vehicle, levels)
    
    if list_levels == []:
        return None

    highest_priority, level_selected = (list_levels[0].fill_priority, list_levels[0])
    for level in list_levels:
        if level.fill_priority > highest_priority:
            highest_priority, level_selected = level.fill_priority, level

    decrease_level_available_spot(type_vehicle, level_selected)

    return level_selected


def timestamp():
    now = datetime.now(tz=timezone.utc)
    return now

def calculate_amount_paid(vehicle_arrived_at, timestamp_end):
    pricing = Pricing.objects.last()
    start = vehicle_arrived_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    end = timestamp_end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    f = '%Y-%m-%dT%H:%M:%S.%fZ'
    
    total_seconds = (datetime.strptime(end, f) - datetime.strptime(start, f)).total_seconds()
    total_hours = int(total_seconds / 60 / 60)

    value = pricing.a_coefficient + pricing.b_coefficient * total_hours

    return value