
import Sensor
import Motion

def init():
    global motion
    global sensor
    global arduino_to_write

    motion = Motion.Motion()
    sensor = Sensor.Sensor()
    arduino_to_write = []
