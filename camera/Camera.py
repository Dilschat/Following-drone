from  __future__ import print_function
import cv2
import socket
import numpy as np
import time
import sys
from urllib2 import urlopen
import Connection

class Camera:
    """
    Camera capturing and connection handler
    """
    def __init__(self, tracker, FPS, connection, resize):
        """
        Initialize variables, connections, etc
        @tracker - tracker class 
        @FPS - camera FPS
        @local - set True, if going to use webcam
        @connect - if needed another computer to send information. This is 
        sent using socket to 192.168.1.2 with port 5000
        """
        raise NotImplementedError
    
    def start(self):
        """
        Initializing connecton and camera preparation
        """
        raise NotImplementedError
        
    def run(self):
        """
        Start stream
        """
        raise NotImplementedError
        
    def adjust_selection_area(self):
        """
        Offer a ROI selection window for object remarking
        """
        raise NotImplementedError
    
    def img_resize(img_raw, factor=1):
        raise NotImplementedError
