from Camera_factory import Camera_factory

if __name__ == '__main__':
    camera_factory = Camera_factory()
    cam = camera_factory.give_hero_cam()
    cam.start()
    cam.run()
