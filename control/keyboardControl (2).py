import time
from tabulate import tabulate
from pymavlink import mavutil
from pynput import keyboard
from dronekit import connect, VehicleMode
import dronekit_sitl
import numpy as np
from colorama import Fore, Back, Style
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import Connector
import DroneControl
import DroneCommands

SPEED = 3  # Speed in m/s
ALTITUDE = 4  # ALtitude in meters

connector = Connector.Connector()
vehicle = connector.connect()
control = DroneControl.DroneControl(vehicle)
drone = DroneCommands.DroneCommands(vehicle, SPEED, ALTITUDE)

print tabulate([['t', 'takeoff'], ['w', 'go forward'], ['s', 'go backward'], ['a', 'go left'], ['d', 'go right']
                   , ['r', 'rotate right'], ['e', 'rotate left'], ['i', 'go up'], ['k', 'go down'], ['esc', "land"]
                   , ['backspace', 'go home'], ['m(n)', 'altitude above ground(sea level)'], ['b', 'athimut']],
               headers=['button', 'action'])


def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 't':  # takeoff
        drone.take_off()
    elif k == 'm':
        print "\nAltitude" + str(vehicle.location.global_relative_frame.alt) + " m\n"  # Print altitude above sea level
    elif k == 'n':
        print "\nAltitude" + str(vehicle.location.global_frame.alt) + "m\n"  # print altitude above sea level
    elif k == 'a':
        drone.go_left()
    elif k == 'w':
        drone.go_forward()
    elif k == 'd':
        drone.go_right()
    elif k == 's':
        drone.go_back()
    elif k == 'i':
        drone.go_up()
    elif k == 'k':
        drone.go_down()
    elif k == 'r':
        drone.rotate_right()
    elif k == 'e':
        drone.rotate_left()
    elif k == 'b':
        print vehicle.heading  # print athimut
    elif key == keyboard.Key.esc:  # Landing
        drone.land()
    elif key == keyboard.Key.backspace:
        drone.go_home()
    elif k == 'f':  # Following mode 1
        drone.following_mode_1()


def on_release(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name
    if k == 'a' or k == 's' or k == 'w' or k == 'd' or k == 'i' or k == 'k':
        control.send_ned_velocity(0, 0, 0, 0)


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
