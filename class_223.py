import glob
import os
import sys
import time

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

actor_list = []


def generate_radar_blueprint(blueprint_library):
    radar_blueprint = blueprint_library.filter('sensor.other.radar')[0]
    radar_blueprint.set_attribute('horizontal_fov', str(40))
    radar_blueprint.set_attribute('vertical_fov', str(30))
    radar_blueprint.set_attribute('points_per_second', str(15000))
    radar_blueprint.set_attribute('range', str(20))
    return radar_blueprint

def car_control():
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.51))
    time.sleep(1)

def check_traffic_lights():
    if dropped_vehicle.is_at_traffic_light():
        traffic_light = dropped_vehicle.get_traffic_light()
        if traffic_light.get_state() == carla.TrafficLightState.Red:
            dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))
            dropped_vehicle.set_light_state(carla.VehicleLightState(carla.VehicleLightState.Brake))
    else:
        dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.51))  


try:
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    get_blueprint_of_world = world.get_blueprint_library()
    car_model = get_blueprint_of_world.filter('model3')[0]
    spawn_point = (world.get_map().get_spawn_points()[20])
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)

    simulator_camera_location_rotation = carla.Transform(spawn_point.location, spawn_point.rotation)
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    actor_list.append(dropped_vehicle)

    radar_sensor = generate_radar_blueprint(get_blueprint_of_world)
    sensor_radar_spawn_point = carla.Transform(carla.Location(x=-0.5, z=1.8))
    sensor = world.spawn_actor(radar_sensor, sensor_radar_spawn_point, attach_to=dropped_vehicle)

    sensor.listen(lambda radar_data: _Radar_callback(radar_data))

    check_traffic_lights()
    def _Radar_callback(radar_data):
        distance_name_data = {}
        for detection in radar_data:
            distance_name_data["distance"] = detection.depth
            print("distance name and data: ", distance_name_data)
            if distance_name_data["distance"] > 3 and distance_name_data["distance"] < 6:
                print("Brake")
                dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))

                break
            else:
                check_traffic_lights()

    actor_list.append(sensor)
    check_traffic_lights()
    time.sleep(1000)
finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')