from  __future__ import print_function
import cv2
import time
import sys
from Camera import Camera


class Camera_local(Camera):

    def __init__(self, tracker, FPS, connection, resize):
        """
        Initialize variables, connections, etc
        @tracker - tracker class 
        @FPS - camera FPS
        @local - set True, if going to use webcam
        @connect - if needed another computer to send information. This is 
        sent using socket to 192.168.1.2 with port 5000
        """
        self.__tracker_name = tracker
        self.__FPS = int(FPS / 2)
        self.resize_factor = resize
        self.__tracker_active = False
        self.connection = connection
        self.skip = 0
    
    
    def start(self):
        """
        Initializing connecton and camera preparation
        """
        self.__cap = cv2.VideoCapture(0)
        ret, img_raw = self.__cap.read()
        check = 0 # try to connect to camera 5 times, else drop the program
        while not ret and check < 5:
            ret, img_raw = cap.read()
            check += 1
            
        if not ret and check == 5: 
            print("Camera can't be reached!")
            sys.exit(0)
            
        img = self.img_resize(img_raw, self.resize_factor) 
        
        self.__width = len(img[0]); self.__middle_w_coord = int(self.__width/2)
        self.__length = len(img); self.__middle_l_coord = int(self.__width/2)

        
    def run(self):
        """
        Start stream
        """
        time_s = 0
        while True:
        
            # loop time
            time_e = time.time()
            print("{}".format(time_e-time_s)) 
            time_s = time_e
            
            # show image
            for _ in range(self.skip): _1,_2 = self.__cap.read()
            ret, img_raw = self.__cap.read()
            
            if ret:
                img = self.img_resize(img_raw, self.resize_factor)

                if self.__tracker_active:
    
                    ok, bbox = self.__tracker.update(img)
                    if ok:
                        self.send_data(bbox)
                    bmin = int(min(bbox[2], bbox[3]))
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bmin), int(bbox[1] + bmin))
                    cv2.rectangle(img, p1, p2, (0, 0, 255))
                    
                cv2.imshow("My Window", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    # quit
                    break
                elif cv2.waitKey(1) & 0xFF == ord('a'):
                    print("Select Window")
                    self.adjust_selection_area()
                
        self.__cap.release()
        if self.connection is not None:
            self.connection.close()
        sys.exit()
            
    def send_data(self, bbox):
        bmin = int(min(bbox[2], bbox[3]))
        mid_w_frame = bbox[0]+int(bmin / 2)
        mid_l_frame = bbox[1] + int(bmin / 2)
        
        diff_x = mid_w_frame - self.__middle_w_coord
        diff_y = self.__middle_l_coord - mid_l_frame
        OK = (mid_w_frame != 0) or (mid_l_frame != 0)
        string = '{} {} {}'.format(diff_x, diff_y, OK)
        print(string)
        
        if self.connection is None:
            return
        else:
            self.connection.send(string)
            
        
    def adjust_selection_area(self):
        """
        Offer a ROI selection window for object remarking
        it also starts tracking, if needed
        """
        time_bs = time.time()
        ret, img_raw = self.__cap.read()
        if ret:
            img = self.img_resize(img_raw, self.resize_factor)
            bbox = cv2.selectROI(img, False)
            time_be = time.time()
            # skip frames while selecting
            for _ in range(int(self.__FPS * (time_be - time_bs))): _1, _2 = self.__cap.read()
            cv2.destroyWindow("ROI selector")
            
            self.__tracker = cv2.Tracker_create(self.__tracker_name)
            self.__tracker.init(img, bbox)
            
            self.__tracker_active = True
    
    def img_resize(self, img_raw, factor=1):
        if factor == 1: return img_raw
        else:           return cv2.resize(img_raw, (0,0), fx=factor, fy=factor) 
