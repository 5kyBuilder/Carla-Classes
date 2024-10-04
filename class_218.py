import glob
import os
import sys
import time
import random

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

actor_list = []


def car_control():
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.51))
    time.sleep(20)


try:
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    map = world.get_map()
    get_blueprint_of_world = world.get_blueprint_library()
    car_model = get_blueprint_of_world.filter('model3')[0]
    spawn_point = (world.get_map().get_spawn_points()[2])
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)

    #write code here for spawnning walker
    walker_blueprint = random.choice(get_blueprint_of_world.filter('walker'))
    walkers_spawn_point = world.get_map().get_spawn_points()[1]
    dropped_walker = world.spawn_actor(walker_blueprint, walkers_spawn_point)

    #write code here for providing speed and direction of walking
    control_walker = carla.WalkerControl()
    control_walker.speed = 2
    control_walker.x = 0
    control_walker.y = 1
    control_walker.z = 1000
    dropped_walker.apply_control(control_walker)

    simulator_camera_location_rotation = carla.Transform(walkers_spawn_point.location, walkers_spawn_point.rotation)
    simulator_camera_location_rotation.location += walkers_spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    actor_list.append(dropped_vehicle)

    car_control()

    time.sleep(1000)
finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')