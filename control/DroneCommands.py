from dronekit import connect, VehicleMode
import DroneControl
import time
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import numpy as np


class DroneCommands:
    def __init__(self, vehicle, speed, alt):
        self.vehicle = vehicle
        self.control = DroneControl.DroneControl(self.vehicle)
        self.SPEED = speed
        self.ALTITUDE = alt

    def go_forward(self):
        self.control.send_ned_velocity(self.control.calculateX(self.SPEED, self.vehicle.heading),
                                       self.control.calculateY(self.SPEED, self.vehicle.heading), 0, 1)  # go forward

    def take_off(self):
        self.vehicle.mode = VehicleMode("GUIDED")
        while not self.vehicle.mode.name == "GUIDED":  # Wait until mode has changed
            print " Waiting for mode change ..."
            time.sleep(3)
        self.vehicle.armed = True
        while not self.vehicle.armed:
            print " Waiting for arming..."
            time.sleep(1)
        print "Vehicle is armed"
        self.vehicle.simple_takeoff(self.ALTITUDE)
        while self.vehicle.location.global_relative_frame.alt < self.ALTITUDE * 0.9:
            print self.vehicle.location.global_relative_frame.alt
            time.sleep(1)

    def go_right(self):
        self.control.send_ned_velocity(self.control.calculateX(self.SPEED, self.vehicle.heading + 90),
                                       self.control.calculateY(self.SPEED, self.vehicle.heading + 90), 0,
                                       1)  # go right

    def go_left(self):
        self.control.send_ned_velocity(self.control.calculateX(self.SPEED, self.vehicle.heading - 90),
                                       self.control.calculateY(self.SPEED, self.vehicle.heading - 90), 0,
                                       1)  # go left

    def go_back(self):
        self.control.send_ned_velocity(-self.control.calculateX(self.SPEED, self.vehicle.heading),
                                       -self.control.calculateY(self.SPEED, self.vehicle.heading), 0, 1)  # go backward

    def go_up(self):
        self.control.send_ned_velocity(0, 0, -self.SPEED, 1)  # go up

    def go_down(self):
        self.ontrol.send_ned_velocity(0, 0, self.SPEED, 1)  # go down

    def rotate_right(self):
        self.control.condition_yaw(self.vehicle.heading + 5)  # rotate to right

    def rotate_left(self):
        self.control.condition_yaw(self.vehicle.heading - 5)  # rotate to left

    def land(self):
        self.vehicle.mode = VehicleMode("LAND")
        self.vehicle.armed = False
        while not self.vehicle.armed == False:
            print "Stop"
            time.sleep(1)
            self.vehicle.close()
        print "Landed and closed"

    def go_home(self):
        print "GO HOME"
        self.vehicle.mode = VehicleMode("RTL")  # go home

    # Script for following
    def following_mode_1(self):
        """
        Opens socket and get data from vision part.Sends commands to drone for following object
        """

        PORT_NUMBER = 5000
        SIZE = 1024
        MAX_SPEED = 0.5
        verRes = 120  # vertical resolution of image
        gorRes = 216  # horizontal resolution of image
        hostName = gethostbyname('192.168.1.2')  # IP of another machine in local network

        mySocket = socket(AF_INET, SOCK_DGRAM)
        mySocket.bind((hostName, PORT_NUMBER))

        print ("Server listening on port {0}\n".format(PORT_NUMBER))

        try:
            print "Start Following mode.!!!Stop it by KeyboardInterrupt!!!"
            while self.vehicle.mode.name == "GUIDED":
                (data, addr) = mySocket.recvfrom(SIZE)
                print data
                listOfInts = data.split(' ')  # array of data margins of object in image
                yMargin = int(float(listOfInts[0]))  # horizontal margin
                xMargin = int(float(listOfInts[1]))  # vertical margin
                isTrack = bool(listOfInts[2])
                # vector show how far object from center of image and shows with which speed drone should fly
                vector = MAX_SPEED * np.sqrt(np.square(xMargin) + np.square(yMargin)) / np.sqrt(
                    np.square(verRes) + np.square(gorRes))
                if isTrack:
                    if xMargin != 0:  # avoid zero division
                        angle = np.rad2deg(np.arctan(yMargin / xMargin))  # angle for movement in degrees
                        if xMargin > 0:
                            self.control.send_ned_velocity(
                                self.control.calculateX(vector, self.vehicle.heading + angle),
                                self.control.calculateY(vector, self.vehicle.heading + angle), 0, 0.25)
                        if xMargin < 0:
                            self.control.send_ned_velocity(
                                -self.control.calculateX(vector, self.vehicle.heading + angle),
                                -self.control.calculateY(vector, self.vehicle.heading + angle), 0, 0.25)
                    else:
                        if yMargin > 0:
                            self.control.send_ned_velocity(0, -vector, 0.25)
                        if yMargin < 0:
                            self.control.send_ned_velocity(0, vector, 0.25)
                time.sleep(0.2)
                print "TRACKING"

        except KeyboardInterrupt:
            print 'Stop Following mode'
            return 1
