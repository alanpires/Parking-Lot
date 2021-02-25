from levels.models import Level

def select_level_priority(type_vehicle):
    # verificando qual level tem maior prioridade e se tem vaga disponível
    levels = Level.objects.all()

    highest_priority, level = (levels[0].fill_priority, levels[0])
    for level in levels:
        if type_vehicle == "car" and level.available_car_spots > 0:
            if level.fill_priority > highest_priority:
                highest_priority, level = level.fill_priority, level
                level.available_car_spots = level.available_car_spots - 1
                level.save()
            
        elif type_vehicle == "bike" and level.available_bike_spots > 0:
            if level.fill_priority > highest_priority:
                highest_priority, level = level.fill_priority, level
                level.available_bike_spots = level.available_bike_spots - 1
                level.save()

    return level