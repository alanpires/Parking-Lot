from levels.models import Level

def update_level_available_spots(type_vehicle, level_selected):
    if type_vehicle == "car":
        level_selected.available_car_spots -= 1
        level_selected.save()
    elif type_vehicle == "bike":
        level_selected.available_bike_spots -= 1
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

    update_level_available_spots(type_vehicle, level_selected)

    return level_selected