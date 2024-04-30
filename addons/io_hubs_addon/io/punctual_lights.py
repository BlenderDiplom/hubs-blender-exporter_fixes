import bpy

LIGHT_INTENSITY_MULTIPLIER = 0.001
stored_lamps = []

def convert_lights(blacklist):
    global stored_lamps
    stored_lamps = []
    lights = [light for light in bpy.scene.objects if light.type in ['POINT', 'SPOT']]
    for light in lights:
        if light.name in blacklist:
            continue
        if light.type == 'POINT' and light.hubs_component_point_light is not None:
            light.energy *= LIGHT_INTENSITY_MULTIPLIER
            stored_lamps.append(light)
        elif light.type == 'SPOT' and light.hubs_component_spot_light is not None:
            light.energy *= LIGHT_INTENSITY_MULTIPLIER
            stored_lamps.append(light)

def restore_lights():
    for light in stored_lamps:
        light.energy /= LIGHT_INTENSITY_MULTIPLIER