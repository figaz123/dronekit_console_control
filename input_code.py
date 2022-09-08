from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

def arm_and_takeoff(alt_veh):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    alt_veh = vehicle.simple_takeoff(alt_veh)  

    return alt_veh

def input_waypoint():
    print("Welcome, where do you want to go?")
    print("please input your altitude desire: ")
    altitude_vehicle = input()
    print("please input your latitude: ")
    latitude_vehicle = input()
    print("please input your longitude: ")
    longitude_vehicle = input()
    print("please input your groundspeed: ")
    groundspeed_vehicle = input()
    #vehicle_airspeed = input()
    #print("please input your vehicle airspeed: ", vehicle_airspeed)

    return [altitude_vehicle, latitude_vehicle, longitude_vehicle, groundspeed_vehicle]

while True:
    input_waypoint()
    print(" Altitude: ", vehicle.location.global_relative_frame.alt)
    if vehicle.location.global_relative_frame.alt >= arm_and_takeoff() * 0.95:
        print("Reached target altitude")
        break
    alt_veh = input_waypoint(0)
    lat_veh = input_waypoint(1)
    lon_veh = input_waypoint(2)
    gro_speed = input_waypoint(3)
    print("vehicle move")
    print('Going to longitude (%f) latitude (%f) altitude (%f)'% (alt_veh,
                                                                  lat_veh,
                                                                  lon_veh,
                                                                  ))
    point = LocationGlobalRelative(lon_veh, lat_veh, alt_veh)
    vehicle.simple_goto(point, groundspeed=gro_speed)
    time.sleep(10)

vehicle.close()

if sitl:
    sitl.stop()
