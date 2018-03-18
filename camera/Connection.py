from  __future__ import print_function
import socket
import sys
from urllib2 import urlopen

class Connection:
    """
    Used to send data via socket
    """
    def __init__(self, server_ip, port_number, size=1024):
        """
        @server_ip
        """
        self.__server_ip = server_ip
        self.__port_number = port_number
        self.__size = size
        self.__controller = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        
    def send(self, string):
        self.__controller.sendto(string, (SERVER_IP, PORT_NUMBER))
        return True
        
    def close(self):
        self.__controller.close()
