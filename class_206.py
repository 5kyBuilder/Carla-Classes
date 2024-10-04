import glob
import os
import sys
import random
import time
import numpy as np
import cv2

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

IM_WIDTH = 640
IM_HEIGHT = 480
actor_list = []

#Define function here named image
    #Store data using save_to_disk(in output folder with jpg extension)

def camera(get_blueprint_of_world):
    camera_sensor = get_blueprint_of_world.find('sensor.camera.rgb')
    camera_sensor.set_attribute('image_size_x', f'{IM_WIDTH}')
    camera_sensor.set_attribute('image_size_y', f'{IM_HEIGHT}')
    camera_sensor.set_attribute('fov', '70')

    return camera_sensor

def image(image):
    matrix_representational_data = np.array(image.raw_data)
    reshape_of_image = matrix_representational_data.reshape((IM_HEIGHT, IM_WIDTH, 4))

    live_feed_camera = reshape_of_image[:, :, :3]

    cv2.imshow("", live_feed_camera)    
    cv2.waitKey(1)

    return

try:
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    get_blueprint_of_world = world.get_blueprint_library()
    #Define vehicle name here and store in car_model variable
    car_model = get_blueprint_of_world.filter('model3')[0]
    spawn_point = random.choice(world.get_map().get_spawn_points())
    #Define spawn points for car and store in spawn_point variable
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)

    dropped_vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=1.0))  # if you just wanted some NPCs to drive.
    simulator_camera_location_rotation = carla.Transform(spawn_point.location, spawn_point.rotation)
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    dropped_vehicle.set_transform(spawn_point)

    camera_sensor = camera(get_blueprint_of_world)
    sensor_camera_spawnpoint = carla.Transform(carla.Location(x=2.5, z=0.7))
    sensor = world.spawn_actor(camera_sensor, sensor_camera_spawnpoint, attach_to=dropped_vehicle)
    actor_list.append(sensor)
    sensor.listen(lambda camera_data: image(camera_data))

    speed = lambda speed: carla.VehicleControl(throttle=speed)
    dropped_vehicle.apply_control(speed(0.5))

    time.sleep(11)

    steering = lambda steer: carla.VehicleControl(steer=steer)
    dropped_vehicle.apply_control(steering(0.5))

    time.sleep(5)
    actor_list.append(dropped_vehicle)
finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')