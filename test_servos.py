from lx16a import *
import time
import numpy as np

LX16A.initialize("/dev/ttyUSB0", 0.1)

minN = 1
maxN = 9

servos = [0]

try:
    for i in range(minN, maxN):
        servos.append(LX16A(i))
        servos[i].set_angle_limits(0, 240)
        servos[i].enable_torque()

except ServoTimeoutError as e:
    print(f"INITIALIZATION ERROR: Servo {e.id_} is not responding. Exiting...")
    quit()

servos[5].move(100,time=1000)