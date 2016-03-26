
import Sensor
import Motion
import Camera

def init():
    global motion
    global sensor
    global arduino_to_write
    global Camera

    motion = Motion.Motion()
    sensor = Sensor.Sensor()
    camera = Camera.Camera()
    arduino_to_write = []
