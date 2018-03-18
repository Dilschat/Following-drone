from dronekit import connect, VehicleMode
import dronekit_sitl
import sys
from colorama import Fore, Back, Style


class Connector(object):
    simulator_udp = 'udp:127.0.0.1:14551'
    real_udp = 'udpin:0.0.0.0:14550'

    def __init__(self):  # this method creates the class object.
        pass

    def connect(self):
        print "Start"

        try:
            print "Connecting to simulator...."
            self.drone = connect(self.simulator_udp, wait_ready=True)  # Connecting to simulator
        except:
            try:
                print "Connecting to real drone...."
                self.drone = connect(self.real_udp, wait_ready=True)  # Connecting to real drone
            except:
                print (Fore.RED + "No Vehicle")
                sys.exit()
        print "connected"

        print "Vehicle controlled by keyboard......."
        return self.drone
