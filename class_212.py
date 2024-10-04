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


# Show camera sensor result with raw data, reshape image, show image with opencv
def image(image):
    matrix_representational_data = np.array(image.raw_data)
    reshape_of_image = matrix_representational_data.reshape((IM_HEIGHT, IM_WIDTH, 4))
    live_feed_from_camera = reshape_of_image[:, :, :3]
    cv2.imshow("", live_feed_from_camera)
    cv2.waitKey(1)
    return


# camera sensor, width, height and fov
def camera(get_blueprint_of_world):
    camera_sensor = get_blueprint_of_world.find("sensor.camera.rgb")
    camera_sensor.set_attribute("image_size_x", f'{IM_WIDTH}')
    camera_sensor.set_attribute("image_size_y", f'{IM_HEIGHT}')
    camera_sensor.set_attribute("fov", "70")
    return camera_sensor


data = []
actor_list = []
try:
    # Carla world defination which includes carla host, port, set timeout, Initialised carla world and get blueprint library
    client = carla.Client("127.0.0.1", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    get_blueprint_of_world = world.get_blueprint_library()

    # Defination of car model, spawn point for car, address spawn point to car model, set driving mode as autopilot
    car_model = get_blueprint_of_world.filter("model3")[0]
    spawn_point = random.choice(world.get_map().get_spawn_points())
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)
    dropped_vehicle.set_autopilot(True)

    # Define carla simulation camera, location, rotation, forword focus, angle
    simulator_camera_location_rotation = carla.Transform(spawn_point.location, spawn_point.rotation)
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)

    # Define camera sensor, location for sensor, attach camera sensor to car, listen method to show result
    camera_sensor = camera(get_blueprint_of_world)
    sensor_camera_spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    sensor = world.spawn_actor(camera_sensor, sensor_camera_spawn_point, attach_to=dropped_vehicle)
    sensor.listen(lambda cameraData: image(cameraData))

    # actor list for sensor and dropped vehicle
    actor_list.append(sensor)
    actor_list.append(dropped_vehicle)

    # time sleep
    time.sleep(1000)
finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')