from Camera import Camera
from Camera_local import Camera_local
from Camera_hero4 import Camera_hero4
from Connection import Connection

class Camera_factory:
    def __init__(self):
        pass
        
    def give_local_cam(self, tracker='MEDIANFLOW', connection=False):
        cam = Camera_local(tracker, 30, None, 0.5)
        if connection:
            #connection = Connection('192.168.1.2', 5000)
            #cam.connection = connection
            cam.skip = 0
        return cam
        
    def give_hero_cam(self, tracker='MEDIANFLOW', connection=False):
        cam = Camera_hero4(tracker, 30, None, 0.5)
        if connection:
            #connection = Connection('192.168.1.2', 5000)
            #cam.connection = connection
            cam.skip = 0
            
        return cam
