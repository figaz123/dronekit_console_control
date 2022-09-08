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



def arm_and_takeoff(altitude_vehicle):
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
    aTargetAltitude = vehicle.simple_takeoff(altitude_vehicle)  

    return aTargetAltitude

def input_waypoint():
    print("Welcome, please input autonomous data for vehicle")
    print("please input your altitude desire: ")
    altitude_vehicle = input()
    print("please input your latitude: ")
    latitude_vehicle = input()
    print("please input your longitude: ")
    longitude_vehicle = input()
    #vehicle_airspeed = input()
    #print("please input your vehicle airspeed: ", vehicle_airspeed)

    return [altitude_vehicle, latitude_vehicle, longitude_vehicle]

while True:
    input_waypoint()
    print(" Altitude: ", vehicle.location.global_relative_frame.alt)
    if vehicle.location.global_relative_frame.alt >= arm_and_takeoff() * 0.95:
        print("Reached target altitude")
        break
    time.sleep(1)
    print("vehicle move")
    print('Going to longitude (%s) latitude (%s) altitude (%s) with airspeed(%s)'% (input_waypoint(0),
                                                                                    input_waypoint(1),
                                                                                    input_waypoint(2),
                                                                                    ))
    point = LocationGlobalRelative(input_waypoint(0), input_waypoint(1), input_waypoint(2))
    vehicle.simple_goto(point)
    time.sleep(10)

vehicle.close()

if sitl:
    sitl.stop()
